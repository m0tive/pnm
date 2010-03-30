## @file singletonApp.py
#  @brief A generalised, simple, singleton %application class containing logging
#    and event managment.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.singletonApp
#  @brief A generalised, simple, singleton %application class containing logging
#    and event managment.

#-------------------------------------------------------------------------------


from logger import Log
from events import EventManager


#-------------------------------------------------------------------------------
## A generalised, simple, singleton %application class containing logging
#    and event managment.
#
#  Singleton pattern taken from post on Stackoverflow.com by "modi" <br />
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#   <br />Accessed: 9th March 2010
class SingletonApp (object):

  ## Instance of the singleton class
  __inst = None
  
  
  #-----------------------------------------------------------------------------
  ## Singleton constructor. Sets up logger and eventManager
  def __new__(cls):
    if not cls.__inst:
      cls.__inst = super(SingletonApp,cls).__new__(cls)
      ## Initialise log and send info message
      Log(level="DEBUG").info("SingletonApp instance created")
      cls.__inst._setup()
    return cls.__inst
    
    
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__():
    Log().info("SingletonApp deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Setup the eventManager and hook "singletonApp_setup"
  def _setup(self):
    ## An instance of events.eventManager.EventManager. Initialised in 
    #   SingletonApp._setup and deleted in SingletonApp.close
    self.eventManager = EventManager()
    Log().debug("SingletonApp setup")
    self.eventManager.hook("singletonApp_setup")
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    del self.eventManager
    Log().info("SingletonApp closed")
    