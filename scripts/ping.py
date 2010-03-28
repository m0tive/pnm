## @file scripts/ping.py
#  @brief Script file, see scripts.ping
#  @author Peter Dodds
#  @version 1.1
#  @date 28/03/10
#  @todo make ncca compliant

## @package scripts.ping
#  @brief A %ping event (for debugging)

#-------------------------------------------------------------------------------

## Event function.
#  @param eman - event manager
#  @param data - information passed
#  @return True if the event is successful
def e (eman, data):
  print "ping"
  
  return True
