## @file agentManager.py
#  @brief Agent and %pathfinding manager.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.pathfinding.agentManager
#  @brief Agent and %pathfinding manager.

#-------------------------------------------------------------------------------

from ..logger import Log
from ..application import Application as App
from ..math import Math


#import ogre.renderer.OGRE as ogre

## Agent and %pathfinding manager
class AgentManager (object):
  
  #-----------------------------------------------------------------------------
  
  ## An agent
  class __Agent (object):
    def __init__(self, node, _manager):
      self.__node = node
      self.__rotation = 0
      self.__velocity = 0
      self.__triangle = None
      
      self.__man = _manager
      
      self.__goal = None
      self.__path = None
      
    def getNode(self):
      return self.__node
      
    def getManager(self):
      return self.__man
      
    def update(self, timeElapsed):
      pos = self.__node.getPosition()
      
      
      if self.__goal != None:
        c = 0.001
        if Math.fcmp(self.__goal.x,pos.x,c) and \
            Math.fcmp(self.__goal.z,pos.z,c):
          App().eventManager.hook("agent_atGoal",self)
          self.__goal = None
          self.__path = None
        else:
          target = None
          if len(self.__path) == 0: # this shouldn't happen, but lets be careful
            target = self.__goal
          else:
            target = self.__path[0].getPosition()
            if Math.fcmp(target.x, pos.x,c) and \
                Math.fcmp(target.z, pos.z,c):
              App().eventManager.hook("agent_atPathNode",self)
              self.__path.pop(0)
              target = self.__path[0].getPosition()
            
          mov = (target - pos).normalisedCopy() * (timeElapsed)
          
          self.__node.translate(mov.x,mov.y,mov.z)
          pos = self.__node.getPosition()
          
          
          # move it to the right height on the mesh
          o = self.__man._AgentManager__navigationMesh. \
                        getPointOnMesh(pos,self.__triangle)
          if o != None:
            self.__node.setPosition(o[0])
            if self.__triangle != o[1]:
              Log().debug(o[1])
              oldTri = self.__triangle
              App().eventManager.hook("agent_changeTriangle", [self,o[1]])
              self.__triangle = o[1]
          #self.__node.translate(0,0,self.__velocity * timeElapsed)
    
    def setGoal(self,_goal):
      self.__goal = _goal
      self.__path = self.__man._AgentManager__navigationMesh. \
                        findPath(self.__node.getPosition(), _goal)
    
  #-----------------------------------------------------------------------------
  
  ## Constructor
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
    
    newAgent = self.__Agent(node,self)
    self.__agents.append(newAgent)
    return newAgent
    
  def getAgents (self):
    return list(self.__agents)
    
  def setNavigationMesh (self, navMesh):
    if len(navMesh.getTriangles()) == 0:
      raise Exception ("NavigationMesh is empty")
    self.__navigationMesh = navMesh
    
  def getNavigationMesh(self):
    return self.__navigationMesh
    
  def update(self,timeElapsed):
    for ag in self.__agents:
      ag.update(timeElapsed)