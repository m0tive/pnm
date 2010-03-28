## @file scripts/input_resetView.py
#  @brief Script file, see scripts.input_resetView
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.input_resetView
#  @brief 

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
