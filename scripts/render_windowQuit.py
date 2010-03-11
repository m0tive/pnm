import pnm

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
	pnm.Application().renderManager.quit(True)

	return True
