## @file eventManager.py
#  @brief 

## Event Manager
class EventManager (object):
	def __init__(self, parent):
			self.parent = parent
			self.__delays = []
			
	def __del__(self):
			pass
			
	def hook(self, etype, maker=None, data=None):
			
			event = __import__("_scripts", globals(), locals(), [etype])
			
			try:
				return event.__dict__[etype].e(self, maker, data)
			except KeyError:
				print ("Event \"" + etype + "\" has no action")
			except:
				print ("Unexpected error")
				raise
			
			return False
			
	def hook_delayed(self, delay, etype, maker=None, data=None):
			self.__delays.append([delay,etype,maker,data])
			
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
