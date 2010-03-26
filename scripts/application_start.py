from pnm.application import Application as App
from pnm.pathfinding.navigationMesh import NavigationMesh
from pnm.pathfinding.buildFixedNavMesh import buildFixedNavMesh
from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  
  navMeshVisual = App().renderManager.displayMesh("navMesh")
  agentOuterNode = App().renderManager.sceneNode.createChildSceneNode("agentOuterNode")
  agent = App().agentManager.newAgent(agentOuterNode)
  agentEntity, agentNode = App().renderManager.displayMesh("agent", agent.getNode())
  
  agentNode.scale(2,4,1.5)
  
  navMesh = NavigationMesh()
  buildFixedNavMesh(navMesh)
  App().agentManager.setNavigationMesh(navMesh)
  
  firstNode = navMesh.getNode(0)
  Log().debug(firstNode)
  Log().debug(firstNode.getPosition())
  agent.getNode().setPosition(firstNode.getPosition())
  Log().debug(agent.getNode().getPosition())
  
  Log().debug(navMesh.getTriangle(1).getNormal())
  
  return True
