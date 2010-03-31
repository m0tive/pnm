## @file scripts/render_frameStarted.py
#  @brief Script file, see scripts.render_frameStarted

## @package scripts.render_frameStarted
#  @brief FrameStart event hooked just prior to the frame beggining rendering.
#  This is hooked by pnm.renderer.renderManager.FrameListener
#  <br> The \c data passed is a reference to the frameStart event

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
