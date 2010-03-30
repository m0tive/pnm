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

## A navigation mesh used for %pathfinding
class NavigationMesh (object):
 
  #class __Node ():
    #def __init__(self,p1,p2):
      #pass
    
  #-----------------------------------------------------------------------------
  
  ## A path node
  #
  class __Node ():
    __idIt = 1
    
    def __init__(self,pos):
      self.__id = NavigationMesh._NavigationMesh__Node.__idIt
      NavigationMesh._NavigationMesh__Node.__idIt += 1
      self.__position = pos
      self.__triangles = []
      self.__neighbours = []
      self.__astar_neighbourCosts = {}
    
    #def __del__(self):
      #Log().info(self.__class__.__name__ + " deleted")
      
    def close(self):
      del self.__position
      del self.__triangles
      del self.__neighbours
      del self.__neighbourCosts
      
      #Log().debug(self.__class__.__name__ + " closed")
      
    def getPosition(self):
      return ogre.Vector3(self.__position.x, self.__position.y, self.__position.z)
      
    def getId(self):
      return self.__id
      
    def getTriangles(self):
      return list(self.__triangles)
      
    def getNeighbours(self):
      return list(self.__neighbours)
      
    def __addNeighbours(self,L):
      for n in L:
        if n not in self.__neighbours and n != self:
          if n == None:
            raise Exception ("n == None")
          #Log().debug("node %d adding neighbour %d" % (self.__id, n._Node__id))
          cost = self.__position.distance(n._Node__position)
          
          ## @todo Take into account change in height when saving cost
          
          self.__neighbours.append(n)
          self.__neighbourCosts[n] = cost
          n._Node__neighbours.append(self)
          n._Node__neighbourCosts[self] = cost
      
    def __str__ (self):
      return "Node[%f, %f, %f]" % \
        (self.__position.x, self.__position.y, self.__position.z)
  
  #-----------------------------------------------------------------------------
  
  ## A collection of three __Node
  class __Triangle ():
    def __init__(self,v1,v2,v3):
      self.__mesh = None
      
      self._tested = False
      
      self.__normal = None
      
      v1._Node__triangles.append(self)
      v2._Node__triangles.append(self)
      v3._Node__triangles.append(self)
      
      self.__nodes = [v1,v2,v3]
      
      self.__neighbours = []
      Log().debug("building %s" % self)
    
    #def __del__(self):
      #Log().info(self.__class__.__name__ + " deleted")
      
    def close(self):
      del self.__neighbours
      del self.__nodes
      del self.__mesh
      
      #Log().debug(self.__class__.__name__ + " closed")
      
    def getMidpoint(self,pt1,pt2):
      return pt1 + (pt2 - pt1)*0.5
      
    def getMesh(self):
      return self.__mesh
      
    def addNeighbour (self,triangle):
      if len(self.__neighbours) == 3:
        return False
      self.__neighbours.append(triangle)
      if not triangle.isNeighbour(self):
        triangle.addNeighbour(self)
      return True
      
    def isNeighbour (self,triangle):
      return (triangle in self.__neighbours)
      
    def getNeighbours (self):
      return list(self.__neighbours)
      
    def getVertices (self):
      return list(self.__nodes)
      
    def getVertexPosition(self, _id):
      return self.__nodes[_id].getPosition()
      
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
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v1._Node__id, v2._Node__id, m12._Node__id, m.x, m.y, m.z))
        v1._Node__addNeighbours([m12])
        v2._Node__addNeighbours([m12])
      else:
        v1._Node__addNeighbours([v2])
        
      if v2tris != 1 and v3tris != 1:
        m = v2pos + (v3pos - v2pos)*0.5
        m23 = self.__mesh._NavigationMesh__newNode(m.x, m.y, m.z)
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v2._Node__id, v3._Node__id, m23._Node__id, m.x, m.y, m.z))
        v2._Node__addNeighbours([m23])
        v3._Node__addNeighbours([m23])
        if m12 != None:
          m23._Node__addNeighbours([m12])
      else:
        v2._Node__addNeighbours([v3])
        
      if v3tris != 1 and v1tris != 1:
        m = v3pos + (v1pos - v3pos)*0.5
        m31 = self.__mesh._NavigationMesh__newNode(m.x, m.y, m.z)
        Log().debug("add midpoint for %d & %d: %d [%.2f, %.2f, %.2f]" % 
          (v3._Node__id, v1._Node__id, m31._Node__id, m.x, m.y, m.z))
        v3._Node__addNeighbours([m31])
        v1._Node__addNeighbours([m31])
        if m12 != None:
          m31._Node__addNeighbours([m12])
        if m23 != None:
          m31._Node__addNeighbours([m23])
      else:
        v3._Node__addNeighbours([v1])
        
      
    def getNormal(self):
      if self.__normal == None:
        p1 = self.__nodes[0]._Node__position
        p2 = self.__nodes[1]._Node__position
        p3 = self.__nodes[2]._Node__position
        self.__normal = ((p2 - p1).crossProduct(p3 - p1)).normalisedCopy()
      return self.__normal
      
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
      
      
    def __str__(self):
      return "Triangle[%d, %d, %d]" % (self.__nodes[0].getId(), 
          self.__nodes[1].getId(), self.__nodes[2].getId())
  
  ##----------------------------------------------------------------------------
  
  ## Constructor
  def __init__(self):
    self.__ogreMesh = None
    self.__nodes = []
    self.__triangles = []
    
  ## Destructor
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
  def close(self):
    for t in self.__triangles:
      t.close()
    for n in self.__nodes:
      n.close()
    
    Log().info(self.__class__.__name__ + " closed")
    
  def __newNode (self,x,y,z):
    for vertex in self.__nodes:
      p = vertex._Node__position
      if (abs(p.x-x)<1e-6) and (abs(p.y-y)<1e-6) and (abs(p.z-z)<1e-6):
        return vertex
    # else create a new vertex...
    newNode = self.__Node(ogre.Vector3(x,y,z))
    self.__nodes.append(newNode)
    return newNode
    
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
    
  def _buildTriangle(self,id1,id2,id3):
    size = len(self.__nodes)
    if id1 > size or id2 > size or id3 > size:
      raise Exception ("vertex id out of range")
    return self.__newTriangle(self.__nodes[id1-1], self.__nodes[id2-1], self.__nodes[id3-1])
    
  def buildLinks(self):
    for t in self.__triangles:
      t.buildLinks()
      
  def getNode(self, nid):
    return self.__nodes[nid]
    
  def getNodes(self):
    return list(self.__nodes)
    
  def getTriangle(self, tid):
    return self.__triangles[tid]
    
  def getTriangles(self):
    return list(self.__triangles)
    
  
  def __resetTraingleTest(self):
    for tri in self.__triangles:
      tri._tested = False
    
    
  #-----------------------------------------------------------------------------
  ## 
  #  @param _lastTri - The first triangle to test
  #  @todo Change this to a itterative approche. This will miss close neighbours
  #    and pick distant vertically aligned triangles (which we don't want)
  def getPointOnMesh(self, _point, _firstTri=None, _reset=True):
      
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
  def findPath(self,_start,_goal):
    # test start point and goal point are in triangles,
    '''output = self.getPointOnMesh(_start)
    if ouput == None:
      return None
    _start.y = output[0]
    output = self.getPointOnMesh(_goal)'''
    
    # Create start and end node, linking them with all the nodes in their 
    # respective triangle
    
    # Calculate the path using A*
    path = self.__astar_calculatePath()
    
    # Delete start and end node
    
    return path
    
  #-----------------------------------------------------------------------------
  ##
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
    
    return self.__astar_reconstructPath(_goal)
    
    
  #-----------------------------------------------------------------------------
  def __astar_popLowestRank(self,_openList):
    low = 0
    if len(_openList) != 1: # we'll just let it crash if an empty list is passed
      for i in range(1,len(_openList)):
        if _openList[i]._Node__astar_rank < _openList[low]._Node__astar_rank:
          low = i
    return _openList.pop(low)
    
    
  #-----------------------------------------------------------------------------
  def __astar_heuristic(self, _node, _goal):
    return _node._Node__position.distance(_goal._Node__position)
    
    
  #-----------------------------------------------------------------------------
  def __astar_movementcost(self, _nodeA, _nodeB):
    return _nodeA._Node__astar_neighbourCosts[_nodeB]
    
    
  #-----------------------------------------------------------------------------
  def __astar_reconstructPath(self, _node, _path=[]):
    _path.insert(0,_node)
    if _node._Node__astar_parent == None:
      return _path
    return self.__astar_reconstructPath(_node._Node__astar_parent, _path)
    
    
  #-----------------------------------------------------------------------------
  def addTriangle (self,pt1,pt2,pt3):
    vertex1 = self.__newNode(pt1[0],pt1[1],pt1[2])
    vertex2 = self.__newNode(pt2[0],pt2[1],pt2[2])
    vertex3 = self.__newNode(pt3[0],pt3[1],pt3[2])
    
    return self.__newTriangle(vertex1,vertex2,vertex3)
    
    

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
    
    
    
