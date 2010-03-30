## @file inputManager.py
#  @brief Input manager processing ogre and OIS inputs.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.input.inputManager
#  @brief Input manager processing ogre and OIS inputs.

#-------------------------------------------------------------------------------


import ogre.io.OIS as OIS
from ..logger import Log
from ..application import Application as App

import ogre.renderer.OGRE as ogre
import re


#-------------------------------------------------------------------------------
## Input manager processing ogre and OIS inputs.
#  Keyboard and Mouse input are processed
class InputManager (object):
  
  #---------------------------------------------------| Start Nested Classes |--
  
  #-----------------------------------------------------------------------------
  ## Mouse event listener derived from the OIS.MouseListener
  class __MouseListener(OIS.MouseListener):
    
    #---------------------------------------------------------------------------
    ## Constructor
    #  @param _mouse - OIS.Mouse object
    def __init__(self, _mouse):
      OIS.MouseListener.__init__(self)
      
      ## The OIS mouse object
      self.__mouse = _mouse
      
      
    #---------------------------------------------------------------------------
    ## Get the OIS mouse object
    #  @return The OIS mouse object
    def getMouse(self):
      return self.__mouse
      
     
    #---------------------------------------------------------------------------
    ## Mouse move event.
    #  inherited from OIS.MouseListener
    #  @param evt - Event data
    def mouseMoved(self,evt):
      App().eventManager.hook("input_mouseMoved",self)
      
      
    #---------------------------------------------------------------------------
    ## Mouse pressed event.
    #  inherited from OIS.MouseListener
    #  @param evt - Event data
    #  @param button - Mouse button pressed
    def mousePressed(self,evt,button):
      App().eventManager.hook("input_mousePressed",self)
      
      
    #---------------------------------------------------------------------------
    ## Mouse released event.
    #  inherited from OIS.MouseListener
    #  @param evt - Event data
    #  @param button - Mouse button pressed
    def mouseReleased(self,evt,button):
      App().eventManager.hook("input_mouseReleased",self)
      
  #-----------------------------------------------------| End Nested Classes |--
  
  
  # InputManager continued...
  
  #-----------------------------------------------------------------------------
  ## Constructor
  def __init__(self):
    ## OIS (python) input system
    self.system = None
    ## Time elapsed since last update
    #  @see InputManager.update
    self.timeElapsed = 0
    
    ## Flag to prevent setup running twice
    #  @see InputManager.setup
    self.__setup = False
    ## Keyboard input object
    self.__keyb = False
    ## Mouse input object
    self.__mous = False
    ## Mouse event listener
    #  @see InputManager.__MouseListener
    self.__mouseListener = None
    ## Keyboard input maps
    self.__keyMaps = {}
    ## Currently active keyboard maps' names
    self.__activeMaps = []
    ## Currently pressed keys
    self.__keyDownMap = [False] * 256
    
    
  #-----------------------------------------------------------------------------
  ## Destructor
  def __del__(self):
    Log().info("InputManager deleted")
    
    
  #-----------------------------------------------------------------------------
  ## Safe shutdown and dereference of variables.
  #  This stops circular references stopping the garbage collection
  def close(self):
    del self.__mouseListener
    Log().info("InputManager closed")
    
    
  #-----------------------------------------------------------------------------
  ## Setup input systems
  #  Only run once
  def setup(self):
    if self.__setup:
      raise Exception ("InputManager.setup(...) run twice")
    self.__setup = True
    
    # From the ogre demo Simple Application.
    # I assume it fixes an issue on 64bit computers...
    import platform
    int64 = False
    for bit in platform.architecture():
        if '64' in bit:
            int64 = True
    if int64:
        windowHnd = App().renderManager.window.getCustomAttributeUnsignedLong("WINDOW")
    else:
        windowHnd = App().renderManager.window.getCustomAttributeInt("WINDOW")
    
    params = [("WINDOW",str(windowHnd)),
        ("w32_keyboard","DISCL_FOREGROUND"),
        ("w32_keyboard", "DISCL_NONEXCLUSIVE"),
        ("x11_keyboard_grab", "false"),
        ("w32_mouse","DISCL_FOREGROUND"),
        ("w32_mouse", "DISCL_EXCLUSIVE"),
        ("x11_mouse_grab", "true"),
        ("x11_mouse_hide", "true")]
    self.system = OIS.createPythonInputSystem( params )
    self.__keyb = self.system.createInputObjectKeyboard(OIS.OISKeyboard, False)
    self.__mous = self.system.createInputObjectMouse(OIS.OISMouse, True)
    
    self.__mouseListener = self.__MouseListener(self.__mous)
    self.__mous.setEventCallback(self.__mouseListener)
    
    self.__setupKeyboard()
    #Log().debug("%s" % (self.__keyDownMap))
    
    
  #-----------------------------------------------------------------------------
  ## Load a keyboard map.
  #  Keyboard maps are stored using the ogre config file, with a slight 
  #  extention.
  #
  #  example:
  #
  #  -----------------------------------<br />
  #  [Global]  <br />
  #  r-LSHIFT+ESCAPE=exit  <br />
  #  p-SPACE=jumpLeft  <br />
  #  h-CONTROL+Z=run  <br />
  #  -----------------------------------
  #
  #  The line 1 declares the map name. Each of the following lines declares a 
  #  new key combo %input untill the next map name. Each combo has three parts:
  #
  #  [type]-[key]=[event]
  # 
  #  type; p - pressed, h - hold, r - released  <br />
  #  key; keys, using the OIS names (minus "KC_"), joined with "+". In the case
  #    of CONTROL and SHIFT, the combo is replaced with two seperate combos 
  #    with both left and right keys in.  <br />
  #  event; the event name passed to pnm.events.eventManager.EventManager.hook
  # 
  #  Note: Each combo can only contain one of each keys.
  #  
  #  @param keyboardConfig - Keyboard config file name
  def __setupKeyboard(self,keyboardConfig="keyboard.cfg"):
    Log().debug("Loading keyboard map")
    
    config = ogre.ConfigFile()
    config.load(keyboardConfig) # load the maps
    
    sectionIterator = config.getSectionIterator()
    typeSplit = re.compile('-') # to split type from keys
    keySplit = re.compile('\+') # to split combined keys
    while sectionIterator.hasMoreElements():
      name = sectionIterator.peekNextKey()
      section = sectionIterator.getNext()
      if name == '': # if the keymap has no name, skip
        continue
      Log().debug("Config group \'%s\'" % name)
      kMap = {'p':[], 'r':[], 'h':[]}
      for item in section:
        Log().debug("Config item key=\'%s\' value=\'%s\'" % (item.key, item.value))
        errorStr = "Repeated keys in keymap \'%s\': \'%s\'" % (name, item.key)
        
        eventType = typeSplit.split(item.key) # get the event type
        Log().debug("Processing type=\'%s\'" % eventType)
        keys = keySplit.split(eventType[1]) # split the keys up
        eventType = eventType[0]
        
        Log().debug("Processing type=%s keys=\'%s\'" % (eventType, keys))
        shift = None
        ctrl = None
        # fix shifts and controls
        # @todo fix bug in control and shift replacement
        for i in range(len(keys)):
          if keys[i] == "SHIFT": # replace SHIFT
            shift = i
            if "LSHIFT" in keys:
              if "RSHIFT" in keys:
                raise Exception (errorStr)
              else:
                keys[i] = "RSHIFT"
            else:
              keys[i] = "LSHIFT"
          if keys[i] == "CONTROL": # replace CONTROL
            ctrl = i
            if "LCONTROL" in keys:
              if "RCONTROL" in keys:
                raise Exception (errorStr)
              else:
                keys[i] = "RCONTROL"
            else:
              keys[i] = "LCONTROL"
        
        # add matching RSHIFT and/or RCONTROL if needed.
        if shift != None and "RSHIFT" in keys:
          keys[shift] = "RSHIFT"
          kMap[eventType].append([keys,item.value])
        if ctrl != None and "RCONTROL" not in keys:
          keys[ctrl] = "RCONTROL"
          kMap[eventType].append([keys,item.value])
        
        # check for repeating keys, and preppend "KC_" for OIS
        for i in range(len(keys)):
          if keys.count(keys[i]) != 1:
            raise Exception (errorStr)
          keys[i] = OIS.__dict__["KC_" + keys[i]]
        
        Log().debug("Split key: " + str(keys))
        kMap[eventType].append([keys,item.value])
        
      Log().debug("Map: " + str(kMap['p']))
      if name in self.__keyMaps:
        self.__keyMaps[name][0].extend(kMap['p'])
        self.__keyMaps[name][1].extend(kMap['r'])
        self.__keyMaps[name][2].extend(kMap['h'])
      else:
        self.__keyMaps[name] = []
        self.__keyMaps[name].append(kMap['p'])
        self.__keyMaps[name].append(kMap['r'])
        self.__keyMaps[name].append(kMap['h'])
        if (name == "Global") and ("Global" not in self.__activeMaps):
          self.__activeMaps.append("Global")
        
    Log().debug("Loaded maps: " + str(self.__keyMaps))
    
    
  #-----------------------------------------------------------------------------
  ## Process inputs
  #  @param timeElapsed - Time since last update
  def update(self,timeElapsed):
    self.timeElapsed = timeElapsed
    
    self.__keyb.capture()
    self.__mous.capture()
    
    for i in range(len(self.__keyDownMap)):
      if self.__keyb.isKeyDown(OIS.KeyCode(i)):
        if not self.__keyDownMap[i]:
          self.__keyDownMap[i] = True
          self.__checkKey(i,0)
          App().eventManager.hook("input_keyPressed",i)
        self.__checkKey(i,2)
        App().eventManager.hook("input_keyHold",i)
      elif self.__keyDownMap[i]:
        self.__keyDownMap[i] = False
        self.__checkKey(i,1)
        App().eventManager.hook("input_keyReleased",i)
    
    
  #-----------------------------------------------------------------------------
  ## Check if a key is in a given state, and run it's event
  #  @param key - Key, in OIS format, to check
  #  @param itype - Input type, 0 - pressed, 1 - released, 2 - held down
  def __checkKey(self,key,itype):
    for name in self.__activeMaps: ## for current maps
      for keySet in self.__keyMaps[name][itype]: # look through each key set
        for k in keySet[0]: # get in individual keys
          if k == key: # and check if they are the same as 'key'
            good = True
            #Log().debug("got 1: t%d %s" % (itype,k))
            for sib in keySet[0]: # now check the rest of the keys in the set
              if (sib != k) and not self.__keyDownMap[sib]:
                good = False
                break # stop checking
            if good: # if all the set are down
              #Log().debug("Hit t%d %s" % (itype,keySet))
              App().eventManager.hook(keySet[1],self)
              #break # I think we should carry on looking...
