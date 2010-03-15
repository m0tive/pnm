import pnm.logger

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
	# event script...
	ms = data._mouse.getMouseState()
	pnm.logger.Log().debug("<%d,%d,%d> %d" % (ms.X.rel, ms.Y.rel, ms.Z.rel, ms.buttons))
	
	return True
