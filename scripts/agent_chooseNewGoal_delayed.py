## @file scripts/agent_chooseNewGoal_delayed.py
#  @brief Script file, see scripts.agent_chooseNewGoal_delayed

## @package scripts.agent_chooseNewGoal_delayed
#  @brief Agent has should choose a new goal location.
#  This is a delayed event, setup in agent_atGoal
#  <br> The \c data passed is a reference to the __Agent class

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
