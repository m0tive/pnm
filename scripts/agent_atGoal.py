## @file scripts/agent_atGoal.py
#  @brief Script file, see scripts.agent_atGoal

## @package scripts.agent_atGoal
#  @brief ...

#-------------------------------------------------------------------------------

from pnm.application import Application as App
#from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  
  App().eventManager.hook_delayed(4.0,"agent_chooseNewGoal",data)
  
  return True
