## @file scripts/application_start.py
#  @brief Script file, see scripts.application_start

## @package scripts.application_start
#  @brief Application start event
#  This is hooked by pnm.application.Application.start before entering the 
#    render loop.
#  <br> No \c data is passed.

#-------------------------------------------------------------------------------

from pnm.application import Application as App
from pnm.pathfinding.navigationMesh import NavigationMesh
from pnm.pathfinding.buildFixedNavMesh import buildFixedNavMesh
from pnm.logger import Log


## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  
  navMeshVisual = App().renderManager.displayMesh("navMesh")
  agentOuterNode = App().renderManager.sceneNode.createChildSceneNode("agentOuterNode")
  agent = App().agentManager.newAgent(agentOuterNode)
  agentEntity, agentNode = App().renderManager.displayMesh("agent", agent.getNode())
  
  agentNode.scale(2,2,2)#4,1.5)
  
  navMesh = NavigationMesh()
  buildFixedNavMesh(navMesh)
  navMesh.buildLinks()
  App().agentManager.setNavigationMesh(navMesh)
  
  import ogre.renderer.OGRE as ogre
  output = navMesh.getPointOnMesh(ogre.Vector3(0,0,0))
  if output != None:
    agent.getNode().setPosition(output[0])
  
  agentNode.pitch(ogre.Math.DegreesToRadians(90))
  agentNode.translate(0,0.4,-0.2)
  
  App().eventManager.hook("agent_atGoal",agent)
  
  return True
