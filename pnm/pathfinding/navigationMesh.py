
from ..logger import Log
from ..application import Application as App

import ogre.renderer.OGRE as ogre

## 
class NavigationMesh (object):
 
  #class __Node ():
    #def __init__(self,p1,p2):
      #pass
    
  ##----------------------------------------------------------------------------
  
  class __Node ():
    __idIt = 1
    
    def __init__(self,pos):
      self.__id = NavigationMesh._NavigationMesh__Node.__idIt
      NavigationMesh._NavigationMesh__Node.__idIt += 1
      self.__position = pos
      self.__triangles = []
      self.__neighbours = []
    
    #def __del__(self):
      #Log().info(self.__class__.__name__ + " deleted")
      
    def close(self):
      del self.__position
      del self.__triangles
      del self.__neighbours
      
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
          self.__neighbours.append(n)
          n._Node__neighbours.append(self)
  
  ##----------------------------------------------------------------------------
  
  class __Triangle ():
    def __init__(self,v1,v2,v3):
      self.__mesh = None
      v1._Node__triangles.append(self)
      v2._Node__triangles.append(self)
      v3._Node__triangles.append(self)
      
      self.__vertices = [v1,v2,v3]
      
      self.__neighbours = []
      Log().debug("building %s" % self)
    
    #def __del__(self):
      #Log().info(self.__class__.__name__ + " deleted")
      
    def close(self):
      del self.__neighbours
      del self.__vertices
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
      return list(self.__vertices)
      
    def buildLinks(self):
      v1 = self.__vertices[0]
      v2 = self.__vertices[1]
      v3 = self.__vertices[2]
      
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
        
      
      
    def __str__(self):
      return "Triangle[%d, %d, %d]" % (self.__vertices[0].getId(), 
          self.__vertices[1].getId(), self.__vertices[2].getId())
  
  ##----------------------------------------------------------------------------
  
  def __init__(self):
    self.__ogreMesh = None
    self.__vertices = []
    self.__triangles = []

    #self.loadMesh(meshName)
    
  def __del__(self):
    Log().info(self.__class__.__name__ + " deleted")
    
  def close(self):
    for t in self.__triangles:
      t.close()
    for n in self.__vertices:
      n.close()
    
    Log().info(self.__class__.__name__ + " closed")
    
  def __newNode (self,x,y,z):
    for vertex in self.__vertices:
      p = vertex._Node__position
      if (abs(p.x-x)<1e-6) and (abs(p.y-y)<1e-6) and (abs(p.z-z)<1e-6):
        return vertex
    # else create a new vertex...
    newNode = self.__Node(ogre.Vector3(x,y,z))
    self.__vertices.append(newNode)
    return newNode
    
  def __newTriangle (self,v1,v2,v3):
    
    neighbours = []
    
    for tri in self.__triangles:
      matches = 0
      for vertex in tri._Triangle__vertices:
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
    size = len(self.__vertices)
    if id1 > size or id2 > size or id3 > size:
      raise Exception ("vertex id out of range")
    return self.__newTriangle(self.__vertices[id1-1], self.__vertices[id2-1], self.__vertices[id3-1])
    
  def buildLinks(self):
    for t in self.__triangles:
      t.buildLinks()
    
  def addTriangle (self,pt1,pt2,pt3):
    vertex1 = self.__newNode(pt1[0],pt1[1],pt1[2])
    vertex2 = self.__newNode(pt2[0],pt2[1],pt2[2])
    vertex3 = self.__newNode(pt3[0],pt3[1],pt3[2])
    
    return self.__newTriangle(vertex1,vertex2,vertex3)
    
    #Log().debug(tri)
    #Log().debug(tri._Triangle__neighbours)
    #Log().debug(len(self.__triangles))

  """def loadMesh(self,meshName):
    del self.__ogreMesh
    
    
    '''
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
    
    '''"""
    
    
    
