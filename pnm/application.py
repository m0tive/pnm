
from singletonApp import SingletonApp
from logger import Log

from renderer.renderManager import RenderManager

## Application class
class Application (SingletonApp):
	def _setup(self):
		super(Application,self)._setup()
		
		self.renderManager = RenderManager()
		
		Log().debug("Application setup")
		self.eventManager.hook("application_setup")
		
	def start(self):
		self.eventManager.hook("application_start")
		
	def close(self):
		del self.renderManager
		Log().info("Application closed")
		
		## close the parent application
		super(Application,self).close()