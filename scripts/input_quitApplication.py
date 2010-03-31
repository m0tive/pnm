## @file scripts/input_quitApplication.py
#  @brief Script file, see scripts.input_quitApplication

## @package scripts.input_quitApplication
#  @brief Exit the application.
#  This is hooked by a keypress (noramlly ESCAPE) in 
#    pnm.input.inputManager.InputManager
#  <br> The \c data passed is a reference to inputManager

#-------------------------------------------------------------------------------

import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  pnm.Application().renderManager.quit(True)
  
  return True
