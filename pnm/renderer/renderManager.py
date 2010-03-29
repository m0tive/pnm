## @file renderManager.py
#  @brief OGRE and render manager.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.renderer.renderManager
#  @brief OGRE and render manager.

#-------------------------------------------------------------------------------


import os, os.path
import ogre.renderer.OGRE as ogre

from ..logger import Log
from ..application import Application as App
from camera import Camera

from ..pathfinding.navigationMesh import NavigationMesh
from ..pathfinding.buildFixedNavMesh import buildFixedNavMesh


#-------------------------------------------------------------------------------
## OGRE and render manager.
class RenderManager (object):

  #-----------------------------------------------------------------------------
  ## Constructor.
  def __init__(self):
    # Public variables
    ## OGRE %application Root
    self.ogreRoot = None
    ## Window object
    self.window = None
    ## OGRE sceneManager
    self.sceneManager = None
    ## root sceneNode
    self.rootNode = None
    ## sceneNode containing all displayed objects
    self.sceneNode = None
    
    # Private variables
    ## Setup flag (True after RenderManager.setup has been run once)
    self.__setup = False
    ## Close down flag (True if render loop is to stop)
    #  @see RenderManager.quit
    self.__quit = False
    ## Window event listener
    #  @see WindowEventListener
    self.__windowEventListener = None
    ## Frame event listener
    #  @see FrameListener
    self.__frameListener = None
    ## %Camera object
    #  @see pnm.renderer.camera.Camera
    self.__camera = None
    ## OGRE viewport
    self.__viewport = None
    ## Axis name id
    self.__axisCount = 0
    
  
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    Log().info("RenderManager deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    if self.__windowEventListener:
      ogre.WindowEventUtilities.removeWindowEventListener(self.window, 
          self.__windowEventListener)
    
    if self.__frameListener:
      self.ogreRoot.removeFrameListener(self.__frameListener)
      
    del self.__windowEventListener
    del self.__frameListener
    
    Log().info("RenderManager closed")
    
    
  #-----------------------------------------------------------------------------
  ## Access or set the quit flag.
  #  If False is passed (or \c do is ommited), then the current state of quit is
  #  returned. If True is passed, RenderManager.__quit is set to True and the 
  #  %renderer will quit at the start of the next render loop (inside 
  #  WindowEventListener.frameStarted )
  #  @param do - True to set the %renderer to quite, False (default) to query 
  #    the value of RenderManager.__quit
  #  @return RenderManager.__quit if \c do is False
  #  @see WindowEventListener.frameStarted
  def quit(self,do=False):
    if do:
      self.__quit = True
      Log().info("RenderManager quitting")
    return self.__quit
    
    
  #-----------------------------------------------------------------------------
  ## Get the %camera object.
  #  @return a reference to RenderManager.__camera
  #  @see pnm.renderer.camera.Camera
  def getCamera (self):
    return self.__camera
    
    
  #-----------------------------------------------------------------------------
  ## Setup the %renderer, window, viewport and sceneManager.
  #  @param pluginConfig - plugin config file location, full path (default, 
  #    "./plugins/plugins.cfg")
  #  @param resourcesConfig - resource config file name (default, 
  #    "resources.cfg")
  #  @param restoreConfig - True to restore the OGRE config file, or False to 
  #    run the OGRE config dialog
  #  @return False if the setup failed or was canceled
  def setup(self,pluginConfig=None,resourcesConfig="resources.cfg",restoreConfig=False):
    if self.__setup:
      raise Exception("RenderManager.setup(...) run twice")
    self.__setup = True
    
    if not pluginConfig:
      pluginConfig = os.path.join(os.getcwd(), 'plugins', 'plugins.cfg')
    self.ogreRoot = ogre.Root(pluginConfig)
    
    self.__addResourcesLocations(resourcesConfig)
    
    if (not restoreConfig) or (not self.ogreRoot.restoreConfig()):
      if not self.ogreRoot.showConfigDialog():
        return False
    
    self.__createWindow("Window")
    
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
    
    return True
  
  
  #-----------------------------------------------------------------------------
  ## Display a mesh.
  #  The mesh is created within a new sceneNode which is created within
  #    \c parent
  #  @param name - name of mesh to be displayed
  #  @param parent - SceneNode to attach the mesh to (default, 
  #    RenderManager.sceneNode)
  #  @return tuple; The mesh entity, the sceneNode containing the entity
  def displayMesh(self,name,parent=None):
    if parent == None:
      parent = self.sceneNode
    entity = self.sceneManager.createEntity(name + "Entity", name + ".mesh")
    node = parent.createChildSceneNode(name + "Node")
    node.attachObject(entity)
    
    return entity, node
    
    
  #-----------------------------------------------------------------------------
  ## Attach a debug x-y-z axis to a sceneNode.
  #  The axis is created with a unique name, using RenderManager.__axisCount
  #  (increment be one each time) to stop conflicts.
  #  @param node - SceneNode to attach the axis to
  #  @return The axis mesh entity
  def attachAxis(self,node):
    entity = self.sceneManager.createEntity('__Axis_' + str(self.__axisCount), 
                                            'axes.mesh')
    node.attachObject(entity)
    self.__axisCount += 1
    return entity
  
  
  #-----------------------------------------------------------------------------
  ## Start the render loop
  def start(self):
    App().eventManager.hook("input_resetView")
    self.ogreRoot.startRendering()
    
    
  #-----------------------------------------------------------------------------
  ## Update the render manager with the time elapsed in the last frame.
  #  Called in scripts.render_frameStarted
  def update(self,timeElapsed):
    self.__timeElapsed = timeElapsed
    
    
  #-----------------------------------------------------------------------------
  ## Get time elapsed since last frame
  #  @see RenderManager.update
  def getTimeElapsed(self):
    return self.__timeElapsed
    
    
  #-----------------------------------------------------------------------------
  ## Parse resource config file and add the resource locations
  #  @param resourcesConfig - Resource location config file name
  def __addResourcesLocations(self,resourcesConfig):
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
    
    
  #-----------------------------------------------------------------------------
  ## Create the OGRE render window.
  #  @note This will only run once
  #  @param title - The windows title
  def __createWindow(self,title):
    if self.window:
      raise Exception("RenderManager.__createWindow(...) run twice")
    self.window = self.ogreRoot.initialise(True,title)
    self.__windowEventListener = WindowEventListener(self)
    self.__windowEventListener.windowResized(self.window)
    ogre.WindowEventUtilities.addWindowEventListener(self.window, 
        self.__windowEventListener)
    App().eventManager.hook("render_windowCreated",self)
    
    
    
#-------------------------------------------------------------------------------
## Window event listener
#  Derived from OGRE.WindowEventListener
class WindowEventListener (ogre.WindowEventListener):

  #-----------------------------------------------------------------------------
  ## Constructor
  #  @param rm - reference to the parent RenderManager
  def __init__ (self,rm):
    super(WindowEventListener,self).__init__()
    
    ## Reference to the parent RenderManager
    self.__rm = rm
    
  
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__ (self):
    Log().debug("WindowEventListener deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Window closed event, from OGRE.WindowEventListener
  #  This is called by OGRE in the render loop when the window is closed
  def windowClosed (self, rw):
    App().eventManager.hook("render_windowQuit",rw)
    
    
  #-----------------------------------------------------------------------------
  ## Window resize event, from OGRE.WindowEventListener
  #  This is called by OGRE in the render loop when the window is resized
  def windowResized (self, rw):
    pass # keep me
    

    
#-------------------------------------------------------------------------------
## Frame event listener
#  Derived from OGRE.FrameListener
class FrameListener (ogre.FrameListener):
  
  #-----------------------------------------------------------------------------
  ## Constructor
  #  @param rm - reference to the parent RenderManager
  def __init__ (self,rm):
    super(FrameListener,self).__init__()
    self.__rm = rm
    
  
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__ (self):
    Log().debug("FrameListener deleted")
    
  
  #-----------------------------------------------------------------------------
  ## Event called before rendering a frame.
  #  Derived from OGRE.FrameListener.
  #  @param evt - event data
  #  @return False if the render loop should quit
  def frameStarted (self, evt):
    if self.__rm.quit():
      Log().debug("FrameListener detected a quitter")
      return False
    self.__rm.update(evt.timeSinceLastFrame)
    return App().eventManager.hook("render_frameStarted",evt)
