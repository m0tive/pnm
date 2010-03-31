## @file scripts/input_moveLeft.py
#  @brief Script file, see scripts.input_moveLeft

## @package scripts.input_moveLeft
#  @brief Move the camera left (positive in the x-axis).
#  This is hooked by a keypress in pnm.input.inputManager.InputManager
#  <br> The \c data passed is a reference to inputManager

#-------------------------------------------------------------------------------

from pnm.application import Application as App
from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  #pnm.Application().renderManager.getCamera().getNode().translate(
  #    data.timeElapsed*30,0,0)
  
  App().renderManager.getCamera().track(x=data.timeElapsed)
  
  return True
