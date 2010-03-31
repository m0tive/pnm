## @file scripts/render_windowQuit.py
#  @brief Script file, see scripts.render_windowQuit

## @package scripts.render_windowQuit
#  @brief Window quit event.
#  This is hooked by pnm.renderer.renderManager.WindowEventListener.
#  <br> The \c data passed is a reference to the OGRE RenderWindow object

#-------------------------------------------------------------------------------

import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  pnm.Application().renderManager.quit(True)
  
  return True
