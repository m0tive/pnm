## @file eventManager.py
#  @brief 

import os, os.path
import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App


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
		
		
	def start(self,pluginConfig=None,resourcesConfig="resources.cfg",restoreConfig=False):
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
		self.ogreRoot.startRendering()
		
		return True
		
		
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
		return True #App().eventManager.hook("render_frameStarted",evt)