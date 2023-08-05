import os, re, logging, json, subprocess, copy, time
import vytools.utils as utils
from vytools.config import CONFIG
from pathlib import Path
import cerberus
from termcolor import cprint

#todo NOT SURE THIS IS THE RIGHT REGEX
COPY_STAGE_A = re.compile('^copy[\s]+--from=[\'"]?([\w-]+)',re.I | re.M)
COPY_STAGE_B = re.compile('^from[\s]+([\w\-:\.\/]+)',re.I | re.M)
COPY_REPO = re.compile('^copy[\s]+[\'"]?([\w-]+)',re.I | re.M)
INFOCOLOR = 'blue'

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['stage']},
  'build_context':{'type':'string', 'maxlength': 1024},
  'secrets':{'type':'list','schema': {'type': 'string', 'maxlength':64}},
  'args':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'key': {'type': 'string', 'maxlength': 64},
        'value': {'type': 'string', 'maxlength': 64}
      }
    }
  }
})

VALIDATE = cerberus.Validator(SCHEMA)

def get_repo_info(name):
  return {'type':'git','source':'bitbucket','account':'autonomoussolutions','name':name}

def line_before_escape(line):
  return re.split(r'([^\\]#)',line)[0]      # All characters before unescaped # (comments)

def remove_quotes(line):
  if line.startswith('"') and line.endswith('"'):
    return line.strip('"')
  elif line.startswith("'") and line.endswith("'"):
    return line.strip("'")
  else:
    return line

def dependencies(stage_text,stage_sources):
  dependency = []
  args = []
  started = False
  for linex in stage_text.splitlines(): # TODO would be nice to preserve backslash continuation lines as one line
    line = linex.strip()
    if line.startswith('#'): continue         # need this
    line = line_before_escape(line)           # All characters before unescaped # (comments)
    m = re.match(COPY_STAGE_A, line)
    if not m:
      m = re.match(COPY_STAGE_B, line)
      if m: started = True
    if m and 'stage:'+m.group(1) not in dependency:  # COPY/FROM STAGE
      sn = m.group(1)
      stage_sources[sn] = '?' if sn not in stage_sources else stage_sources[sn]
      if stage_sources[sn] != '':
        dependency.append('stage:'+m.group(1))  # add dependency
    if started: # For multistage builds only get args AFTER FROM (only these will work)
      m = re.match(r'^[\s]*arg[\s]+(.+)',line,re.I)
      if m:
        argline = line_before_escape(m.group(1)).split('=',1)
        argkey = argline[0].strip()
        argval = argline[1].strip() if len(argline) > 1 else ''
        if argkey not in [a['key'] for a in args]:
          args.append({'key':argkey, 'value':remove_quotes(argval)}) 
  return (dependency, args)

def parse(namein, pth, reponame, items):
  name = namein.lower() # Stages must be unique case insensitively
  with open(pth,'r') as r:
    stage_text = r.read()
  secrets = []
  build_context = '.'
  sources = {}
  for line in stage_text.splitlines():
    m = re.search(r'^#vy(.+)', line, re.I | re.M)
    if m:
      try:
        obj = json.loads(m.group(1))
        build_context = obj.get('context',build_context)
        sources.update(obj.get('source',{}))
      except Exception as exc:
        logging.error('Failed to read potential vy json comment ({c}) in "{p}"'.format(c=m.group(1), p=pth))
        return False
    m = re.search(r'--mount=type=secret(.+)',line,re.I | re.M)
    if m:
      m = re.search(r'id=([^\s]+)',m.group(1),re.I | re.M)
      if m and m.group(1) not in secrets:
        secrets.append(m.group(1))
  type_name = 'stage:'+name
  if type_name in items:
    logging.error('Found stage "{n}" at {p1} but a stage of that name already exists at {p2}'.format( \
      n=name, p1=pth, p2=items[type_name]['path']))
  elif os.path.isabs(build_context):
    logging.error('Stage build contexts should be relative paths "{p}"'.format(p=build_context))
  else:
    (dependency,args) = dependencies(stage_text,sources)
    item = {'name':name,
      'thingtype':'stage',
      'path':pth,
      'repo':reponame,
      'args':args,
      'secrets':secrets,
      'build_context':str(Path(os.path.join(os.path.dirname(pth),build_context)).resolve()),
      'sources':sources,
      'depends_on':dependency
    }
    # if len(reponame) > 0: item['depends_on'].append('repo:'+reponame)
    if VALIDATE.validate(item):
      items[type_name] = item
      return True
    else:
      logging.error('Stage "{n}" at "{p}" failed validation {s}'.format(n=name, p=pth, s=VALIDATE.errors))
  return False

