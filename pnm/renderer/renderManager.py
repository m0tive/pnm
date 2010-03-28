## @file renderManager.py
#  @brief OGRE and render manager.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.events.renderManager
#  @brief OGRE and render manager.

#-------------------------------------------------------------------------------


import os, os.path
import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App
from ..pathfinding.navigationMesh import NavigationMesh
from camera import Camera
from ..pathfinding.buildFixedNavMesh import buildFixedNavMesh

## Render manager.
class RenderManager (object):
  ## Constructor.
  def __init__(self):
    self.__setup = False
    self.__quit = False
    
    self.ogreRoot = None
    
    self.window = None
    self.__windowEventListener = None
    self.__frameListener = None
    
    self.sceneManager = None
    self.__camera = None
    self.rootNode = None
    self.sceneNode = None
    
    self.__viewport = None
    
    self.__axisCount = 0
    
    
  def __del__(self):
    Log().info("RenderManager deleted")
    
    
  def close(self):
    if self.__windowEventListener:
      ogre.WindowEventUtilities.removeWindowEventListener(self.window, 
          self.__windowEventListener)
    
    if self.__frameListener:
      self.ogreRoot.removeFrameListener(self.__frameListener)
      
    del self.__windowEventListener
    del self.__frameListener
    
    Log().info("RenderManager closed")
    
    
  def quit(self,do=False):
    if do:
      self.__quit = True
      Log().info("RenderManager quitting")
    return self.__quit
    
  def getCamera (self):
    return self.__camera
    
    
  def setup(self,pluginConfig=None,resourcesConfig="resources.cfg",restoreConfig=False):
    if self.__setup:
      raise Exception("RenderManager.setup(...) run twice")
    self.__setup = True
    
    if not pluginConfig:
      pluginConfig = os.path.join(os.getcwd(), 'plugins', 'plugins.cfg')
    self.ogreRoot = ogre.Root(pluginConfig)
    
    self._addResourcesLocations(resourcesConfig)
    
    if (not restoreConfig) or (not self.ogreRoot.restoreConfig()):
      if not self.ogreRoot.showConfigDialog():
        return False
    
    self._createWindow("Window")
    
    self.__frameListener = FrameListener(self)
    self.ogreRoot.addFrameListener(self.__frameListener)
    
    self.sceneManager = self.ogreRoot.createSceneManager(ogre.ST_GENERIC,"SceneManager")
    #self.sceneManager.setDisplaySceneNodes(True)
    self.rootNode = self.sceneManager.getRootSceneNode()
    
    self.__camera = Camera(self.sceneManager)
    #camNode = self.__camera.getNode()
    #camNode.translate(0,0,200)
    #self.__camera.translate(0,100,200)
    
    
    self.__viewport = self.window.addViewport(self.__camera.getOgreCamera())
    self.__viewport.BackgroundColour = ogre.ColourValue(0.1,0.1,0.1)
    
    ogre.TextureManager.getSingleton().setDefaultNumMipmaps (5)
    
    #ogre.ResourceGroupManager.getSingleton().initialiseResourceGroup("OgreCore")
    #ogre.ResourceGroupManager.getSingleton().initialiseResourceGroup("General")
    ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
    
    ## build scene...
    
    self.sceneManager.ambientLight = ogre.ColourValue(.1,.1,.1)
    
    lightMain = self.rootNode.createChildSceneNode("MainLightNode")
    light = self.sceneManager.createLight("MainLight")
    light.setType(ogre.Light.LT_DIRECTIONAL)
    light.setDiffuseColour (1,1,1)
    lightMain.attachObject(light)
    
    lightMain.setPosition (10,100,0)
    lightMain.yaw(ogre.Math.DegreesToRadians(30))
    lightMain.pitch(ogre.Math.DegreesToRadians(45))
    
    self.attachAxis(lightMain)
    
    lightFill = self.rootNode.createChildSceneNode("FillLightNode")
    light = self.sceneManager.createLight("FillLight")
    light.setType(ogre.Light.LT_DIRECTIONAL)
    light.setDiffuseColour (.1,.1,.15)
    lightFill.attachObject(light)
    
    lightFill.setPosition (-10,100,0)
    lightFill.yaw(ogre.Math.DegreesToRadians(60))
    lightFill.yaw(ogre.Math.DegreesToRadians(180))
    lightFill.pitch(ogre.Math.DegreesToRadians(-30))
    
    self.attachAxis(lightFill)
    
    
    meshManager = ogre.MeshManager.getSingleton()
    meshManager.createPlane('gridPlane','General',
          ogre.Plane(ogre.Vector3().UNIT_Y, ogre.Vector3().ZERO),
          5000,5000,10,10,upVector=ogre.Vector3().UNIT_Z)
    
    gridEntity = self.sceneManager.createEntity('gridEntity', 'gridPlane')
    gridNode = self.rootNode.createChildSceneNode("gridNode")
    gridNode.attachObject(gridEntity)
    gridEntity.setMaterialName("pnm/Wireframe")
    
    self.sceneNode = self.rootNode.createChildSceneNode("sceneNode")
    self.sceneNode.scale(100,100,100)
    
    #testEnt = self.sceneManager.createEntity('Cube', 'navMesh.mesh')
    #cubeNode = self.rootNode.createChildSceneNode("CubeNode")
    #cubeNode.attachObject(testEnt)
    #cubeNode.scale(100,100,100)
    #cubeNode.translate(0,5,0)
    
    """navMesh = testEnt.getMesh()
    nM_edgeList = navMesh.getEdgeList()
    nM_triangles = nM_edgeList.triangles
    
    Log().debug(len(nM_triangles))"""
    
    #navMesh = NavigationMesh("navMesh.mesh")
    
    #navMesh = NavigationMesh()
    #buildFixedNavMesh(navMesh)
    #navMesh.buildLinks()
    
    #navMesh.close()
    
    
    from pnm.math import Math
    #Log().debug(Math.distanceToLine(ogre.Vector3(0,0,0), ogre.Vector3(0,,1), ogre.Vector3(0,1,-1)))
    
    return True
    
  def displayMesh(self,name,parent=None):
    if parent == None:
      parent = self.sceneNode
    entity = self.sceneManager.createEntity(name + "Entity", name + ".mesh")
    node = parent.createChildSceneNode(name + "Node")
    node.attachObject(entity)
    
    return entity, node
  
  def start(self):
    App().eventManager.hook("input_resetView")
    self.ogreRoot.startRendering()
    
    
  def update(self,timeElapsed):
    self.__timeElapsed = timeElapsed
    
  def getTimeElapsed(self):
    return self.__timeElapsed
    
  def _addResourcesLocations(self,resourcesConfig):
    config = ogre.ConfigFile()
    config.load(resourcesConfig)
    
    rgm = ogre.ResourceGroupManager.getSingleton()
    sectionIterator = config.getSectionIterator()
    while sectionIterator.hasMoreElements():
      name = sectionIterator.peekNextKey()
      section = sectionIterator.getNext()
      Log().debug("Adding resource group \'%s\'" % name)
      for item in section:
        rgm.addResourceLocation(item.value, item.key, name)
        Log().debug("Adding location \'%s\'" % item.value)
    
    
  def _createWindow(self,title):
    if self.window:
      raise Exception("RenderManager._createWindow(...) run twice")
    self.window = self.ogreRoot.initialise(True,title)
    self.__windowEventListener = WindowEventListener(self)
    self.__windowEventListener.windowResized(self.window)
    ogre.WindowEventUtilities.addWindowEventListener(self.window, 
        self.__windowEventListener)
    App().eventManager.hook("render_windowCreated",self)
    
    
  def attachAxis(self,node):
    entity = self.sceneManager.createEntity('__Axis_' + str(self.__axisCount), 'axes.mesh')
    node.attachObject(entity)
    self.__axisCount += 1
    return entity
    
    
## Window event listener
class WindowEventListener (ogre.WindowEventListener):
  def __init__ (self,rm):
    super(WindowEventListener,self).__init__()
    self.__rm = rm
    
  def __del__ (self):
    Log().debug("WindowEventListener deleted")
    
  def windowClosed (self, rw):
    App().eventManager.hook("render_windowQuit",rw)
    
  def windowResized (self, rw):
    pass
    
    
## Frame event listener
class FrameListener (ogre.FrameListener):
  def __init__ (self,rm):
    super(FrameListener,self).__init__()
    self.__rm = rm
    
  def __del__ (self):
    Log().debug("FrameListener deleted")
    
  def frameStarted (self, evt):
    if self.__rm.quit():
      Log().debug("FrameListener detected a quitter")
      return False
    self.__rm.update(evt.timeSinceLastFrame)
    return App().eventManager.hook("render_frameStarted",evt)
