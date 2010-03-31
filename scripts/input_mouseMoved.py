## @file scripts/input_mouseMoved.py
#  @brief Script file, see scripts.input_mouseMoved

## @package scripts.input_mouseMoved
#  @brief Move movement event.
#  This is hooked by 
#    pnm.input.inputManager.InputManager.__MouseListener.mouseMoved 
#  <br> The \c data passed is a reference to the OIS mouse input object.

#-------------------------------------------------------------------------------

import pnm.logger

#-------------------------------------------------------------------------------
## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  ms = data.getMouse().getMouseState()
  t = pnm.Application().renderManager.getTimeElapsed()
  
  pnm.Application().renderManager.getCamera().yaw(-ms.X.rel*0.004)
  pnm.Application().renderManager.getCamera().pitch(-ms.Y.rel*0.004)
  
  return True
