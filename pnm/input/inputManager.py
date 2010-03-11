
#import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
from ..logger import Log
from ..application import Application as App

## Keyboard, Mouse and Joystick input manager
class InputManager (object):
	## Constructor
	def __init__(self):
		self.__setup = False
		self.system = None
		
		self.__keyb = False
		self.__mous = False
		self.__joys = False
		
		self.__keybListener = None
		
	def __del__(self):
		Log().info("InputManager deleted")
		
	def close(self):
		Log().info("InputManager closed")
		
	## Setup input systems
	#  Only run once
	def setup(self):
		if self.__setup:
			raise Exception ("InputManager.setup(...) run twice")
		self.__setup = True
		
		#Log().debug(dir(OIS.KeyListener().keyPressed))
		
		
		## From the ogre demo Simple Application.
		## I assume it fixes an issue on 64bit computers...
		import platform
		int64 = False
		for bit in platform.architecture():
				if '64' in bit:
						int64 = True
		if int64:
				windowHnd = App().renderManager.window.getCustomAttributeUnsignedLong("WINDOW")
		else:
				windowHnd = App().renderManager.window.getCustomAttributeInt("WINDOW")
		
		params = [("WINDOW",str(windowHnd))]
		self.system = OIS.createPythonInputSystem( params )
		self.__keyb = self.system.createInputObjectKeyboard(OIS.OISKeyboard, True)
		
		#self.__keybListener = KeyListener()
		#self.__keyb.setEventCallback(self.__keybListener)
	
	## Process inputs
	#  @param timeElapsed - Time since last update
	def update(self,timeElapsed):
		self.__keyb.capture()
	
	
class KeyListener (OIS.KeyListener):
	def __init__(self):
		Log().debug("KeyListener created")
	
	def keyPressed(self,keyEvent):
		Log().debug(str(keyEvent.text))