## @file math.py
#  @brief Static maths functions contained within a class.
#  @author Peter Dodds
#  @version 1.0
#  @date 28/03/10
#  @todo make ncca compliant

## @package pnm.math
#  @brief Static maths functions contained within a class.

#-------------------------------------------------------------------------------

from .logger import Log

#-------------------------------------------------------------------------------
## Static maths functions contained within a class.
class Math (object):
  @staticmethod
  def distanceToLine(s,p1,p2):
    ## from Wolfram MathWorld (accessed 26/03/10)
    ## http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    return ((s - p1).crossProduct(s - p2)).length() / (p2 - p1).length()
    
  @staticmethod
  def distanceToPlane(s,p,n):
    ## from Wolfram MathWorld (accessed 26/03/10)
    ## http://mathworld.wolfram.com/Point-PlaneDistance.html
    return n.dotProduct(s-p)
    
    
  #-----------------------------------------------------------------------------
  ##
  #  Sime Side Technique from:
  #  http://www.blackpawn.com/texts/pointinpoly/default.html (accessed 29/04/10)
  #  @param _p - OGRE Vector2 point to be tested
  #  @param _t1 - OGRE Vector2 first triangle vertex
  #  @param _t2 - OGRE Vector2 second triangle vertex
  #  @param _t3 - OGRE Vector2 third triangle vertex
  #  @return True if the point is within the triangle
  @staticmethod
  def getPointIn2dTriangle(_p, _t1, _t2, _t3):
    return (  Math.__SameSide2d(_t1, _t2, _t3, _p) and \
              Math.__SameSide2d(_t2, _t3, _t1, _p) and \
              Math.__SameSide2d(_t3, _t1, _t2, _p) )
    
  @staticmethod
  def __SameSide2d(_base, _ref, _p1, _p2):
    v1 = _ref - _base
    cp1 = v1.crossProduct(_p1 - _base)
    cp2 = v1.crossProduct(_p2 - _base)
    
    Log().debug( str(cp1) + " " + str(cp2) )
    
    #return (cp1.dotProduct(cp2) >= 0)
    return ((cp1 * cp2) >= 0) # True if both positive or both negative