## @file scripts/agent_chooseNewGoal.py
#  @brief Script file, see scripts.agent_chooseNewGoal

## @package scripts.agent_chooseNewGoal
#  @brief ...

#-------------------------------------------------------------------------------

from pnm.application import Application as App
#from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  
  agent = data["passed"]
  navMesh = agent.getManager().getNavigationMesh()
  tris = navMesh.getTriangles()
  import random
  
  agent.setGoal(random.choice(tris).getCentre())
  
  return True