TAGSAFE = lambda v : re.sub(r'[^a-zA-Z0-9\-\_]','_',v)
ARGTAG = lambda k,a : TAGSAFE(k) + '.' + TAGSAFE(a[k])
def __build__(stage, already_tagged, build_arg_dict):
  stage_name = 'stage:'+stage['name']
  tag = already_tagged[stage_name]['tag']
  with open(stage['path'], 'r') as r:
    contents = r.read().replace('${VYNAME}',stage['name'])
  text = '# syntax=docker/dockerfile:experimental\n'    
  for (k,v) in build_arg_dict.items():
    text += 'ARG {k}="{v}"\n'.format(k=k,v=v)
  for s in stage['depends_on']:
    st = already_tagged[s]
    text += 'FROM {t} as {s}\n'.format(t=st['tag'],s=st['name'])
  for line in contents.splitlines(): #TODO nice to preserve backslash continuation
    text += line+'\n'
    if re.search(r'^[\s]*FROM ',line,re.I):
      text += 'LABEL tools.vy.remove=true\nLABEL tools.vy.tag=-\n'
  text += 'LABEL tools.vy.tag=' + tag + '\n# ----------------------------------------\n\n\n'

  build_context = stage['build_context']
  jobpath = CONFIG.job_path()
  if not jobpath:
    return False
  df = os.path.join(jobpath, tag+'.dockerfile')
  with open(df,'w') as w: w.write(text)
  cmd = ['docker', 'build', '--force-rm', '-f', df,'-t',tag]  # don't tag because of cleanup , '-t', node['s['tag']']
  cmd += ['--progress=plain']
  for (k,v) in build_arg_dict.items():
    cmd += ['--build-arg',k+'='+v]

  ok,cmds = CONFIG.secrets_cmd(stage['secrets'])
  if not ok:
    logging.error('Failed to build '+tag)
    return False
  else:
    cmd += cmds
    cmd += [build_context]
    # cprint(' '.join(cmd),INFOCOLOR)
    # cprint('\n'+text,INFOCOLOR)
    logging.info('** Building image '+tag)
    proc = subprocess.run(cmd, env={'DOCKER_BUILDKIT':'1'})
    success = proc.returncode == 0
    if success:
      already_tagged[stage_name]['hash'] = subprocess.check_output(['docker','inspect','--format','{{.ID}}',tag]).decode('utf-8').strip()
      clean_up(['dangling=true','label=tools.vy.tag='+tag])
      # os.remove(df)
    else:
      logging.error('Failed to build '+tag)
  return success

def sorted_vy_images(filters):
  cmd = ['docker','images']
  for f in filters:
    cmd += ['--filter',f]
  cmd += ['--format','{{.CreatedAt}}\t{{.ID}}\t{{.Repository}}\t{{.Tag}}']
  imlist = subprocess.check_output(cmd).decode('ascii').strip()
  if len(imlist) > 0:
    images = []
    for im in imlist.split('\n'):
      imageid = im.split('\t')
      images.append({'created':imageid[0], 'id':imageid[1], 'repo':imageid[2], 'tag':imageid[3]})
    return sorted(images, key=lambda k: k['created'], reverse=True) # Most recent first
  return []

