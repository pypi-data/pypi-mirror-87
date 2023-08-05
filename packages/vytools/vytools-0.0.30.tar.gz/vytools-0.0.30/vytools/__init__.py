from vytools.config import ITEMS, CONFIG
from vytools.ui import server
from vytools._actions import build, run, info, _scan

def scan():
  (success, items) = _scan()
  ITEMS.clear()
  ITEMS.update(items)
  CONFIG.set('items',[i for i in items]) # Always write items?
  return success

__version__ = "0.0.30"
