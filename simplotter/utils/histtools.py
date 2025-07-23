import numpy as np

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