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


#-------------------------------------------------------------------------------
## A utility class to setup and contain the python %logger.
#  To create a log entity use the python %logger functions: debug(), info(), 
#    warning(), error() and critical()
#
#  eg:<br> 
#  Log().critical("Houston we have a problem")
#
#  These function calls will then send the log string to the output stream and 
#    to the log file.
#  
#  Singleton pattern taken from post on Stackoverflow.com by "modi"<br>
#  http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern/1810367#1810367
#  <br>Accessed: 9th March 2010
#
#  @see Python logging.logger
class Log (object):

  ## Instance of the singleton class
  __inst = None

  
  #-----------------------------------------------------------------------------
  ## Singleton constructor.
  #  On the first run of Log(), arguments can be passed to setup the %logger 
  #    (subsequent runs will just return a referece to the Log.__inst). The 
  #    class accepts a the following keyword arguments on setup:
  #
  #  \c level - The logging level, one of; DEBUG, INFO, WARNING, ERROR or 
  #    CRITICAL (default, INFO)
  #
  #  \c file - File the log will be output to (default, "pnm.log")
  # 
  #  \c maxBytes - maximum size of the log file before it is swapped/cleared 
  #    (default, 512kB)
  #
  #  \c backups - number of backup files (default, 0)
  #
  #  \c streamFormat - string format for log output to the command prompt 
  #    (default, "%(filename)s:%(lineno)d : %(levelname)s : %(message)s" )
  #
  #  \c fileFormat - string format for log output to file 
  #    (default, "(%(asctime)s) %(filename)s:%(lineno)d : %(levelname)s : 
  #               %(message)s" )
  #  @param cls - reference to Log class.
  #  @param kwargs - key word arguments.
  def __new__(cls, **kwargs):
    if not cls.__inst:
      cls.__inst = super(Log,cls).__new__(cls)
      inst = cls.__inst
      
      ## Default values for keyword arguments
      inst.__level = "INFO"
      inst.__fileName = "pnm.log"
      inst.__maxBytes = 1024 * 512 # 512kB
      inst.__backups = 0
      inst.__streamFormat="%(filename)s:%(lineno)d : %(levelname)s : %(message)s"
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
    
    
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    print "Log deleted"
    
    
  #-----------------------------------------------------------------------------
  ## Create the python %logger class
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

  
  #-----------------------------------------------------------------------------
  ## Get Class Attribute overload. If an attribute is not found
  #    in Log, this redirects the request to Log.logger, 
  #    ie. Log().debug() -> Log().logger.debug()
  def __getattr__(self,name):
    return getattr(self.logger, name)
    
    
  #-----------------------------------------------------------------------------
  # Doxygen info for variables
  
  ## @var logger
  #  @brief Python logger
  
  ## @var __fHandler
  #  @brief log-to-file handler
  
  ## @var __sHandler
  #  @brief log-to-stream handler