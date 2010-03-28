## @file scripts/render_windowQuit.py
#  @brief Script file, see scripts.render_windowQuit
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.render_windowQuit
#  @brief 

#-------------------------------------------------------------------------------

import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  pnm.Application().renderManager.quit(True)
  
  return True
