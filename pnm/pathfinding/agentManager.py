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


#-------------------------------------------------------------------------------
## Agent and %pathfinding manager
class AgentManager (object):
  
  #---------------------------------------------------| Start Nested Classes |--
  
  #-----------------------------------------------------------------------------
  ## An agent
  class __Agent (object):
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param _node - OGRE sceneNode to attach the agent to
    #  @param _manager - AgentManager containing this agent
    def __init__(self, _node, _manager):
      ## The OGRE SceneNode controlled by the agent
      self.__node = _node
      ## The AgentManager this agent is within
      self.__man = _manager
      
      ## The navigationMesh.NavigationMesh.__Triangle this Agent is within
      self.__triangle = None
      ## The Agents goal location (an OGRE Vector3). If \c None, then the Agent 
      #    is stationary
      self.__goal = None
      ## The current path to the __goal, stored as a list of 
      #    navigationMesh.NavigationMesh.__Node
      #  @see navigationMesh.NavigationMesh.findPath
      self.__path = None
      
      
    #---------------------------------------------------------------------------
    ## Safe shutdown and dereference of variables.
    #  This stops circular references stopping the garbage collection
    def close(self):
      self.__node = None
      self.__man = None
      self.__triangle = None
      self.__goal = None
      self.__path = None
      
    
    #---------------------------------------------------------------------------
    ## Get SceneNode the agent is attached to
    #  @return The agent's SceneNode
    def getNode(self):
      return self.__node
      
      
    #---------------------------------------------------------------------------
    ## Get the AgentManager this agent is within
    #  @return The AgentManager this is within
    def getManager(self):
      return self.__man
    
    
    #---------------------------------------------------------------------------
    ## Set the agent's goal location and calculate a path to it.
    #  This calls navigationMesh.NavigationMesh.findPath to calculate a path to
    #    the given goal location
    #  @param _goal - A OGRE Vector3 describing the goal location
    def setGoal(self,_goal):
      self.__goal = _goal
      self.__path = self.__man._AgentManager__navigationMesh. \
                        findPath(self.__node.getPosition(), _goal)
      
      
    #---------------------------------------------------------------------------
    ## Update the agents position towards it's current goal (if one is set)
    #  @param timeElapsed - The time since last updated
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
          
          # Turns out we don't need to do this... each path vector is parrallel
          #   with the polygon we're on.
          '''# move it to the right height on the mesh
          o = self.__man._AgentManager__navigationMesh. \
                        getPointOnMesh(pos,self.__triangle)
          if o != None:
            self.__node.setPosition(o[0])
            if self.__triangle != o[1]:
              Log().debug(o[1])
              oldTri = self.__triangle
              App().eventManager.hook("agent_changeTriangle", [self,o[1]])
              self.__triangle = o[1]'''
    
  #-----------------------------------------------------| End Nested Classes |--
  
  
  # AgentManager continued...
  
  #-----------------------------------------------------------------------------
  ## Constructor
  def __init__(self):
    ## A list of the agents managed by this class
    self.__agents = []
    ## The navmesh associated with this set of agents
    self.__navigationMesh = None
    
   
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    for agent in self.__agents:
      agent.close()
    
    if self.__navigationMesh != None:
      self.__navigationMesh.close()
      
    del self.__agents
    del self.__navigationMesh
    
    Log().info(self.__class__.__name__ + " closed")
    
    
  #-----------------------------------------------------------------------------
  ## Create a new agent.
  #  @note If an agent already exists on the given node, no new agent is created
  #    and the existing node is returned
  #  @param _node - OGRE SceneNode to attach the agent to
  #  @return A new (or similar) agent
  def newAgent (self, _node):
    for a in self.__agents:
      if a.getNode() == _node:
        return a
    
    newAgent = self.__Agent(_node,self)
    self.__agents.append(newAgent)
    return newAgent
    
    
  #-----------------------------------------------------------------------------
  ## Get a copy of the list of agents
  #  @return A copy of the agent list
  def getAgents (self):
    return list(self.__agents)
    
    
  #-----------------------------------------------------------------------------
  ## Set the navigation mesh.
  #  @note This must be done before giving agents goals
  #  @return The navigationMesh.NavigationMesh to be used
  def setNavigationMesh (self, navMesh):
    if len(navMesh.getTriangles()) == 0:
      raise Exception ("NavigationMesh is empty")
    self.__navigationMesh = navMesh
    
    
  #-----------------------------------------------------------------------------
  ## Get the current naviation mesh
  #  @return The navigationMesh.NavigationMesh in use
  def getNavigationMesh(self):
    return self.__navigationMesh
    
    
  #-----------------------------------------------------------------------------
  ## Update the agents
  #  @see __Agent.update
  #  @param timeElapsed - The time since last updated
  def update(self,timeElapsed):
    for ag in self.__agents:
      ag.update(timeElapsed)
      