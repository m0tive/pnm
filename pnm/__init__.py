## @file __init__.py
#  @brief Main package init file.
#  Contains all other packages and start up function.

## @package pnm
#  @brief Peter's Navigation Mesh pathfinder.
#  An application to demonstrate pathfinding using navigation meshes

from application import *

## Start up function.
#  Run once to start the application.
def run ():
	app = Application(foo="Hello World", bar=3.147)
	print "pnm has run away"
	app2 = Application(foo="hello")

