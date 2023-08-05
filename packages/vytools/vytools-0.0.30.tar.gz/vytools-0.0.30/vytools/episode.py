
import vytools.utils
import vytools.compose
import vytools.definition
import vytools.object
from termcolor import cprint
from pathlib import Path
from vytools.config import CONFIG
import re, json, shutil, os, yaml, subprocess, sys
import signal
import cerberus
import logging

SCHEMA = vytools.utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['episode']},
  'finished': {'type':'string', 'maxlength': 64},
  'tags':{'type':'list','schema': {'type': 'string', 'maxlength':64}},
  'root':{'type':'string', 'maxlength': 64},
  'course':{'type':'string', 'maxlength': 64},
  'passed':{'type':'boolean'},
  'expectation':{'type':'boolean'},
  'data':{'type': 'string', 'maxlength': 64},
  'data_modified':{'type': 'boolean', 'required': False}
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items):
  success = True
  
  def checkadd(item, label, typ):
    if label in item:
      fullname = typ+':'+item[label]
      if fullname in items: item['depends_on'].append(fullname)
  
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'episode',
    'path':pth
  }
  type_name = 'episode:' + name
  item['depends_on'] = [] # ['repo:'+item['repo']] if len(item['repo']) > 0 else []
  try:
    with open(pth,'r') as r:
      content = json.loads(r.read())
      for sc in SCHEMA:
        if sc in content:
          item[sc] = content[sc]
      checkadd(item, 'root', 'compose')
      checkadd(item, 'data', 'object')
    items[type_name] = item
    if 'compose:' + item['root'] in items:
      assembly = items['compose:' + item['root']]
    else:
      logging.error('The compose "{c}" in episode "{n}" at "{p}" was not found'.format(n=name, p=pth, c=item['root']))
      success = False
  except Exception as exc:
    logging.error('Failed to parse episode "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    success = False

  if not VALIDATE.validate(item):
    logging.error('"{n}" at "{p}" failed validation {s}'.format(n=name, p=pth, s=VALIDATE.errors))
    success = False

  if type_name in items and not success:
    del items[type_name]

  return success

def find_all(items):
  return vytools.utils.search_all(r'(.+)\.episode\.json', parse, items)

def build(type_name, build_arg_dict, items, built, build_level, data=None, data_mods=None):
  item = items[type_name]
  rootcompose = 'compose:'+item['root']
  objdata = 'object:'+item['data']
  if data is None:
    data = items[objdata]['data'] if objdata in items else {}
  return _build(rootcompose, build_arg_dict, items, built, build_level, data, data_mods)

def _build(rootcompose, build_arg_dict, items, built, build_level, data=None, data_mods=None):
  if data is None:
    data = {}
  elif type(data) == str and data in items:
    data = items[data]['data']
  return vytools.compose.build({'name':rootcompose,'parent_data':data,'data_mods':data_mods},
                        build_arg_dict, items, built, build_level)

global SHUTDOWN
SHUTDOWN = {'path':'','down':[],'logs':[],'services':[]}
def stop():
  logs = subprocess.run(SHUTDOWN['logs'], cwd=SHUTDOWN['path'], stdout=subprocess.PIPE)
  subprocess.run(SHUTDOWN['down'], cwd=SHUTDOWN['path'])
  return logs

def compose_exit_code(jobpath):
  success = True
  try:
    anyzeros = False
    if not os.path.isdir(jobpath):
      return False

    # Get services, wish there was a better way...
    services = []
    for s in subprocess.check_output(SHUTDOWN['services'], 
        cwd=SHUTDOWN['path']).decode('ascii').strip().split('\n'):
      count = 1
      while True:
        name = SHUTDOWN['jobid']+'_'+s+'_'+str(count)
        count+=1
        if name not in services:
          break
      services.append(name)

    for service in services:
      try:
        exitcode = subprocess.check_output(['docker', 'container', 'inspect',service,'--format','{{.State.ExitCode}}']).decode('ascii').strip()
      except Exception as exc:
        success = False
        exitcode = '1'
        logging.error('Failed to get exit code for {s}: {e}'.format(s=service, e=exc))
      anyzeros |= int(exitcode) == 0
      logging.info('---- Service '+service+' exited with code '+exitcode)
    return success and anyzeros
  except Exception as exc:
    logging.error('Failed to get exit codes'+str(exc))
    return False

ORIGINAL_SIGINT = signal.getsignal(signal.SIGINT)
def exit_gracefully(signum, frame):
  signal.signal(signal.SIGINT, ORIGINAL_SIGINT) # restore the original signal handler
  logs = stop()
  sys.exit(signum) # TODO is this right? pass out signum?

def get_job_id(episode):
  return episode['name'].lower()

def artifact_paths(episode_name, items):
  if episode_name not in items:
    return {}
  episode = items[episode_name]
  jobpath = CONFIG.job_path(relpath=get_job_id(episode),create=False)
  return vytools.compose.artifact_paths(jobpath, 'compose:'+episode['root'], items)

def run(type_name, build_arg_dict, items, save, clean, data=None, data_mods=None):
  if type_name not in items: return False
  episode = items[type_name]
  jobid = get_job_id(episode)
  jobpath = CONFIG.job_path(relpath=jobid,create=True)
  if data is None:
    data = 'object:'+episode['data']
  results = _run(jobid, 'compose:'+episode['root'], build_arg_dict, items, save, clean, data=data, data_mods=data_mods)
  if results:
    with open(os.path.join(jobpath, episode['name']+'.job.json'),'w') as w2:
      w2.write(json.dumps(results))
  return results

def _run(jobid, compose_name, build_arg_dict, items, save, clean, data=None, data_mods=None):
  global SHUTDOWN
  # TODO test jobid, lower case, alphanumeric starts with alpha?
  deplist = [compose_name,data] if type(data) == str else [compose_name]
  results = {'is_data_modified':data is not None or data_mods is not None}
  jobpath = CONFIG.job_path(relpath=jobid,create=True)
  if not jobpath:
    return False

  if clean:
    try:
      shutil.rmtree(jobpath)
      jobpath = CONFIG.job_path(relpath=jobid,create=True)
    except Exception as exc:
      logging.error('Failed to clean .../.vy/jobs folder {n}'.format(n=jobpath))
      return False

  build_args = build_arg_dict.copy()
  built = {}
  composition = _build(compose_name, build_args, items, built, -1, data, data_mods) # get components
  if composition == False: return False

  cmd = ['docker-compose']
  for k in sorted(composition.keys(), key = lambda j: composition[j]['i']):
    cmpse = composition[k]
    cname = k+'.compose.yaml'
    cmd += ['-f',cname]
    with open(os.path.join(jobpath, cname),'w') as w:
      yaml.safe_dump(cmpse['compose'], w, default_flow_style=False)
    if 'volume' in cmpse:
      with open(os.path.join(jobpath,k+'_cal.json'),'w') as w2:
        w2.write(json.dumps(cmpse['volume']))

  cmd += ['--project-name', jobid]

  cmdup = cmd+['up', '--abort-on-container-exit']
  SHUTDOWN['down'] = cmd + ['down','--volumes']
  SHUTDOWN['jobid'] = jobid
  SHUTDOWN['path'] = jobpath
  SHUTDOWN['logs'] = cmd + ['logs']
  SHUTDOWN['services'] = cmd + ['ps','--services']
  try:
    signal.signal(signal.SIGINT, exit_gracefully)
  except Exception as exc:
    logging.warning(str(exc))
    
  with open(os.path.join(jobpath,'start.sh'),'w') as w2:
    w2.write(' '.join(cmdup))

  proc = subprocess.run(cmdup, cwd=jobpath)
  compose_exit = compose_exit_code(jobpath)
  stop()
  
  results['passed'] = compose_exit and proc.returncode == 0
  logging.info(' --- done with episode execution: '+jobid)
  logging.info(' --- done reading output of run episode: '+jobid)
  
  checked = vytools.utils.get_repo_versions(deplist, items)
  for v in checked.values():
    cprint(v,'yellow' if v.endswith('+') else 'green')
  results['repos'] = [v for v in checked.values()]

  # if episode['repo'] in checked:
  #   del checked[episode['repo']] # Remove the repository containing this episode

  results['artifacts'] = vytools.compose.artifact_paths(jobpath,compose_name,items)
  return results
