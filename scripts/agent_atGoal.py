## @file scripts/agent_atGoal.py
#  @brief Script file, see scripts.agent_atGoal

## @package scripts.agent_atGoal
#  @brief Agent has arrived at its goal location.
#  This is hooked by pnm.pathfinding.agentManager.AgentManager.__Agent.update
#  <br> The \c data passed is a reference to the __Agent class

#-------------------------------------------------------------------------------

from pnm.application import Application as App
#from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  
  App().eventManager.hook_delayed(4.0,"agent_chooseNewGoal_delayed",data)
  
  return True
