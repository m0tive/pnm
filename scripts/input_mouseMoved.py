## @file scripts/input_mouseMoved.py
#  @brief Script file, see scripts.input_mouseMoved
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.input_mouseMoved
#  @brief 

#-------------------------------------------------------------------------------

import pnm.logger

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  ms = data.getMouse().getMouseState()
  t = pnm.Application().renderManager.getTimeElapsed()
  #pnm.logger.Log().debug("<%d,%d,%d> %d" % (ms.X.rel, ms.Y.rel, ms.Z.rel, ms.buttons))
  
  '''if ms.buttons & 0b001:
    pnm.Application().renderManager.getCamera().yaw(ms.X.rel*0.001)
    pnm.Application().renderManager.getCamera().pitch(ms.Y.rel*0.001)'''
  
  pnm.Application().renderManager.getCamera().yaw(-ms.X.rel*0.004)
  pnm.Application().renderManager.getCamera().pitch(-ms.Y.rel*0.004)
  
  return True
