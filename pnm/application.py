
from events import eventManager
from logger import *

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
		elif kwargs:
			Log().warning("Application arguments not used after creation")
		return cls.__inst

	def __init__(self, **kwargs):
		Log(level="debug")
		for k in kwargs:
			if k == "foo":
				Log().warning("Hello World :3")
				
