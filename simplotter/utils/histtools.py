import numpy as np

def getHist(ROOTfile, branch):
    """This function imports the histogram under `branch` of the given `ROOTfile` and returns the `Hist`. 

    Args:
        ROOTfile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        branch (string): branch of the desired histogram in the ROOTfile (relative to the open directory in the file).
    """    
    return ROOTfile[branch].to_hist()


def findXLimits(histogram, log=False):
    """
    Finds the x range that fully covers the given histogram.
    """
    values = histogram.values()
    edges = histogram.axes.edges[0]
    # if histogram is empty return None
    if np.sum(values) <= 0:
        return (None, None)
    # else find the best edges
    else:
        mask = values > 0
        xMin = edges[:-1][mask][0]
        xMax = edges[1:][mask][-1]
        if log:
            factor = 10 ** (np.log10(xMax / xMin) / 20 *0.75)
            return (xMin/factor, xMax*factor)
        else:
            dxMin = dxMax = (xMax-xMin) / 20 *0.75
            return (xMin-dxMin, xMax+dxMax)