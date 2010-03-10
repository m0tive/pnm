## @file eventManager.py
#  @brief 

import re, os, os.path
from ..logger import Log

## Event scripts manager.
#  @todo create a generate script function that creates temp scripts (which 
#  could be wrote to file on request)
class EventManager (object):
  ## Constructor.
	def __init__(self):
		self.__indexed = False
		self.__events = []
		self.__loadedEvents = {}
		self.__delays = []
		self.scriptDir = "scripts"
		
  ## Hook an event, if one exists.
  #  This fires and event if it exists in the _scripts folder.
  #  @param etype - Event name.
  #  @param data - Information to be sent to the event.
  #  @todo add note about data.
	def hook(self, etype, data=None):
		if self.__indexed == False:
			self.indexEvents()
		
		if etype in self.__events:
			if etype not in self.__loadedEvents:
				Log().debug("Loading event \'%s\' for the first time" % etype)
				module = __import__(self.scriptDir, globals(), locals(), [etype])
				self.__loadedEvents[etype] = module.__dict__[etype].e
			return self.__loadedEvents[etype](self, data)
		
		return None
		
  ## Hook an event after a given delay.
	#  @param delay - Time to wait before hooking the event
  #  @param etype - Event name.
  #  @param data - Information to be sent to the event.
	def hook_delayed(self, delay, etype, data=None):
		if etype in self.__events:
			self.__delays.append([delay,etype,data])
			return True
		return False
		
	## Process the delayed event list
	#  @param timeElapsed - The time passed since last update
	def update(self, timeElapsed):
			completed = []
			for i in range(len(self.__delays)):
				self.__delays[i][0] -= timeElapsed
				if self.__delays[i][0] < 0:
					## hook the event, supplying the data and the time elapsed from the
					## point at which the event was ment to have been called.
					self.hook(self.__delays[i][1],self.__delays[i][2],
						{"delayError":(-self.__delays[i][0]),"passed":self.__delays[i][3]})
					completed.append(self.__delays[i])
					
			for i in completed:
				self.__delays.remove(i)
				
	## Check and index event script files
	#  Searches through given script directory for event script files. If the 
	#  files are in the correct format they are added to the event list used by
	#  hook.
	#  @param scriptDir - Script directory name. Important: This is not a path, 
	#    only the name of the directory.
	def indexEvents(self,scriptDir=None):
		if not scriptDir:
			scriptDir = self.scriptDir
		else:
			if re.search("\\\|/", scriptDir):
				raise Exception("script directory name \'%s\' contains '\\' or '/'" % scriptDir)
			self.scriptDir = scriptDir
		
		longScriptDir = os.path.join(os.getcwd(), scriptDir)
		Log().debug("indexing events in \'" + longScriptDir + "\'")
		
		files = os.listdir(longScriptDir)
		## Regular expression for file names
		reg = re.compile("(?P<eventName>.+)\.py$")
		## Regular expression for event function
		defReg = re.compile("^def *e *\( *\w+, *\w+ *\)")
		for fileName in files:
			match = reg.match(fileName)
			if match and fileName != "__init__.py":
				eventName = match.group("eventName")
				Log().debug("found event file: \'%s\'" % fileName)
				
				## Open the file and check that the event function exists...
				with open(os.path.join(longScriptDir, fileName),'r') as f:
					found = False
					for line in f:
						if defReg.match(line):
							Log().debug("found event function")
							found = True
							self.__events.append(eventName)
							break
					if not found:
						Log().debug("no event function found, ignoring \'%s\'" % eventName)
		
		Log().debug("events: %s" % self.__events)
		self.__indexed = True
		