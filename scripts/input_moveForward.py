## @file scripts/input_moveForward.py
#  @brief Script file, see scripts.input_moveForward
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.input_moveForward
#  @brief 

#-------------------------------------------------------------------------------

import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  pnm.Application().renderManager.getCamera().track(z=-data.timeElapsed)
  
  return True
