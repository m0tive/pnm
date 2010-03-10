
from singletonApp import SingletonApp
from logger import Log

## Application class
class Application (SingletonApp):
	def _setup(self):
		super(Application,self)._setup()
		Log().debug("Application setup")
		self.eventManager.hook("application_setup")
		
	def start(self):
		self.eventManager.hook("application_start")