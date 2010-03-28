## @file logger.py
#  @brief A utility class to setup and contain the python %logger.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.logger
#  @brief A utility class to setup and contain the python %logger.

#-------------------------------------------------------------------------------

import logging, logging.handlers
import os, os.path

## A utility class to setup and contain the python %logger.
#  
#  Singleton pattern taken from post on Stackoverflow.com by "modi"
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#  Accessed: 9th March 2010
class Log (object):
  ## Singleton instance
  __inst = None

  ## Singleton constructor
  #  @param cls - reference to Log class
  #  @param kwargs - key word arguments
  def __new__(cls, **kwargs):
    if not cls.__inst:
      cls.__inst = super(Log,cls).__new__(cls)
      inst = cls.__inst
      
      ## Default values for keyword arguments
      inst.__level = "DEBUG"
      inst.__fileName = "pnm.log"
      inst.__maxBytes = 1024 * 512 # 512kB
      inst.__backups = 0
      inst.__streamFormat = "%(filename)s:%(lineno)d : %(levelname)s : %(message)s"
      inst.__fileFormat = "(%(asctime)s) " + inst.__streamFormat
          
      ## Process arguments...
      for k in kwargs:
        if k == "level":
          inst.__level = kwargs[k]
        elif k == "file":
          inst.__fileName = kwargs[k]
        elif k == "maxBytes":
          inst.__maxBytes = kwargs[k]
        elif k == "backups":
          inst.__backups = kwargs[k]
        elif k == "fileFormat":
          inst.__fileFormat = kwargs[k]
        elif k == "streamFormat":
          inst.__streamFormat = kwargs[k]
          
      ## Setup python logger
      inst.__setup()
      
    ## If keywords were passed after creating the singleton warn the user
    elif kwargs:
      cls.__inst.logger.warning("Application arguments not used after creation")
    return cls.__inst
    
  ## Destructor
  def __del__(self):
    print "Log deleted"
    
  ## Create the python logger class
  def __setup(self):
    print "Creating logger with level \"%s\"" % self.__level
    
    self.logger = logging.getLogger("__main_logger__")
    self.logger.setLevel(logging.__dict__[self.__level])

    self.__fHandler = logging.handlers.RotatingFileHandler(
        os.path.join(os.getcwd(), self.__fileName), 
        maxBytes = self.__maxBytes, backupCount = self.__backups)
    self.__fHandler.setFormatter(logging.Formatter(self.__fileFormat))
    self.logger.addHandler(self.__fHandler)

    self.__sHandler = logging.StreamHandler()
    self.__sHandler.setFormatter(logging.Formatter(self.__streamFormat))
    self.logger.addHandler(self.__sHandler)

    self.logger.info("Logger created (and working)")

  def __getattr__(self,name):
    return getattr(self.logger, name)
    
  # Doxygen info for variables
  
  ## @var logger
  #  @brief Python logger
  #
  
  ## @var __fHandler
  #  @brief log-to-file handler
  #
  
  ## @var __sHandler
  #  @brief log-to-stream handler