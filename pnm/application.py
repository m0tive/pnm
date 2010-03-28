## @file application.py
#  @brief The application class.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#-------------------------------------------------------------------------------

from singletonApp import SingletonApp
from logger import Log


## Application class
class Application (SingletonApp):
  def _setup(self):
    super(Application,self)._setup()
    
    from .renderer.renderManager import RenderManager
    self.renderManager = RenderManager()
    
    from .input.inputManager import InputManager
    self.inputManager = InputManager()
    
    from .pathfinding.agentManager import AgentManager
    self.agentManager = AgentManager()
    
    Log().debug("Application setup")
    self.eventManager.hook("application_setup")
    
  def start(self):
    self.eventManager.hook("application_preStart")
    self.renderManager.setup(restoreConfig=True)
    self.inputManager.setup()
    
    
    self.eventManager.hook("application_start")
    self.renderManager.start()
    
    
  def close(self):
    
    self.agentManager.close()
    del self.agentManager
    
    self.inputManager.close()
    del self.inputManager
    
    self.renderManager.close()
    del self.renderManager
    
    Log().info("Application closed")
    
    ## close the parent application
    super(Application,self).close()