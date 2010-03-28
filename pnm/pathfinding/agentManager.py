## @file agentManager.py
#  @brief Agent and pathfinding manager
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#-------------------------------------------------------------------------------

from ..logger import Log
from ..application import Application as App


#import ogre.renderer.OGRE as ogre

## Agent and pathfinding manager
class AgentManager (object):
  
  ##----------------------------------------------------------------------------
  
  ## An agent
  class __Agent (object):
    def __init__(self, node):
      self.__node = node
      self.__rotation = 0
      self.__velocity = 1
      self.__triangle = None
      
    def getNode(self):
      return self.__node
      
    def update(self, timeElapsed):
      self.__node.translate(0,0,self.__velocity * timeElapsed)
    
  ##----------------------------------------------------------------------------
  
  def __init__(self):
    self.__agents = []
    self.__navigationMesh = None
    
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
  def close(self):
    Log().info(self.__class__.__name__ + " closed")
    
  def newAgent (self, node):
    for a in self.__agents:
      if a.getNode() == node:
        return a
    
    newAgent = self.__Agent(node)
    self.__agents.append(newAgent)
    return newAgent
    
  def getAgents (self):
    return list(self.__agents)
    
  def setNavigationMesh (self, navMesh):
    if len(navMesh.getTriangles()) == 0:
      raise Exception ("NavigationMesh is empty")
    self.__navigationMesh = navMesh
    
  def update(self,timeElapsed):
    for ag in self.__agents:
      ag.update(timeElapsed)