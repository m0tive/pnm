## @file application.py
#  @brief The %application class.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.application
#  @brief The %application class.

#-------------------------------------------------------------------------------


from singletonApp import SingletonApp
from logger import Log


#-------------------------------------------------------------------------------
## The %application class.
class Application (SingletonApp):

  #-----------------------------------------------------------------------------
  ## Setup and initialise the application managers.
  #  Once the application is setup the "application_setup" event is hooked
  def _setup(self):
    super(Application,self)._setup()
    
    from .renderer.renderManager import RenderManager
    ## An instance of renderer.renderManager.RenderManager. Initialised in 
    #   Application._setup and deleted in Application.close
    self.renderManager = RenderManager()
    
    from .input.inputManager import InputManager
    ## An instance of input.inputManager.InputManager. Created in 
    #   Application._setup and deleted in Application.close
    self.inputManager = InputManager()
    
    from .pathfinding.agentManager import AgentManager
    ## An instance of pathfinding.agentManager.AgentManager. Initialised in 
    #    Application._setup and deleted in Application.close
    self.agentManager = AgentManager()
    
    Log().debug("Application setup")
    self.eventManager.hook("application_setup")
    
    
  #-----------------------------------------------------------------------------
  ## Start the application.
  #  This runs the renderer setup (creating the window) and then sets the input
  #    manager up to recieve mouse and keyboard events from the render window.
  #    Before these elements run, the "application_preStart" event is hooked;
  #    afterwards (but before starting the render loop) the "application_start"
  #    event is hooked.
  #
  #  This function only exist once the render loop has stopped
  def start(self):
    self.eventManager.hook("application_preStart")
    self.renderManager.setup(restoreConfig=True)
    self.inputManager.setup()
    
    
    self.eventManager.hook("application_start")
    self.renderManager.start()
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    
    self.agentManager.close()
    del self.agentManager
    
    self.inputManager.close()
    del self.inputManager
    
    self.renderManager.close()
    del self.renderManager
    
    Log().info("Application closed")
    
    # close the parent application
    super(Application,self).close()