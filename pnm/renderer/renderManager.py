## @file eventManager.py
#  @brief 

import os, os.path
import ogre.renderer.OGRE as ogre
from ..logger import Log


## Render manager.
class RenderManager (object):
	## Constructor.
	def __init__(self,pluginConfg=None):
		if not pluginConfg:
			pluginConfig = os.path.join(os.getcwd(), 'plugins', 'plugins.cfg')
		self.ogreRoot = ogre.Root(pluginConfig)
		
		
	def __del__(self):
		Log().info("RenderManager closing")
		