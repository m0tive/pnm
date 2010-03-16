import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
	# event script...
	pnm.Application().renderManager.getCamera().track(y=data.timeElapsed)
	
	return True
