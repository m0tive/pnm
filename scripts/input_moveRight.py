## @file scripts/input_moveRight.py
#  @brief Script file, see scripts.input_moveRight
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.input_moveRight
#  @brief 

#-------------------------------------------------------------------------------

import pnm
from pnm.logger import Log
import ogre.renderer.OGRE as ogre

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  # event script...
  #pnm.Application().renderManager.getCamera().getNode().translate(
  #    -data.timeElapsed*30,0,0,ogre.Node().TransformSpace().TS_LOCAL)
  
  pnm.Application().renderManager.getCamera().track(x=-data.timeElapsed)
  
  return True
