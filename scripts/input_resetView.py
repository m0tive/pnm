## @file scripts/input_resetView.py
#  @brief Script file, see scripts.input_resetView

## @package scripts.input_resetView
#  @brief Reset the camera's position.
#  This is hooked by a keypress (noramlly HOME) in 
#    pnm.input.inputManager.InputManager.
#  <br> The \c data passed is a reference to inputManager.

#-------------------------------------------------------------------------------

from pnm.application import Application as App
#from pnm.logger import Log

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  cam = App().renderManager.getCamera()
  cam.resetPosition()
  cam.resetOrientation()

  cam.translate(0,100,200)
  
  return True
