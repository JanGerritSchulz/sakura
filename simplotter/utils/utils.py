import matplotlib.pyplot as plt
import numpy as np

def split_scientificNotation(n):
    a = '%E' % n
    return float(a.split('E')[0].rstrip('0').rstrip('.')), int(a.split('E')[1])
    
def valToLatexStr(val):
    """
    Transforms a given float/int value into a nice Latex string representation.
    E.g.:
      100000 => "10^{5}"
      5.0 => "5"
      2.3 => "2.3"
      0.134 => "0.13"
      0.00735 => "7.35 \times 10^{-3}"
    """
    # option 1: int or large float
    if isinstance(val, int) or val.is_integer() or (val>100):
        if abs(val) < 10000:
            valStr = "%i" % int(val)
        else:
            coefficient, exponent = split_scientificNotation(val)
            if (coefficient).is_integer():
                valStr = "%i" % coefficient
                if valStr == "1":
                    return r"10^{" + str(exponent) + r"}"
                elif valStr == "-1":
                    return r"-10^{" + str(exponent) + r"}"
            elif (coefficient*10).is_integer():
                valStr = "%.1f" % coefficient
            else:
                valStr = "%.2f" % coefficient
            
            valStr += r"\times 10^{" + str(exponent) + r"}" 
    
    # option 2: float close or larger than 1
    elif abs(val) >= 0.1:
        if (val*10).is_integer():
            valStr = "%.1f" % val
        else:
            valStr = "%.2f" % val

    # option 3: small float
    else:
        coefficient, exponent = split_scientificNotation(val)
        if (coefficient).is_integer():
            valStr = "%i" % coefficient
            if valStr == "1":
                return r"10^{" + str(exponent) + r"}"
            elif valStr == "-1":
                return r"-10^{" + str(exponent) + r"}"
        elif (coefficient*10).is_integer():
            valStr = "%.1f" % coefficient
        else:
            valStr = "%.2f" % coefficient

        valStr += r"\times 10^{" + str(exponent) + r"}" 

    return valStr


def limitNone(a,b, func):
    if (a is None) and (b is None):
        return None
    elif (a is None):
        return b
    elif (b is None):
        return a
    else:
        return func(a,b)



def limitXNone(xLim1, xLim2):
    return (limitNone(xLim1[0], xLim2[0], min), limitNone(xLim1[1], xLim2[1], max))


def toRGBA(hex, alpha=1):
    """
    Takes a color in hex format "#XXXXXX" and transforms it to the rgb format with alpha.
    E.g.:
    #FF0000 + alpha=0.5 -> (1, 0, 0, 0.5)
    """
    r,g,b = tuple(int(hex[i:i+2], 16)/255 for i in (1, 3, 5))
    return (r,g,b,alpha)