## @file eventManager.py
#  @brief 

import os, os.path
import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App
from camera import Camera

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
		
		self.__viewport = None
		
		
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
		self.sceneRoot = self.sceneManager.getRootSceneNode()
		
		self.__camera = Camera(self.sceneManager)
		#camNode = self.__camera.getNode()
		#camNode.translate(0,0,200)
		self.__camera.translate(z=200)
		
		
		self.__viewport = self.window.addViewport(self.__camera.getCamera())
		self.__viewport.BackgroundColour = ogre.ColourValue(0,0,0)
		
		## build scene...
		
		self.sceneManager.ambientLight = ogre.ColourValue(0.5,0.5,0.5)
		
		meshManager = ogre.MeshManager.getSingleton()
		meshManager.createPlane('testPlane','General',
					ogre.Plane(ogre.Vector3().UNIT_Z, ogre.Vector3().ZERO),100,100,2,2)
		
		testNode = self.sceneRoot.createChildSceneNode("Test")
		testNode.attachObject(self.sceneManager.createEntity('testEntity', 'testPlane'))
		
		return True
	
	
	def start(self):
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
		
		
	def loadAllResources(self):
		ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
		
		
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