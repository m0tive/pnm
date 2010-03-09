## @file eventManager.py
#  @brief 

## Event scripts manager.
#  @todo add an indexing function for the event scripts to speed things up.
#  @todo create a generate script function that creates temp scripts (which 
#  could be wrote to file on request)
class EventManager (object):
  ## Constructor.
  #  @param parent Reference to the object containing the event manager, usually
  #  the application class.
	def __init__(self, parent):
			self.parent = parent
			self.__delays = []
			
  ## Destructor
	def __del__(self):
			pass
			
  ## Hook an event, if one exists.
  #  This fires and event if it exists in the _scripts folder.
  #  @param etype - Event name.
  #  @param data - Information to be sent to the event.
  #  @todo add note about data.
	def hook(self, etype, data=None):
			event = __import__("_scripts", globals(), locals(), [etype])
			
			try:
				return event.__dict__[etype].e(self, data)
			except KeyError:
				print ("Event \"" + etype + "\" has no action")
			except:
				print ("Unexpected error")
				raise
			
			return False
			
  ## Hook an event after a given delay.
	def hook_delayed(self, delay, etype, data=None):
			self.__delays.append([delay,etype,data])
			
	## Process the delayed event list
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
				