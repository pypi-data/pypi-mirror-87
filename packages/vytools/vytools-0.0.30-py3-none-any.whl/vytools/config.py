import os, json, logging
from termcolor import cprint
from pathlib import Path
_FOLDER = os.path.dirname(os.path.realpath(__file__))
_CONFIGFILE = os.path.join(_FOLDER,'vyconfig.json')
_FIELDS = ['contexts','items','secrets','jobs','menu']
SEARCHED_REPO_PATHS = []
ITEMS = {}

def get_secrets(path):
  SECRETS = {}
  for root, dirs, files in os.walk(path):
    for sname in files:
      SECRETS[sname] = os.path.join(path,sname)
  return SECRETS

class __CONFIG:
  def __init__(self):
    self._data = {}
    self._secrets = {}
    try:
      self._data = json.loads(Path(_CONFIGFILE).read_text().strip())
      self.__get_secrets()
    except:
      pass
  
  def __write(self):
    with open(_CONFIGFILE,'w') as w:
      w.write(json.dumps(self._data))

  def __get_secrets(self):
    if 'secrets' in self._data and self._data['secrets']:
      self._secrets = get_secrets(self._data['secrets'])

  def set(self,field,value):
    if field in _FIELDS:
      if field == 'contexts':
        contexts = [str(Path(v).resolve()) for v in value.split(',')]
        self._data[field] = [v for v in contexts if os.path.isdir(v)]
      elif field in ['secrets','jobs']:
        self._data[field] = str(Path(value).resolve())
        ign = os.path.join(self._data[field],'.vyignore')
        if not os.path.exists(ign):
          with open(ign,'w'): pass
      else:
        self._data[field] = value
      self.__write()
      if field == 'secrets':
        self.__get_secrets()

  def get(self,field):
    return self._data[field] if self._data and field in self._data else None

  def secrets_cmd(self, secret_list):
    cmd = []
    ok = True
    for secret in secret_list:
      if secret not in self._secrets:
        logging.error('No secret found for id={s}'.format(s=secret))
        secrets_path = self.get('secrets')
        if not secrets_path:
          logging.error('secrets path not specified, specify path with vytools --secrets , (e.g. "vytools --secrets path/to/folder/containing/secrets" info)')
        else:
          logging.error('This secret should be in '+secrets_path)
        ok = False
      else:
        cmd += ['--secret','id='+secret+',src='+self._secrets[secret]]
    return (ok, cmd)

  def info(self):
    cprint('VyTools Configuration & Summary:', attrs=['bold'])
    print('  Configuration saved at: '+_CONFIGFILE)
    print('  Contexts = {s}'.format(s=self.get('contexts')))
    print('  Secrets at {s}'.format(s=self.get('secrets')))
    jobpath = self.get('jobs')
    if jobpath:
      print('  Jobs at {s}'.format(s=jobpath))
    else:
      cprint('  Jobs path not specified, specify path with vytools --jobs , (e.g. "vytools --jobs path/to/folder/for/jobs" info)', attrs=['bold'])
    print('  Items found:')
    items = self.get('items')
    typs = {}
    if items:
      for i in items:
        typ = i.split(':')[0]
        if typ not in typs: typs[typ] = 0
        typs[typ] += 1
    for typ in typs:
      print('    - {n} {t} items'.format(t=typ,n=typs[typ]))

  def job_path(self, relpath=None, create=False):
    job_path = self.get('jobs')
    if not job_path:
      logging.error('No jobs path specified ("vytools info")')
      return None

    if relpath is None: return job_path
    
    job_path_p = Path(job_path)
    pth = os.path.join(job_path, relpath)
    if not os.path.exists(pth):
      if create:
        os.makedirs(pth,exist_ok=True)
      else:
        return None
    if job_path_p not in Path(pth).resolve().parents:
      logging.error('  Failed to get path "{n}". "{p}" is not in job path'.format(n=relpath, p=pth))
      return None
    return pth


CONFIG = __CONFIG()

