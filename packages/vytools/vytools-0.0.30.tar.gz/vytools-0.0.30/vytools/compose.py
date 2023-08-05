
import vytools.utils as utils
import vytools.stage
from vytools.config import CONFIG
import yaml, re, json, os
import cerberus
import logging
from pathlib import Path

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['compose']},
  'ui':{'type':'string', 'maxlength': 64, 'required': False},
  'subassembly':{'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 64},
        'calibration':{'type': 'dict', 'required':False}
      }
    }
  },
  'artifact':{'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 64},
        'type': {'type': 'string', 'allowed': ['text','json','binary']},
        'source':{'type': 'string', 'maxlength':2048}
      }
    }
  },
  'image':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'search': {'type': 'string', 'maxlength': 64},
        'stage': {'type': 'string', 'maxlength': 64},
        'build_arg':{
          'type':'list',
          'required':False,
          'schema': {
            'type': 'dict',
            'schema': {
              'key': {'type': 'string', 'maxlength': 64},
              'value': {'type': 'string', 'maxlength': 64}
            }
          }
        },
      }
    }
  },
  'calibration':{
    'type':'dict',
    'required':False,
    'schema': {
      'name': {'type': 'string', 'maxlength': 64},
      'definition': {'type': 'string', 'maxlength': 64},
      'volume': {'type': 'string', 'maxlength': 1024}
    }
  }
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items):
  success = True
  item = {
    'name':name,
    'thingtype':'compose',
    'repo':reponame,
    'depends_on':[],
    'artifact':[],
    'subassembly':[],
    'image':[],
    'path':pth
  }

  with open(pth,'r') as r:
    content = r.read()
    for line in content.splitlines():
      m = re.search(r'^#vy(.+)', line, re.I | re.M)
      if m:
        try:
          subitem = json.loads(m.group(1))
        except Exception as exc:
          logging.error('  Failed to parse #vy tag in {n} at {g}. Bad json.'.format(n=pth, g=m.group(1)))
          continue
        for si in subitem:
          if si == 'subassembly':
            item[si].append(subitem[si])
          elif si == 'artifact':
            item[si].append(subitem[si])
          elif si == 'ui':
            item['ui'] = subitem[si]
          elif si == 'image':
            item[si].append(subitem[si])
          elif si == 'calibration':
            if 'definition' in subitem[si]:
              typ = subitem[si]['definition']
              if not (typ in utils.BASE_DATA_TYPES or 'definition:'+typ in items):
                success = False
                logging.error('  Calibration "{s}" in {p} must have a valid type'.format(p=pth, s=subitem))
            else:
              success = False
              logging.error('  Calibration "{s}" in {p} must have a valid type'.format(p=pth, s=subitem))
            item['calibration'] = subitem[si]

  if 'calibration' in item:
    defin = item['calibration'].get('definition','')
    if 'definition:'+defin in items:
      item['depends_on'].append('definition:'+defin)
    else:
      success = False
      logging.error('Calibration in compose "{n}" has an invalid definition {t}'.format(n=name, t=defin))

  if success and VALIDATE.validate(item):
    items['compose:'+name] = item
  elif success:
    logging.error('Compose "{n}" at "{p}" failed validation {s}'.format(n=name, p=pth, s=VALIDATE.errors))
  return success

def build(assembly, build_arg_dict, items, built, build_level):
  type_name = assembly['name']
  item = items[type_name]
  name = item['name']
  label = assembly.get('label', type_name.replace('compose:',''))
  # Build all subassemblies
  composition = {}
  calibration = item.get('calibration',{})
  calvolume = calibration.get('volume',None)
  data = {}
  if 'definition' in calibration:
    data = vytools.object.expand(assembly.get('parent_data',{}),
        calibration['definition'],items,data_mods=assembly.get('data_mods',None))

  for sa in item['subassembly']:
    build_args = build_arg_dict.copy()
    subassembly = sa.copy()
    subassembly['label'] = label + '.'+subassembly['name']
    subassembly['name'] = 'compose:' + subassembly['name']
    subassembly['parent_data'] = data
    subcomps = build(subassembly, build_args, items, built, build_level)
    if subcomps == False:
      return False
    else:
      composition.update(subcomps)

  if build_level == -1:
    with open(item['path'],'r') as r:
      composition[label] = {'compose':yaml.safe_load(r.read()),'i':len(composition)}

  for img in item.get('image',[]):
    image_build_args = {}
    for bai in img.get('build_arg',[]): image_build_args[bai['key']] = bai['value']
    image_build_args.update(build_arg_dict) # Overwrite with top level
    # TODO Overwrite with data
    stage_name = 'stage:'+img['stage']
    stages = [stage_name]
    if not utils.exists(stages, items):
      return False
    tagged = vytools.stage.build(stages, items, image_build_args, built, build_level)
    if tagged == False:
      return False
    elif build_level == -1:
      for sname,service in composition[label]['compose'].get('services',{}).items():
        if 'image' in service and service['image'] == img['search']:
          service['image'] = tagged[stage_name]['tag']
        for volume in service.get('volumes',[]):
          if isinstance(volume,dict) and 'source' in volume and volume['source']==calvolume:
            composition[label]['volume'] = data
            volume['source'] = './'+label+'_cal.json'
  return composition

def find_all(items):
  success = utils.search_all(r'(.+)\.compose\.y[a]*ml', parse, items)
  if success: # process definitions
    for (type_name, item) in items.items():
      if type_name.startswith('compose:'):
        (typ, name) = type_name.split(':',1)
        item['depends_on'] = [] # ['repo:'+item['repo']] if len(item['repo']) > 0 else []
        for e in item['image']:
          item['depends_on'].append('stage:' + e['stage'])
        if 'ui' in item:
          item['depends_on'].append('ui:' + item['ui'])
        for e in item['subassembly']:
          if 'compose:' + e['name'] in items:
            item['depends_on'].append('compose:' + e['name'])
          else:
            success = False
            logging.error('Subassembly in compose "{n}" does not exist compose:{t}'.format(n=name, t=e['name']))

  return success

def artifact_paths(jobpath, compose_name, items):
  artifacts = {}
  def get_artifacts(i,artifacts):
    if i in items:
      for a in items[i]['artifact']:
        pth = CONFIG.job_path(relpath=os.path.join(jobpath,a['source']))
        if pth:
          artifacts[a['name']] = str(pth)
      for sa in items[i]['subassembly']: get_artifacts(sa['name'],artifacts)
  get_artifacts(compose_name,artifacts)
  return artifacts
