
import vytools.utils as utils
import yaml, re, json
import cerberus
import logging

SCHEMA = utils.BASE_SCHEMA.copy()
SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['definition']},
  'element':{
    'type':'list',
    'schema': {
      'type': 'dict',
      'schema': {
        'name': {'type': 'string', 'maxlength': 64},
        'optional': {'type': 'boolean', 'required':False},
        'length': {'type': 'string'},
        'type': {'type': 'string'}
      }
    }
  }
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'definition',
    'depends_on':[],
    'element':[],
    'path':pth
  }
  try:
    with open(pth,'r') as r:
      content = json.loads(r.read())
      item['element'] = content['element']
  except Exception as exc:
    logging.error('Failed to parse definition "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

  if VALIDATE.validate(item):
    items['definition:'+name] = item
  else:
    logging.error('"{n}" at "{p}" failed validation {s}'.format(n=name, p=pth, s=VALIDATE.errors))
    return False
  return True

def find_all(items):
  success = utils.search_all(r'(.+)\.definition\.json', parse, items)
  if success: # process definitions
    for (type_name, item) in items.items():
      if type_name.startswith('definition:'):
        (typ, name) = type_name.split(':',1)
        item['depends_on'] = [] # ['repo:'+item['repo']] if len(item['repo']) > 0 else []
        for e in item['element']:
          if e['type'] in utils.BASE_DATA_TYPES:
            pass
          elif 'definition:'+e['type'] in items:
            item['depends_on'].append('definition:'+e['type'])
          else:
            success = False
            logging.error('definition "{n}" has an invalid element type {t}'.format(n=name, t=e['type']))
  return success