def clean_up(filters):
  untagged = [im['id'] for im in sorted_vy_images(filters)]
  untagged.reverse()
  if len(untagged) > 0:
    while True:
      try:
        logging.info('Attempting to remove dangling images:'+str(untagged))
        subprocess.check_output(['docker','rmi']+untagged)
        break
      except Exception as exc:
        logging.warning(str(exc))
        time.sleep(5)

def find_all(items):
  # r'[.]*dockerfile[.]*'
  return utils.search_all(r'(.+)\.stage\.dockerfile', parse, items)

def check_args(stages, build_arg_dict, items):
  success = True
  def __add_args__(name):
    for arg in items[name]['args']:
      if arg['key'] not in build_arg_dict or len(build_arg_dict[arg['key']]) == 0:
        build_arg_dict[arg['key']] = arg['value']
    for s in items[name]['depends_on']: __add_args__(s)
  for name in stages:
    __add_args__(name)
  for (key,val) in build_arg_dict.items():
    if len(val)==0:
      logging.error('ARG {k} is required and does not have a default value'.format(k=key))
      success = False
  return success

def build(stages, items, build_arg_dict, already_built, build_level):
  # build_level = 1 # Rebuild all - unless you've already
  # build_level = 0 # Rebuild top level - unless you've already sometime 
  # build_level = -1 # Don't build anything
  existing_images = [im['repo']+':'+im['tag'] for im in sorted_vy_images(['label=tools.vy.tag'])]
  already_tagged = {}
  def __multistage__(stage_name):
    stage = items[stage_name]
    my_dep_args = [sa['key'] for sa in stage['args']]
    for s in stage['depends_on']:
      da = __multistage__(s)
      if da == False: return False
      my_dep_args += [a for a in da if a not in my_dep_args]
    if stage_name not in already_tagged:
      keys = list(build_arg_dict.keys())
      keys.sort()
      lst = [ARGTAG(key,build_arg_dict) for key in keys if key in my_dep_args]
      tag = 'vy__' + stage['name'].lower() + (':' + '.'.join(lst) if len(lst) > 0 else ':latest')
      already_tagged[stage_name] = {'tag':tag,'name':stage['name'],'skipped':False}
      oktobuild = ((build_level == 0 and stage_name in stages) or
                  (build_level == 1) or (tag not in existing_images)) and tag not in already_built
      if oktobuild:
        cprint('  - Building: '+stage_name,INFOCOLOR)
        this_args = {}
        for key in my_dep_args:
          if key in build_arg_dict:
            cprint('    - ARG {k}={v}'.format(k=key,v=build_arg_dict[key]),INFOCOLOR)
            this_args[key] = build_arg_dict[key]
          else:
            logging.error('Building {s} requires setting build argument "{b}"'.format(s=stage_name,b=key))
            return False
        if not __build__(stage, already_tagged, this_args): # Build this stage
          cprint('  - Failed {s} as {i}'.format(s=stage_name,i=tag),'red')
          return False
        already_built.append(tag)
        cprint('  - Finished: {s} as {i}'.format(s=stage_name,i=tag),'green')
        print('\n\n')
      else:
        already_tagged[stage_name]['skipped'] = True
        cprint('  - Skipping: {s} as {i}'.format(s=stage_name,i=tag),INFOCOLOR)

    return my_dep_args

  for top_name in stages:
    if False == __multistage__(top_name):
      return False

  if True:
    print('')
    for tag in already_tagged:
      if already_tagged[tag]['skipped']:
        cprint(' * Skipped {n} as {t}'.format(n=tag,t=already_tagged[tag]['tag']),'green')
      else:
        cprint(' * Built {n} as {t}'.format(n=tag,t=already_tagged[tag]['tag']),'green')
  return already_tagged #sum([int(v['hash'],16) for v in already_tagged.values()])
