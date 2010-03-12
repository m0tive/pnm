
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
		
		self.__inputListener = None
		
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
		
		params = [("WINDOW",str(windowHnd)),
				("w32_keyboard","DISCL_FOREGROUND"),
				("w32_keyboard", "DISCL_NONEXCLUSIVE"),
				("x11_keyboard_grab", "false"),
				("w32_mouse","DISCL_FOREGROUND"),
				("w32_mouse", "DISCL_NONEXCLUSIVE"),
				("x11_mouse_grab", "false"),
				("x11_mouse_hide", "false")]
		self.system = OIS.createPythonInputSystem( params )
		self.__keyb = self.system.createInputObjectKeyboard(OIS.OISKeyboard, True)
		self.__mous = self.system.createInputObjectMouse(OIS.OISMouse, True)
		
		self.__inputListener = InputListener()
		self.__keyb.setEventCallback(self.__inputListener)
		self.__mous.setEventCallback(self.__inputListener)
		
	## Process inputs
	#  @param timeElapsed - Time since last update
	def update(self,timeElapsed):
		self.__keyb.capture()
		self.__mous.capture()
		








import ogre.renderer.OGRE as ogre
import re

class InputListener (OIS.KeyListener, OIS.MouseListener):
	def __init__(self, keyboardConfig="keyboard.cfg"):
		OIS.KeyListener.__init__(self)
		OIS.MouseListener.__init__(self)
		
		self.__keyMaps = {}
		self.__activeMaps = []
		
		self.__setupKeyboard(keyboardConfig)
		
		Log().debug("InputListener created")
		
	def __setupKeyboard(self,keyboardConfig):
		Log().debug("Loading keyboard map")
		
		config = ogre.ConfigFile()
		config.load(keyboardConfig)
		
		sectionIterator = config.getSectionIterator()
		keySplit = re.compile('\+')
		typeSplit = re.compile('-')
		while sectionIterator.hasMoreElements():
			name = sectionIterator.peekNextKey()
			section = sectionIterator.getNext()
			if name == '':
				continue
			Log().debug("Config group \'%s\'" % name)
			kMap = {'p':[], 'r':[], 'h':[]}
			for item in section:
				Log().debug("Config item key=\'%s\' value=\'%s\'" % (item.key, item.value))
				errorStr = "Repeated keys in keymap \'%s\': \'%s\'" % (name, item.key)
				eventType = typeSplit.split(item.key)
				Log().debug("Processing type=\'%s\'" % eventType)
				keys = keySplit.split(eventType[1])
				eventType = eventType[0]
				Log().debug("Processing type=%s keys=\'%s\'" % (eventType, keys))
				shift = None
				ctrl = None
				## fix shifts and controls
				for i in range(len(keys)):
					if keys[i] == "SHIFT":
						shift = i
						if "LSHIFT" in keys:
							if "RSHIFT" in keys:
								raise Exception (errorStr)
							else:
								keys[i] = "RSHIFT"
						else:
							keys[i] = "LSHIFT"
					if keys[i] == "CONTROL":
						ctrl = i
						if "LCONTROL" in keys:
							if "RCONTROL" in keys:
								raise Exception (errorStr)
							else:
								keys[i] = "RCONTROL"
						else:
							keys[i] = "LCONTROL"
				
				if shift != None and "RSHIFT" in keys:
					Log().debug("Adding second shift")
					keys[shift] = "RSHIFT"
					kMap[eventType].append([keys,item.value])
				if ctrl != None and "RCONTROL" not in keys:
					Log().debug("Adding second ctrl")
					keys[ctrl] = "RCONTROL"
					kMap[eventType].append([keys,item.value])
				
				for i in range(len(keys)):
					if keys.count(keys[i]) != 1:
						raise Exception (errorStr)
					keys[i] = "KC_" + keys[i]
				
				Log().debug("Split key: " + str(keys))
				kMap[eventType].append([keys,item.value])
				
			Log().debug("Map: " + str(kMap['p']))
			if name in self.__keyMaps:
				self.__keyMaps[name][0].extend(kMap['p'])
				self.__keyMaps[name][1].extend(kMap['r'])
				self.__keyMaps[name][2].extend(kMap['h'])
			else:
				self.__keyMaps[name] = []
				self.__keyMaps[name].append(kMap['p'])
				self.__keyMaps[name].append(kMap['r'])
				self.__keyMaps[name].append(kMap['h'])
				if (name == "Global") and ("Global" not in self.__activeMaps):
					self.__activeMaps.append("Global")
				
		Log().debug("Loaded maps: " + str(self.__keyMaps))
	
	def keyPressed(self,evt):
		#App().eventManager.hook("input_keyPressed")
		#Log().debug("Key pressed: '%s' '%c'" % (evt.key, evt.text))
		
		for name in self.__activeMaps:
			for keySet in self.__keyMaps[name][0]:
				#hit = True
				for k in keySet[0]:
					Log().debug("~ " + str(k))
					if OIS.__dict__[k] == evt.key:
						Log().debug("hit! " + str(evt.key))
						return
		
	def keyReleased(self,evt):
		App().eventManager.hook("input_keyReleased")
		Log().debug("Key released: '%s' '%c'" % (evt.key, evt.text))		
		if evt.key == OIS.KC_ESCAPE:
			App().renderManager.quit(True)
		
	def mouseMoved(self,evt):
		App().eventManager.hook("input_mouseMoved")
		
	def mousePressed(self,evt,button):
		App().eventManager.hook("input_mousePressed")
		
	def mouseReleased(self,evt,button):
		App().eventManager.hook("input_mouseReleased")