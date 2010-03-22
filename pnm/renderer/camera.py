
import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App

class Camera (object):
  TS_LOCAL = ogre.Node().TransformSpace().TS_LOCAL
  TS_PARENT = ogre.Node().TransformSpace().TS_PARENT
  TS_WORLD = ogre.Node().TransformSpace().TS_WORLD
  
  def __init__(self, sceneManager, parent=None, name="Camera", trackSpeed=150):
    self.__camera = None
    self.__node = None
    
    self.__trackSpeed = trackSpeed
    
    if parent == None:
      parent = sceneManager.getRootSceneNode()
    
    self.__camera = sceneManager.createCamera(name)
    self.__camera.setNearClipDistance(0.1)
    self.__node = parent.createChildSceneNode(name + "Node")
    self.__rotNode = self.__node.createChildSceneNode(name + "RotNode")
    #self.__inner = node.createChildSceneNode(name + "InnerNode")
    #self.__inner.attachObject(self.__camera)
    self.__rotNode.attachObject(self.__camera)
    
    
  def __del__(self):
    Log().info("Camera deleted")
    
    
  #def getNode(self):
  #  return self.__node
    
  ## Translate relative to the X-Z plane
  #  Y rotation (yaw) is taken into account
  def track(self,x=0,y=0,z=0):
    if x or z:
      self.__node.translate(x*self.__trackSpeed,0,z*self.__trackSpeed,self.TS_LOCAL)
    if y:
      self.__node.translate(0,y*self.__trackSpeed,0,self.TS_PARENT)
    
    
  def translate(self,x=0,y=0,z=0,ts=TS_LOCAL):
    self.__node.translate(x,y,z,ts)
    
    
  def yaw(self,angle,ts=TS_LOCAL):
    self.__node.yaw(angle,ts)
    
  def pitch(self,angle,ts=TS_LOCAL):
    self.__rotNode.pitch(angle,ts)
    
    
  def getCamera(self):
    return self.__camera
    
