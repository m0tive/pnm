
import ogre.renderer.OGRE as ogre
from ..logger import Log
from ..application import Application as App

class Camera (object):
	def __init__(self, sceneManager, parent=None, name="Camera"):
		self.__camera = None
		self.__node = None
		
		if parent == None:
			parent = sceneManager.getRootSceneNode()
		
		self.__camera = sceneManager.createCamera(name)
		self.__node = parent.createChildSceneNode(name + "Node")
		self.__node.attachObject(self.__camera)
		
		
	def __del__(self):
		Log().info("Camera deleted")
		
		
	def getNode(self):
		return self.__node
		
		
	def getCamera(self):
		return self.__camera
		