
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
		del self.__inputListener
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
		
		self.__inputListener = InputListener(self.__keyb,self.__mous)
		self.__keyb.setEventCallback(self.__inputListener)
		self.__mous.setEventCallback(self.__inputListener)
		
	## Process inputs
	#  @param timeElapsed - Time since last update
	def update(self,timeElapsed):
		self.__keyb.capture()
		self.__mous.capture()
		self.__inputListener.update(timeElapsed)
		








import ogre.renderer.OGRE as ogre
import re

## Input event listener
#  
class InputListener (OIS.KeyListener, OIS.MouseListener):
	## Constructor
	#  @param keyboard - reference to the OIS keyboard input object
	#  @param mouse - reference to the OIS mouse input object
	#  @param keyboardConfig - file name of keyboard input map config file
	def __init__(self, keyboard, mouse, keyboardConfig="keyboard.cfg"):
		OIS.KeyListener.__init__(self)
		OIS.MouseListener.__init__(self)
		
		## Time since last update
		self.__timeElapsed = 0
		
		## Reference to the OIS keyboard input object
		self._keyboard = keyboard
		## Reference to the OIS mouse input object
		self._mouse = mouse
		
		## Keyboard input maps
		self.__keyMaps = {}
		## Currently active keyboard maps' names
		self.__activeMaps = []
		
		## Keys currently pressed.
		#  The reference key for the keyboard key is the OIS key code (ie. OIS.KC_P)
		self.__downMap = {}
		
		## Load the keyboard maps
		self.__setupKeyboard(keyboardConfig)
		
		Log().debug("InputListener created")
		
	def __setupKeyboard(self,keyboardConfig):
		Log().debug("Loading keyboard map")
		
		# Keyboard maps are stored using the ogre config file, with a slight extention
		# ---------------------- start example
		# [Global]
		# r-LSHIFT+ESCAPE=exit
		# p-SPACE=jumpLeft
		# h-CONTROL+Z=run
		# ---------------------- end
		# The line 1 declares the map name. Each of the following lines declares a 
		# new key combo input untill the next map name. Each combo has three parts: 
		# [type]-[key]=[event]
		#
		# type; p - pressed, h - hold, r - released
		# key; keys, using the OIS names (minus "KC_"), joined with "+". In the case
		#   of CONTROL and SHIFT, the combo is replaced with two seperate combos 
		#   with both left and right keys in.
		# event; the event name passed to pnm.events.eventManager.EventManager.hook
		#
		# Note: Each combo can only contain one of each keys.
		
		config = ogre.ConfigFile()
		config.load(keyboardConfig) # load the maps
		
		sectionIterator = config.getSectionIterator()
		typeSplit = re.compile('-') # to split type from keys
		keySplit = re.compile('\+') # to split combined keys
		while sectionIterator.hasMoreElements():
			name = sectionIterator.peekNextKey()
			section = sectionIterator.getNext()
			if name == '': # if the keymap has no name, skip
				continue
			Log().debug("Config group \'%s\'" % name)
			kMap = {'p':[], 'r':[], 'h':[]}
			for item in section:
				Log().debug("Config item key=\'%s\' value=\'%s\'" % (item.key, item.value))
				errorStr = "Repeated keys in keymap \'%s\': \'%s\'" % (name, item.key)
				
				eventType = typeSplit.split(item.key) # get the event type
				Log().debug("Processing type=\'%s\'" % eventType)
				keys = keySplit.split(eventType[1]) # split the keys up
				eventType = eventType[0]
				
				Log().debug("Processing type=%s keys=\'%s\'" % (eventType, keys))
				shift = None
				ctrl = None
				## fix shifts and controls
				for i in range(len(keys)):
					if keys[i] == "SHIFT": # replace SHIFT
						shift = i
						if "LSHIFT" in keys:
							if "RSHIFT" in keys:
								raise Exception (errorStr)
							else:
								keys[i] = "RSHIFT"
						else:
							keys[i] = "LSHIFT"
					if keys[i] == "CONTROL": # replace CONTROL
						ctrl = i
						if "LCONTROL" in keys:
							if "RCONTROL" in keys:
								raise Exception (errorStr)
							else:
								keys[i] = "RCONTROL"
						else:
							keys[i] = "LCONTROL"
				
				## add matching RSHIFT and/or RCONTROL if needed.
				if shift != None and "RSHIFT" in keys:
					keys[shift] = "RSHIFT"
					kMap[eventType].append([keys,item.value])
				if ctrl != None and "RCONTROL" not in keys:
					keys[ctrl] = "RCONTROL"
					kMap[eventType].append([keys,item.value])
				
				# check for repeating keys, and preppend "KC_" for OIS
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
		
	def update(self,timeElapsed):
		self.timeElapsed = timeElapsed
		
		delList = []
		for key in self.__downMap:
			self.__downMap[key] -= timeElapsed
			if self.__downMap[key] <= 0:
				self.__keyReleasedActual(key)
				delList.append(key)
			#else:
			#	self.__keyHold(key)
				
		for i in delList:
			del self.__downMap[i]
			
			
		for name in self.__activeMaps:
			Log().debug("~ " + str(self.__downMap))
			for keySet in self.__keyMaps[name][2]:
				#hit = True
				for k in keySet[0]:
					#Log().debug("~ " + str(k))
					if self.isKeyDown(OIS.__dict__[k]):
						hit = True
						#for sib in keySet[0]:
						#	#Log().debug("# " + sib)
						#	if (sib != k) and not self.isKeyDown(OIS.__dict__[sib]):
						#		#Log().debug("& " + sib)
						#		hit = False
						#		break
						if hit:
							#Log().debug("Hit t%d %s" % (2,keySet))
							App().eventManager.hook(keySet[1],self)
							#break
							
		
	def isKeyDown(self,key):
		return ((key in self.__downMap) and (self.__downMap[key] > 0)) \
				or self._keyboard.isKeyDown(key)
	
	def keyPressed(self,evt):
		App().eventManager.hook("input_keyPressed",self)
		self.__proccessKey(evt.key,0)
		
		
	def keyReleased(self,evt):
		self.__downMap[evt.key] = 0.05
		
		
	def __keyHold(self,key):
		App().eventManager.hook("input_keyHold",self)
		self.__proccessKey(key,2)
		
		
	def __keyReleasedActual(self,key):
		App().eventManager.hook("input_keyReleased",self)
		self.__proccessKey(key,1)
			
			
	def __proccessKey(self,key,itype):
		for name in self.__activeMaps:
			for keySet in self.__keyMaps[name][itype]:
				#hit = True
				for k in keySet[0]:
					#Log().debug("~ " + str(k))
					if OIS.__dict__[k] == key:
						hit = True
						for sib in keySet[0]:
							#Log().debug("# " + sib)
							if (sib != k) and not self.isKeyDown(OIS.__dict__[sib]):
								#Log().debug("& " + sib)
								hit = False
								break
						if hit:
							Log().debug("Hit t%d %s" % (itype,keySet))
							App().eventManager.hook(keySet[1],self)
							break
		
		
	def mouseMoved(self,evt):
		App().eventManager.hook("input_mouseMoved",self)
		
	def mousePressed(self,evt,button):
		App().eventManager.hook("input_mousePressed",self)
		
	def mouseReleased(self,evt,button):
		App().eventManager.hook("input_mouseReleased",self)