
from logger import Log
from events import EventManager

## Singleton application class
#
#  Singleton pattern taken from post on Stackoverflow.com by "modi"
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#  Accessed: 9th March 2010
class SingletonApp (object):
  __inst = None
  
  def __new__(cls, **kwargs):
    if not cls.__inst:
      cls.__inst = super(SingletonApp,cls).__new__(cls)
      ## Initialise log and send info message
      Log(level="DEBUG").info("SingletonApp instance created")
      cls.__inst._setup()
    elif kwargs:
      Log().warning("SingletonApp arguments not used after creation")
    return cls.__inst
    
  def __del__():
    Log().info("SingletonApp deleted")
    
  def _setup(self):
    self.eventManager = EventManager()
    Log().debug("SingletonApp setup")
    self.eventManager.hook("singletonApp_setup")
    
  def close(self):
    del self.eventManager
    Log().info("SingletonApp closed")