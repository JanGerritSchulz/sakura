import numpy as np

class CellCut:
    """
    Small class containing all the information about a certain doublet/connection cut.
    """
    # name of the histogram in the ROOT file
    histname = None
    # label for plots
    label = ""
    cutLabelAddition = ""
    yLabelAddition = ""
    # type of the cut plus limits: "min", "max" or "both"
    type = None
    min = -np.inf
    max = np.inf
    # bools
    isDoubletCut = False
    isConnectionCut = False
    isLayerDependent = False
    isLog = False
    # layerIds
    innerLayer = None
    outerLayer = None

    def __init__(self, histname, min=-np.inf, max=np.inf, 
                 label="", cutLabelAddition="", yLabelAddition="", isLog=False,
                 isDoubletCut=False, isConnectionCut=False, isLayerDependent=False,
                 innerLayer=None, outerLayer=None
                ):
        if (max == np.inf) and (min == -np.inf):
            self.type = None
        elif (max == np.inf):
            self.type = "min"
        elif (min == -np.inf):
            self.type = "max"
        else:
            self.type = "both"
        self.min = min
        self.max = max
        self.name = None
        self.label = label
        self.cutLabelAddition = cutLabelAddition
        self.yLabelAddition = yLabelAddition
        self.histname = histname
        self.isDoubletCut = isDoubletCut
        self.isConnectionCut = isConnectionCut
        self.isLayerDependent = True if (innerLayer is not None) else isLayerDependent
        self.isLog = isLog
        self.innerLayer = innerLayer
        self.outerLayer = outerLayer