## @file scripts/input_moveDown.py
#  @brief Script file, see scripts.input_moveDown

## @package scripts.input_moveDown
#  @brief Move the camera down (negative in the y-axis).
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
  pnm.Application().renderManager.getCamera().track(y=-data.timeElapsed)
  
  return True
