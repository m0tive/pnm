
import logging, logging.handlers
import os, os.path

## Singleton application class
#
#  Singleton pattern taken from post on Stackoverflow.com by "modi"
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#  Accessed: 9th March 2010
class Log (object):
	__inst = None

	logger = None
	__fName = "pnm.log"
	__fHandler = None
	__sHandler = None

	def __new__(cls, **kwargs):
		if not cls.__inst:
			cls.__inst = super(Log,cls).__new__(cls)
		elif kwargs:
			cls.__inst.logger.warning("Application arguments not used after creation")
		return cls.__inst

	def __init__(self, **kwargs):
		level = "debug"
		
		fMaxBytes = 1024 * 512 # 512kB
		fBackups = 0

		fFormat = "(%(asctime)s) %(name)s [%(levelno)s]: %(message)s"
		sFormat = "[%(levelno)s] %(filename)s:%(lineno)d - %(message)s"

		## Process arguments..
		for k in kwargs:
			if k == "file":
				self.__fName = kwargs[k]
			elif k == "maxBytes":
				fMaxBytes = kwargs[k]
			elif k == "backups":
				fBackups = kwargs[k]
			elif k == "fileFormat":
				fFormat = kwargs[k]
			elif k == "streamFormat":
				sFormat = kwargs[k]

		self.logger = logging.getLogger("__main_logger__")
		self.logger.setLevel(logging.DEBUG)

		self.__fHandler = logging.handlers.RotatingFileHandler(
				os.path.join(os.getcwd(), self.__fName), 
				maxBytes = fMaxBytes, backupCount = fBackups)
		self.__fHandler.setFormatter(logging.Formatter(fFormat))
		self.logger.addHandler(self.__fHandler)

		self.__sHandler = logging.StreamHandler()
		self.__sHandler.setFormatter(logging.Formatter(sFormat))
		self.logger.addHandler(self.__sHandler)

		self.logger.debug("Logger created (and working)")

	def __getattr__(self,name):
		return getattr(self.logger, name)

