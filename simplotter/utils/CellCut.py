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
    yLabel = ""
    # type of the cut plus limits: "min", "max" or "both"
    type = None
    min = -np.inf
    max = np.inf
    # bools
    isDoubletCut = False
    isTripletCut = False
    isQuadrupletCut = False
    isStartingCut = False
    isFishbone = False
    isLayerDependent = False
    isLog = False
    isLogY = False
    isLogZ = False
    is2D = False
    # layerIds
    innerLayer = None
    outerLayer = None
    # for 2D cuts: function
    cutFunc = lambda x : None

    def __init__(self, histname, min=-np.inf, max=np.inf, 
                 label="", cutLabelAddition="", yLabelAddition="", yLabel="",
                 isLog=False, isLogY=False, isLogZ=False,
                 isDoubletCut=False, isStartingCut=False,
                 isTripletCut=False, isQuadrupletCut=False,
                 isFishbone=False,
                 isLayerDependent=False, innerLayer=None, outerLayer=None,
                 cutFunc = None
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
        self.isTripletCut = isTripletCut
        self.isQuadrupletCut = isQuadrupletCut
        self.isStartingCut = isStartingCut
        self.isFishbone = isFishbone
        self.isLayerDependent = True if (innerLayer is not None) else isLayerDependent
        self.isLog = isLog
        self.isLogY = isLogY
        self.isLogZ = isLogZ
        self.innerLayer = innerLayer
        self.outerLayer = outerLayer
        if cutFunc is not None:
            self.cutFunc = cutFunc
            self.is2D = True
            self.yLabel = yLabel

        
    def func2D(self, x):
        if self.cutFunc[0] == "linear":
            return self.cutFunc[1]*x + self.cutFunc[2]
        else:
            return 0*x