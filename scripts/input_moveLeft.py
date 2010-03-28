## @file scripts/input_moveLeft.py
#  @brief Script file, see scripts.input_moveLeft
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.input_moveLeft
#  @brief 

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
