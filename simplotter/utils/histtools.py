import numpy as np
import hist

def getHist(rootFile, branch, isPass=False):
    """This function imports the histogram under `branch` of the given `rootFile` and returns the `Hist`. 

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        branch (string): branch of the desired histogram in the rootFile (relative to the open directory in the file).
        isPass (bool, optional): if true, take the pass histogram instead of the total
    """    
    if isPass:
        # if pass histogram, insert a "pass_" in the branch path
        pass_branch = branch.split("/")
        pass_branch[-1] = "pass_"+pass_branch[-1]
        pass_branch = "/".join(pass_branch)
        return rootFile[pass_branch].to_hist()
    else:
        return rootFile[branch].to_hist()
    



def histSlice1DFrom2D(inHist, bin, axis=0, axisIsDiscrete=False):
    """
    Takes a 2D histogram as input and returns the histogram slice of `bin` along `axis` as a new 1D histogram.
    It returns the sliced out histogram together with the value or range of the chosen bin along axis.

    Args:
        inHist (hist.Hist): Input 2D histogram from which a slice be taken.
        bin (int): the bin along the given axis that shall be taken.
        axis (int, optional): axis to take the bin from (the axis that is reduced).
    """
    edges = inHist.axes.edges[axis].flatten()
    values = np.take(inHist.values(), [bin], axis=axis).flatten()
    variances = np.take(inHist.variances(), [bin], axis=axis).flatten()
    
    outHist = hist.Hist(inHist.axes[~axis])
    outHist[:] = values

    # if slice is discrete, return the center of the sliced bin
    # else return the edges of the bin
    if axisIsDiscrete:
        slice = round(inHist.axes.centers[axis].flatten()[bin])
    else:
        slice = inHist.axes.edges[axis].flatten()[bin:bin+2]

    return outHist, slice




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