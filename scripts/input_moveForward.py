## @file scripts/input_moveForward.py
#  @brief Script file, see scripts.input_moveForward

## @package scripts.input_moveForward
#  @brief Move the camera forward (negative in the z-axis).
#  This is hooked by a keypress in pnm.input.inputManager.InputManager
#  <br> The \c data passed is a reference to inputManager

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
