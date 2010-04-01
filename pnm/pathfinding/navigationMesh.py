## @file navigationMesh.py
#  @brief A navigation mesh used for %pathfinding
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.pathfinding.navigationMesh
#  @brief A navigation mesh used for %pathfinding

#-------------------------------------------------------------------------------


from ..logger import Log
from ..application import Application as App
from ..math import Math

import ogre.renderer.OGRE as ogre


#-------------------------------------------------------------------------------
## A navigation mesh used for %pathfinding
class NavigationMesh (object):
  
  #---------------------------------------------------| Start Nested Classes |--
    
  #-----------------------------------------------------------------------------
  ## A path node
  class __Node ():
  
    ## The static id iterator.
    #  @see __Node.__id
    __idIt = 1
    
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param pos - The node's position as an OGRE Vector3.
    def __init__(self,pos):
      ## The unique id.
      self.__id = NavigationMesh._NavigationMesh__Node.__idIt
      ## The position.
      self.__position = pos
      ## The __Triangles this node is within.
      self.__triangles = []
      ## The other __Node this node is linked to.
      self.__neighbours = []
      
      ## Dictionary of %pathfinding cost to move to each neighbour.
      self.__astar_neighbourCosts = {}
      ## The cost so-far to move to this node.
      #  This is used during %pathfinding.
      self.__astar_cost = 0
      ## The node's current %pathfinding rank.
      #  This is used during %pathfinding.
      self.__astar_rank = 0
      ## The node's path parent.
      #  This is used during %pathfinding.
      self.__astar_parent = None
      
      # update the id counter
      NavigationMesh._NavigationMesh__Node.__idIt += 1
      
      
    #---------------------------------------------------------------------------
    ## Safe shutdown and dereference of variables.
    #  This stops circular references stopping the garbage collection
    def close(self):
      del self.__position
      del self.__triangles
      del self.__neighbours
      del self.__astar_neighbourCosts
      
      
    #---------------------------------------------------------------------------
    ## Get the node's position.
    #  @return OGRE Vector3 of the node's position
    def getPosition(self):
      return ogre.Vector3(self.__position.x,self.__position.y,self.__position.z)
      
      
    #---------------------------------------------------------------------------
    ## Get the node's id
    #  @return The node's id
    def getId(self):
      return self.__id
      
      
    #---------------------------------------------------------------------------
    ## Get the triangles this node is within
    #  @return A list of __Triangle
    def getTriangles(self):
      return list(self.__triangles)
      
      
    #---------------------------------------------------------------------------
    ## Get the neighbours this node is linked with.
    #  @return A list of __Node
    def getNeighbours(self):
      return list(self.__neighbours)
      
      
    #---------------------------------------------------------------------------
    ## Add multiple neighbour nodes.
    #  This adds a list of neighbours, checking they're not already added and 
    #    add this node to the given neighbours
    #  @param L - A list of neighbours
    #  @param _cModifier - The %pathfinding cost modifier to be applied
    def __addNeighbours(self,L,_cModifier = 1):
      for n in L:
        if n not in self.__neighbours and n != self:
          if n == None:
            raise Exception ("n == None")
          #Log().debug("node %d adding neighbour %d" % (self.__id, n._Node__id))
          cost = self.__position.distance(n._Node__position)
          
          ## @todo Take into account change in height when saving cost.
          
          self.__neighbours.append(n)
          self.__astar_neighbourCosts[n] = cost * _cModifier
          n._Node__neighbours.append(self)
          n._Node__astar_neighbourCosts[self] = cost * _cModifier
          
          
    #---------------------------------------------------------------------------
    ## Remove a list of neighbours from this node's links.
    #  This unlinks the given neighbours from this node and unlinks this node 
    #    from the given neighbours.
    #  @param L - A list of __Node which are neighbours of this node.
    def __removeNeighbours(self,L):
      for n in L:
        if n in self.__neighbours and n != self:
          if n == None:
            raise Exception ("n == None")
          self.__neighbours.remove(n)
          del self.__astar_neighbourCosts[n]
          n.__neighbours.remove(self)
          del n._Node__astar_neighbourCosts[self]
      
      
    #---------------------------------------------------------------------------
    ## Convert to a string (for debugging).
    #  @return A string containing the node's position.
    def __str__ (self):
      return "Node[%f, %f, %f]" % \
        (self.__position.x, self.__position.y, self.__position.z)
  
  
  
  #-----------------------------------------------------------------------------
  ## A collection of three __Node.
  class __Triangle ():
  
    #---------------------------------------------------------------------------
    ## Constructor.
    #  @param v1 - First __Node.
    #  @param v2 - Second __Node.
    #  @param v3 - Third __Node.
    def __init__(self,v1,v2,v3):
    
      ## NavigationMesh this triangle is within.
      #  This is set by NavigationMesh.
      self.__mesh = None
      ## Flag to indicate if the triangle has already been tested.
      self._tested = False
      ## The normal to this triangle.
      #  @see __Triangle.getNormal
      self.__normal = None
      self.__neighbours = []
      
      v1._Node__triangles.append(self)
      v2._Node__triangles.append(self)
      v3._Node__triangles.append(self)
      
      ## A list of the %pathfinding __Node within this triangle.
      self.__nodes = [v1,v2,v3]
      
      Log().debug("building %s" % self)
      
      
    #---------------------------------------------------------------------------
    ## Safe shutdown and dereference of variables.
    #  This stops circular references stopping the garbage collection
    def close(self):
      del self.__neighbours
      del self.__nodes
      del self.__mesh
      
      #Log().debug(self.__class__.__name__ + " closed")
      
      
    #---------------------------------------------------------------------------
    ## Get the midpoint between two OGRE Vector3.
    #  @return OGRE Vector3 containing the midpoint.
    def getMidpoint(self,pt1,pt2):
      return pt1 + (pt2 - pt1)*0.5
      
      
    #---------------------------------------------------------------------------
    ## Get a reference to the NavigationMesh this triangle is part of.
    #  @return The NavigationMesh.
    def getMesh(self):
      return self.__mesh
      
      
    #---------------------------------------------------------------------------
    ## Add a neighbour triangle.
    #  @param triangle - The __Triangle to be linked with.
    #  @return True if successful.
    def addNeighbour (self,triangle):
      if len(self.__neighbours) == 3:
        return False
      self.__neighbours.append(triangle)
      if not triangle.isNeighbour(self):
        triangle.addNeighbour(self)
      return True
      
      
    #---------------------------------------------------------------------------
    ## Test if a triangle is neighbouring this triangle.
    #  @param triangle - The __Triangle to test
    #  @return True if the triangles are neighbours
    def isNeighbour (self,triangle):
      return (triangle in self.__neighbours)
      
      
    #---------------------------------------------------------------------------
    ## Get the triangles neighbours
    #  @return A copy of the list of neighbouring __Triangle
    def getNeighbours (self):
      return list(self.__neighbours)
      
      
    #---------------------------------------------------------------------------
    ## Get %pathfinding __Node in this triangle
    #  @return A copy of the list of contained __Node
    def getVertices (self):
      return list(self.__nodes)
      
    #---------------------------------------------------------------------------
    ## Get the position of a specific %pathfinding __Node
    #  @param _id - The id of the node
    #  @return The position of the node as an OGRE.Vector3
    def getVertexPosition(self, _id):
      return self.__nodes[_id].getPosition()
      
      
    #---------------------------------------------------------------------------
    ## Process the triangles three nodes, add midpoints and link them together.
    def buildLinks(self):
      v1 = self.__nodes[0]
      v2 = self.__nodes[1]
      v3 = self.__nodes[2]
      
      v1tris = len(v1.getTriangles())
      v2tris = len(v2.getTriangles())
      v3tris = len(v3.getTriangles())
      
      v1pos = v1.getPosition()
      v2pos = v2.getPosition()
      v3pos = v3.getPosition()
      
      m12 = None
      m23 = None
      m31 = None
      
      if v1tris != 1 and v2tris != 1:
        m = v1pos + (v2pos - v1pos)*0.5
        m12 = self.__mesh._NavigationMesh__newNode(m.x, m.y, m.z)
        self.__nodes.append(m12)
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v1._Node__id, v2._Node__id, m12._Node__id, m.x, m.y, m.z))
        m12._Node__addNeighbours([v1,v2],0.9)
      else:
        v1._Node__addNeighbours([v2])
        
      if v2tris != 1 and v3tris != 1:
        m = v2pos + (v3pos - v2pos)*0.5
        m23 = self.__mesh._NavigationMesh__newNode(m.x, m.y, m.z)
        self.__nodes.append(m23)
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v2._Node__id, v3._Node__id, m23._Node__id, m.x, m.y, m.z))
        m23._Node__addNeighbours([v3,v2],0.9)
        if m12 != None:
          m23._Node__addNeighbours([m12],0.8)
      else:
        v2._Node__addNeighbours([v3])
        
      if v3tris != 1 and v1tris != 1:
        m = v3pos + (v1pos - v3pos)*0.5
        m31 = self.__mesh._NavigationMesh__newNode(m.x, m.y, m.z)
        self.__nodes.append(m31)
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v3._Node__id, v1._Node__id, m31._Node__id, m.x, m.y, m.z))
        m31._Node__addNeighbours([v3,v1],0.9)
        if m12 != None:
          m31._Node__addNeighbours([m12],0.8)
        if m23 != None:
          m31._Node__addNeighbours([m23],0.8)
      else:
        v3._Node__addNeighbours([v1])
        
      
    #---------------------------------------------------------------------------
    ## Get the normal to the triangle.
    #  This is calculated once, when getNormal is first run
    #  @return The normal as an OGRE Vector3
    def getNormal(self):
      if self.__normal == None:
        p1 = self.__nodes[0]._Node__position
        p2 = self.__nodes[1]._Node__position
        p3 = self.__nodes[2]._Node__position
        self.__normal = ((p2 - p1).crossProduct(p3 - p1)).normalisedCopy()
      return self.__normal
      
      
    #---------------------------------------------------------------------------
    ## A utility function to get the centre point on the triangle
    #  @return The centre as an OGRE Vector3
    def getCentre(self):
      div3 = 1.0/3.0
      cX = (self.__nodes[0]._Node__position.x + 
            self.__nodes[1]._Node__position.x + 
            self.__nodes[2]._Node__position.x) * div3
      cY = (self.__nodes[0]._Node__position.y + 
            self.__nodes[1]._Node__position.y + 
            self.__nodes[2]._Node__position.y) * div3
      cZ = (self.__nodes[0]._Node__position.z + 
            self.__nodes[1]._Node__position.z + 
            self.__nodes[2]._Node__position.z) * div3
      return ogre.Vector3(cX, cY, cZ)
      
      
    #---------------------------------------------------------------------------
    ## Convert to a string (for debugging).
    #  @return A string containing the first three nodes' id.
    def __str__(self):
      return "Triangle[%d, %d, %d]" % (self.__nodes[0].getId(), 
          self.__nodes[1].getId(), self.__nodes[2].getId())
  
  #-----------------------------------------------------| End Nested Classes |--
  
  # NavigationMesh continued...
  
  #-----------------------------------------------------------------------------
  ## Constructor
  def __init__(self):
    ## The OGRE mesh to generate the navigation mesh from
    self.__ogreMesh = None
    ## A list of all the __Node in the navigation mesh
    self.__nodes = []
    ## A list of all the __Triangle in the navigation mesh
    self.__triangles = []
    
    
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    for t in self.__triangles:
      t.close()
    for n in self.__nodes:
      n.close()
    
    Log().info(self.__class__.__name__ + " closed")
    
    
  #-----------------------------------------------------------------------------
  ## Create a new %pathfinding node.
  #  If the given location already has a node, that node will be returned 
  #    instead.
  #  @param x - The x positon of the node
  #  @param y - The y positon of the node
  #  @param z - The z positon of the node
  #  @return The new __Node
  def __newNode (self,x,y,z):
    for vertex in self.__nodes:
      p = vertex._Node__position
      if Math.fcmp(p.x,x) and Math.fcmp(p.y,y) and Math.fcmp(p.z,z):
        return vertex
    # else create a new vertex...
    newNode = self.__Node(ogre.Vector3(x,y,z))
    self.__nodes.append(newNode)
    return newNode
    
    
  #-----------------------------------------------------------------------------
  ## Create a new triangle from thee nodes.
  #  If a triangle with all three nodes already exists, that triangle is 
  #    returned instead.
  #  @param v1 - First __Node.
  #  @param v2 - Second __Node.
  #  @param v3 - Third __Node.
  #  @return The new __Triangle
  def __newTriangle (self,v1,v2,v3):
    
    neighbours = []
    
    for tri in self.__triangles:
      matches = 0
      for vertex in tri._Triangle__nodes:
        if v1 == vertex or v2 == vertex or v3 == vertex:
          matches += 1
      if matches == 3:
        return tri
      
      if matches == 2:
        neighbours.append(tri)
      
    newTriangle = self.__Triangle(v1,v2,v3)
    for tri in neighbours:
      if not newTriangle.addNeighbour(tri):
        raise Exception ("adding neighbouts failed")
    newTriangle._Triangle__mesh = self
    self.__triangles.append(newTriangle)
    return newTriangle
    
    
  #-----------------------------------------------------------------------------
  ## Build a triangle using node ids.
  #  This is the primary method of creating new triangles.
  #  @param id1 - first node id
  #  @param id2 - second node id
  #  @param id3 - third node id
  #  @return The new __Triangle
  def _buildTriangle(self,id1,id2,id3):
    size = len(self.__nodes)
    if id1 > size or id2 > size or id3 > size:
      raise Exception ("vertex id out of range")
    return self.__newTriangle(self.__nodes[id1-1], self.__nodes[id2-1], self.__nodes[id3-1])
    
    
  #-----------------------------------------------------------------------------
  ## Build all the __Triangle links.
  #  @see __Triangle.buildLinks
  def buildLinks(self):
    for t in self.__triangles:
      t.buildLinks()
      
      
  #-----------------------------------------------------------------------------
  ## Get a %pathfinding node by id
  #  @param nid - node's id
  #  @return The __Node
  def getNode(self, nid):
    return self.__nodes[nid]
    
     
  #-----------------------------------------------------------------------------
  ## Get all the %pathfinding nodes
  #  @return A copy of the list of __Node
  def getNodes(self):
    return list(self.__nodes)
    
    
  #-----------------------------------------------------------------------------
  ## Get a triangle by id
  #  @param tid - triangle's id
  #  @return The __Triangle
  def getTriangle(self, tid):
    return self.__triangles[tid]
    
     
  #-----------------------------------------------------------------------------
  ## Get all the triangles in the navigation mesh
  #  @return A copy of the list of __Triangle
  def getTriangles(self):
    return list(self.__triangles)
    
  
  def __resetTraingleTest(self):
    for tri in self.__triangles:
      tri._tested = False
    
    
  #-----------------------------------------------------------------------------
  ## Test if a point is on the navigation mesh in 2D x-z plane, if so return the 
  #    point on the mesh's surface
  #  @param _point - The OGRE Vector3 point to test.
  #  @param _firstTri - The first triangle to test. (default, the first triangle)
  #  @return The position on the mesh as a OGRE Vector3 or \c None
  def getPointOnMesh(self, _point, _firstTri=None):
      
    if not _firstTri:
      _firstTri = self.__triangles[0]
      
    openT = [_firstTri]
    closedT = []
    
    p2d = ogre.Vector2(_point.x, _point.z)
    it = 0
    while len(openT) != 0:
      current = openT.pop(0)
      
      n = current.getVertices()
      v = [n[0].getPosition(), n[1].getPosition(), n[2].getPosition()]
      v2d = [ogre.Vector2(v[0].x, v[0].z),
             ogre.Vector2(v[1].x, v[1].z),
             ogre.Vector2(v[2].x, v[2].z)]
      output = Math.getPointIn2dTriangle(p2d, v2d[0], v2d[1], v2d[2])
      if output != False: # point within triangle volume
        # calculate y coordinate
        vect = ogre.Vector3(_point.x, _point.y + 1, _point.z)
        r = Math.getLinePlaneIntersection(_point, vect, current.getNormal(), v[0])
        return r, current
      else:
        closedT.append(current)
        for tri in current.getNeighbours():
          if (tri not in openT) and (tri not in closedT):
            openT.append(tri)
      it += 1
      #Log().debug("trying harder %d: open - %d, closed - %d" % (it,len(openT), len(closedT)))
    return None
    
  #-----------------------------------------------------------------------------
  ## Find a path between two points on the mesh.
  #  @param _start - Starting location as an OGRE Vector3.
  #  @param _goal - End location as an OGRE Vector3.
  #  @return None, if no path was found, or a list of OGRE Vector3 (including 
  #    start and end) describing the path.
  def findPath(self,_start,_goal):
    # test start point and goal point are in triangles,
    oStart = self.getPointOnMesh(_start)
    if oStart == None:
      return None
    Log().info("Find path from: " + str(oStart[0]))
    # find the goal position, use the start triangle as the search start...
    oGoal = self.getPointOnMesh(_goal, oStart[1])
    if oGoal == None:
      return None
    Log().info("... to: " + str(oGoal[0]))
    
    # Create start and end node, linking them with all the nodes in their 
    # respective triangle
    nStart = self.__newNode(oStart[0].x,oStart[0].y,oStart[0].z)
    oStart[1]._Triangle__nodes.append(nStart)
    nStart._Node__addNeighbours(oStart[1].getVertices())
    
    nGoal = self.__newNode(oGoal[0].x,oGoal[0].y,oGoal[0].z)
    oGoal[1]._Triangle__nodes.append(nGoal)
    nGoal._Node__addNeighbours(oGoal[1].getVertices())
    
    # Calculate the path using A*
    path = self.__astar_calculatePath(nStart, nGoal)
    
    Log().info("Found path; length %d:" % len(path))
    for n in path:
      Log().info("   %s" % n.getPosition())
    
    # Delete start and end node
    # @todo delete start and end!
    oStart[1]._Triangle__nodes.remove(nStart)
    nStart._Node__removeNeighbours(oStart[1].getVertices())
    oGoal[1]._Triangle__nodes.remove(nGoal)
    nGoal._Node__removeNeighbours(oGoal[1].getVertices())
    
    self.__nodes.remove(nStart)
    self.__nodes.remove(nGoal)
    
    del nStart._Node__triangles
    del nGoal._Node__triangles
    
    # Don't fully delete nStart and nGoal as we'll need them in the path. Once 
    # the path has been finished with, the garbage collector will clean up after
    # us :)
    
    return path
    
  #-----------------------------------------------------------------------------
  ## Using A*, calculate the path between two nodes.
  #  @param _start - The start __Node
  #  @param _goal - The end __Node
  #  @return None, if no path was found, or a list of __Node (including 
  #    start and end) describing the path.
  #  @todo change \c open to a proper priority ranked list (or sort it 
  #    occationally)
  def __astar_calculatePath(self, _start, _goal):
    solved = False
    
    _start._Node__astar_cost = 0
    open = [_start]
    closed = []
    
    while (1):
      if len(open) == 0:
        return None
      
      current = self.__astar_popLowestRank(open)
      if current == _goal:
        break
      
      closed.append(current)
      for neighbour in current.getNeighbours():
        cost = current._Node__astar_cost + \
            self.__astar_movementcost(current,neighbour)
        if (neighbour in open) and (cost < neighbour._Node__astar_cost):
          # remove neighbour from OPEN, because new path is better
          open.remove(neighbour)
        if (neighbour in closed) and (cost < neighbour._Node__astar_cost):
          #remove neighbour from CLOSED
          closed.remove(neighbour)
        if (neighbour not in open) and (neighbour not in closed):
          neighbour._Node__astar_cost = cost
          open.append(neighbour)
          neighbour._Node__astar_rank = neighbour._Node__astar_cost + \
              self.__astar_heuristic(neighbour,_goal)
          neighbour._Node__astar_parent = current
    
    
    path = self.__astar_reconstructPath(_goal, [])
    return path
    
    
  #-----------------------------------------------------------------------------
  ## Pop the lowest rank off the given open list
  #  @param _openList - A list of __Node to pop from
  #  @return The lowest ranking __Node in the list
  def __astar_popLowestRank(self,_openList):
    low = 0
    if len(_openList) != 1: # we'll just let it crash if an empty list is passed
      for i in range(1,len(_openList)):
        if _openList[i]._Node__astar_rank < _openList[low]._Node__astar_rank:
          low = i
    return _openList.pop(low)
    
    
  #-----------------------------------------------------------------------------
  ## Calculte the heuristic function for a given node.
  #  @param _node - The __Node to calculate it for.
  #  @param _goal - The goal __Node
  #  @return A float value
  def __astar_heuristic(self, _node, _goal):
    return _node._Node__position.distance(_goal._Node__position)
    
    
  #-----------------------------------------------------------------------------
  ## Get the movement cost between two nodes.
  #  @param _nodeA - The current __Node.
  #  @param _nodeB - The __Node to move to.
  #  @return The movement cost.
  def __astar_movementcost(self, _nodeA, _nodeB):
    return _nodeA._Node__astar_neighbourCosts[_nodeB]
    
    
  #-----------------------------------------------------------------------------
  ## Trace the parents from a node to reconstruct the path to it.
  #  @note This is a recursive function.
  #  @param _node - __Node to get path to
  #  @param io_path - A list to construct the path in
  #  @return The path as a list of OGRE Vector3, with the start at index 0
  def __astar_reconstructPath(self, _node, io_path):
    io_path.insert(0,_node)
    if _node._Node__astar_parent == None:
      return io_path
    return self.__astar_reconstructPath(_node._Node__astar_parent, io_path)
    
    

  ''' Failed code to load mesh data from ogre hardware buffers
  #-----------------------------------------------------------------------------
  def loadMesh(self,meshName):
    del self.__ogreMesh
    
    
    rmIt = ogre.ResourceGroupManager.getSingleton().getResourceManagerIterator()
    resourceManager = rmIt.getNext()
    while resourceManager.__class__.__name__ != "MeshManager":
      resourceManager = rmIt.getNext()
    
    self.__ogreMesh = resourceManager.getByName(meshName)
    if self.__ogreMesh == None:
      return False
    
    if self.__ogreMesh.sharedNodeData:
      raise Exception ("has shared vertices... I did not plan for this :S")
    
    
    subMeshIt = self.__ogreMesh.getSubMeshIterator()
    for subM in subMeshIt:
      vertData = subM.vertexData
      #Log().debug(subM.vertexData.vertexStart)
      posElement = vertData.vertexDeclaration.findElementBySemantic(ogre.VES_POSITION)
      vbuffer = vertData.vertexBufferBinding.getBuffer(posElement.getSource())
      vertex = vbuffer.lock(ogre.HardwareBuffer.HBL_READ_ONLY)
      
      blah = None
      
      Log().debug(dir(posElement))
      Log().debug(posElement.getBaseType(ogre.VET_FLOAT3))
      Log().debug(dir(posElement))
      help(posElement.getBestColourNodeElementType)
      
    
    edgeList = self.__ogreMesh.getEdgeList()
    for triangle in edgeList.triangles:
      pass #Log().debug(triangle)
    
    '''
    
    
    
