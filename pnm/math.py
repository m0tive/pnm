

## 
class Math (object):
  @staticmethod
  def distanceToLine(s,p1,p2):
    ## from Wolfram MathWorld (accessed 26/03/10)
    ## http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
    return ((s - p1).crossProduct(s - p2)).length() / (p2 - p1).length()