## @file camera.py
#  @brief A %camera class to contain and manage the OGRE camera
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.events.camera
#  @brief A camera class to contain and manage the OGRE camera.

#-------------------------------------------------------------------------------


import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App


#-------------------------------------------------------------------------------
## A %camera class to contain and manage the OGRE %camera.
#  Using Camera.track, the %camera keeps x and z-axis transformations relative 
#  and translations in the y-axis relative in its parent's transformation space.
class Camera (object):
  
  #-----------------------------------------------------------------------------
  ## Local transfromation space flag
  TS_LOCAL = ogre.Node().TransformSpace().TS_LOCAL
  ## Parent transfromation space flag
  TS_PARENT = ogre.Node().TransformSpace().TS_PARENT
  ## World transformation space flag
  TS_WORLD = ogre.Node().TransformSpace().TS_WORLD
  
  
  #-----------------------------------------------------------------------------
  ## Constructor
  #  Creates a new %camera and attaches it to the given parent OGRE SceneNode
  #  @param sceneManager - The OGRE scene manager
  #  @param parent - Parent OGRE sceneNode to attach the %camera to (defaults to
  #    the root SceneNode)
  #  @param name - The camera's name. (default, "Camera")
  #  @param trackSpeed - The speed multiplier for Camera.track motion. (default,
  #    150)
  def __init__(self, sceneManager, parent=None, name="Camera", trackSpeed=150):
    ## The OGRE %camera entity
    self.__camera = None
    ## Outer OGRE SceneNode the %camera is attached to
    self.__node = None
    ## Inner OGRE SceneNode used for rotation
    self.__rotNode = None
    ## The speed multiplier for Camera.track motion.
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
    
  
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    Log().info("Camera deleted")
    
    
  #def getNode(self):
  #  return self.__node
    
  #-----------------------------------------------------------------------------
  ## Translate relative to the X-Z plane.
  #  Y rotation (yaw) is taken into account
  def track(self,x=0,y=0,z=0):
    if x or z:
      self.__node.translate(x*self.__trackSpeed,0,z*self.__trackSpeed,
          self.TS_LOCAL)
    if y:
      self.__node.translate(0,y*self.__trackSpeed,0,self.TS_PARENT)
    
  #-----------------------------------------------------------------------------
  ## Translate the camera's SceneNode
  #  @param x - x-axis translation (default, 0)
  #  @param y - y-axis translation (default, 0)
  #  @param z - z-axis translation (default, 0)
  #  @param ts - Transformation space (default, Camera.TS_LOCAL)
  def translate(self,x=0,y=0,z=0,ts=TS_LOCAL):
    self.__node.translate(x,y,z,ts)
    
    
  #-----------------------------------------------------------------------------
  ## Reset the camera's translation
  def resetPosition(self):
    self.__node.setPosition(0,0,0)
    
    
  #-----------------------------------------------------------------------------
  ## Apply a relative yaw rotation (ie. about the y-axis) to the %camera
  #  @param angle - The angle of rotation in radians
  #  @param ts - Transformation space (default, Camera.TS_LOCAL)
  def yaw(self,angle,ts=TS_LOCAL):
    self.__node.yaw(angle,ts)
    
  
  #-----------------------------------------------------------------------------
  ## Apply a relative pitch rotation (ie. about the x-axis) to the %camera
  #  @param angle - The angle of rotation in radians
  #  @param ts - Transformation space (default, Camera.TS_LOCAL)
  def pitch(self,angle,ts=TS_LOCAL):
    self.__rotNode.pitch(angle,ts)
    
    
  #-----------------------------------------------------------------------------
  ## Reset the camera's rotation
  def resetOrientation(self):
    self.__rotNode.resetOrientation()
    self.__node.resetOrientation()
    
    
  #-----------------------------------------------------------------------------
  ## Get a reference to the OGRE %camera
  def getOgreCamera(self):
    return self.__camera
    
