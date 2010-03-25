
from ..logger import Log
from ..application import Application as App


#import ogre.renderer.OGRE as ogre

## 
class AgentManager (object):
  
  ##----------------------------------------------------------------------------
  class __Agent (object):
    def __init__(self, node):
      self.__node = node
      
    def getNode(self):
      return self.__node
    
  ##----------------------------------------------------------------------------
  
  def __init__(self):
    self.__agents = []
    
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
  def close(self):
    Log().info(self.__class__.__name__ + " closed")
    
  def newAgent (self, node, mesh):
    for a in self.__agents:
      if a.getNode() == node:
        return a
    
    newAgent = self.__Agent(node)
    self.__agents.append(newAgent)
    return newAgent
    
  def getAgents (self):
    return list(self.__agents)