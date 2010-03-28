## @file scripts/render_frameStarted.py
#  @brief Script file, see scripts.render_frameStarted
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.render_frameStarted
#  @brief 

#-------------------------------------------------------------------------------

import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  pnm.Application().eventManager.update(data.timeSinceLastFrame)
  pnm.Application().inputManager.update(data.timeSinceLastFrame)
  pnm.Application().agentManager.update(data.timeSinceLastFrame)
  
  return True
