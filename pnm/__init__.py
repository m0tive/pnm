## @file pnm/__init__.py
#  @brief Package init file
#  Contains all other packages and start up function.

## @package pnm
#  @brief Peter's Navigation Mesh pathfinder package.
#  An %application to demonstrate %pathfinding using navigation meshes

#-------------------------------------------------------------------------------


from application import *


#-------------------------------------------------------------------------------
## Start up function.
#  Run once to start the %application.
def run ():
  Application().start()
  
  # ...
  
  Application().close()
