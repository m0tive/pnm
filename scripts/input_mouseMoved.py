import pnm.logger

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
	# event script...
	ms = data._mouse.getMouseState()
	t = pnm.Application().renderManager.getTimeElapsed()
	#pnm.logger.Log().debug("<%d,%d,%d> %d" % (ms.X.rel, ms.Y.rel, ms.Z.rel, ms.buttons))
	
	"""if ms.buttons & 0b001:
		pnm.Application().renderManager.getCamera().yaw(ms.X.rel*0.001)
		pnm.Application().renderManager.getCamera().pitch(ms.Y.rel*0.001)"""
	
	pnm.Application().renderManager.getCamera().yaw(-ms.X.rel*0.001)
	pnm.Application().renderManager.getCamera().pitch(-ms.Y.rel*0.001)
	
	return True
