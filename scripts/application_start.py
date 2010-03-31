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
  output = navMesh.getPointOnMesh(ogre.Vector3(-2, 0, 6.5))
  if output != None:
    agent.getNode().setPosition(output[0])
    
  #navMesh.getTriangle(1).getCentre()
  agent.setGoal(navMesh.getTriangle(2).getCentre())
  
  
  # start test code ------------------------------------------------------------
  
  firstNode = navMesh.getNode(0)
  Log().debug(firstNode)
  Log().debug(firstNode.getPosition())
  #agent.getNode().setPosition(firstNode.getPosition())
  Log().debug(agent.getNode().getPosition())
  
  tri = navMesh.getTriangle(1)
  Log().debug(tri)
  Log().debug(tri.getNormal())
  
  import ogre.renderer.OGRE as ogre
  from pnm.math import Math
  
  point2d = ogre.Vector2(-2, 6.5) # point in first triangle
  point3d = ogre.Vector3(-2, 0, 6.5) # point in first triangle
  tri0 = tri.getVertexPosition(0)
  tri02d = ogre.Vector2(tri0.x, tri0.z)
  tri1 = tri.getVertexPosition(1)
  tri12d = ogre.Vector2(tri1.x, tri1.z)
  tri2 = tri.getVertexPosition(2)
  tri22d = ogre.Vector2(tri2.x, tri2.z)
  Log().debug((tri0.x, tri0.y, tri0.z))
  Log().debug((tri1.x, tri1.y, tri1.z))
  Log().debug((tri2.x, tri2.y, tri2.z))
  
  #output = Math.getPointIn2dTriangle(point2d, tri02d, tri12d, tri22d)
  output = navMesh.getPointOnMesh(point3d)
  #if output != None:
  #  agent.getNode().setPosition(output[0])
  
  # end test code --------------------------------------------------------------
  
  return True
