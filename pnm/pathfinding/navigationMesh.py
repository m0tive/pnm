
from ..logger import Log
from ..application import Application as App

import ogre.renderer.OGRE as ogre

## 
class NavigationMesh (object):
  
  class __Node ():
    __idIt = 1
    
    def __init__(self,pos):
      self.__id = NavigationMesh._NavigationMesh__Node.__idIt
      NavigationMesh._NavigationMesh__Node.__idIt += 1
      self.__mesh = None
      self.__position = pos
      
    def getMesh(self):
      return self.__mesh
      
    def getPosition(self):
      return self.__position
      
    def getId(self):
      return self.__id
      
  class __Triangle ():
    def __init__(self,n1,n2,n3):
      n1._Node__mesh = self
      n3._Node__mesh = self
      n2._Node__mesh = self
      
      self.__nodes = [n1,n2,n3]
      self.__neighbours = []
      
    def addNeighbour (self,triangle):
      if len(self.__neighbours) == 3:
        return False
      self.__neighbours.append(triangle)
      if not triangle.isNeighbour(self):
        triangle.addNeighbour(self)
      return True
      
    def isNeighbour (self,triangle):
      return (triangle in self.__neighbours)
      
    def __str__(self):
      return "Triangle [%d, %d, %d]" % (self.__nodes[0].getId(), self.__nodes[1].getId(), self.__nodes[2].getId())
  
  def __init__(self):
    self.__ogreMesh = None
    self.__nodes = []
    self.__triangles = []

    #self.loadMesh(meshName)
    
  def __newNode (self,x,y,z):
    for node in self.__nodes:
      p = node._Node__position
      if (abs(p.x-x)<1e-6) and (abs(p.y-y)<1e-6) and (abs(p.z-z)<1e-6):
        return node
    # else create a new node...
    newNode = self.__Node(ogre.Vector3(x,y,z))
    self.__nodes.append(newNode)
    return newNode
    
  def __newTriangle (self,n1,n2,n3):
    
    neighbours = []
    
    for tri in self.__triangles:
      matches = 0
      for node in tri._Triangle__nodes:
        if n1 == node or n2 == node or n3 == node:
          matches += 1
      if matches == 3:
        return tri
      
      if matches == 2:
        neighbours.append(tri)
      
    newTriangle = self.__Triangle(n1,n2,n3)
    for tri in neighbours:
      if not newTriangle.addNeighbour(tri):
        raise Exception ("adding neighbouts failed")
    self.__triangles.append(newTriangle)
    return newTriangle
    
  def _buildTriangle(self,id1,id2,id3):
    size = len(self.__nodes)
    if id1 > size or id2 > size or id3 > size:
      raise Exception ("node id out of range")
    return self.__newTriangle(self.__nodes[id1-1], self.__nodes[id2-1], self.__nodes[id3-1])
    
  def addTriangle (self,pt1,pt2,pt3):
    node1 = self.__newNode(pt1[0],pt1[1],pt1[2])
    node2 = self.__newNode(pt2[0],pt2[1],pt2[2])
    node3 = self.__newNode(pt3[0],pt3[1],pt3[2])
    
    return self.__newTriangle(node1,node2,node3)
    
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
    
    if self.__ogreMesh.sharedVertexData:
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
      help(posElement.getBestColourVertexElementType)
      
    
    edgeList = self.__ogreMesh.getEdgeList()
    for triangle in edgeList.triangles:
      pass #Log().debug(triangle)
    
    '''"""
    
    
    
