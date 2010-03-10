
from logger import Log
from events import EventManager

## Singleton application class
#
#  Singleton pattern taken from post on Stackoverflow.com by "modi"
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#  Accessed: 9th March 2010
class Application (object):
	__inst = None
	
	def __new__(cls, **kwargs):
		if not cls.__inst:
			cls.__inst = super(Application,cls).__new__(cls)
			## Initialise log and send info message
			Log(level="DEBUG").info("Application instance created")
			cls.__inst.__setup()
		elif kwargs:
			Log().warning("Application arguments not used after creation")
		return cls.__inst
		
	def __setup(self):
		## run setup...
		
		self.eventManager = EventManager()
		self.eventManager.hook("ping")
		self.eventManager.hook("ping")
		#self.eventManager.indexEvents()
	
		Log().info("Application setup")
		
	def start(self):
		Log().debug("Starting Application")