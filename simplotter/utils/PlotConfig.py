class PlotConfig:
    """
    Small class containing all the information for plotting a certain histogram.
    """
    # name of the histogram in the ROOT file
    histname = None
    ratiohistname = None
    # name of the plot and subfolder to save the plot in
    plotname = None
    subfolder = ""
    # label for plots
    xLabel = None
    yLabel = None
    yLabelSim = None
    yLabelReco = None
    zLabel = None
    simSubject = ""
    recoSubject = ""
    # type of the plot: 1D, 2D, discrete1D
    type = None
    # bools
    hasLayerPairsOnX = False
    hasLayerPairsOnY = False
    isLogX = False
    isLogY = False
    isLogZ = True
    isDoublets = False
    isNtuplets = False
    isParticles = False
    useStartingPairs = False
    plotCumSumReco = False
    onlyReco = False
    onlySim = False

    def __init__(self, histname, plotname=None, subfolder="", 
                 type=None, ratiohistname=None,
                 xLabel=None, yLabel=None, zLabel=None, 
                 hasLayerPairsOnX=False, hasLayerPairsOnY=False, hasLayerPairsOnXY=False,
                 isLogX=False, isLogY=False, isLogZ=True, plotCumSumReco=False,
                 isDoublets=False, isNtuplets=False, isParticles=False,
                 useStartingPairs=False, onlyReco=False, onlySim=False
                ):
        self.histname = histname
        self.ratiohistname = ratiohistname
        self.plotname = histname if plotname is None else plotname
        self.subfolder = subfolder
        self.type = type
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.zLabel = zLabel
        self.hasLayerPairsOnX = hasLayerPairsOnX
        self.hasLayerPairsOnY = hasLayerPairsOnY
        if hasLayerPairsOnXY:
            self.hasLayerPairsOnX = True
            self.hasLayerPairsOnY = True
        self.isLogX = isLogX
        self.isLogY = isLogY
        self.isLogZ = isLogZ
        self.useStartingPairs = useStartingPairs
        self.plotCumSumReco = plotCumSumReco
        self.onlyReco = onlyReco
        self.onlySim = onlySim

        if isDoublets:
            self.simSubject = "SimDoublet"
            self.recoSubject = "Doublet"
            self.isDoublets = True
        elif isNtuplets:
            self.simSubject = "SimNtuplet"
            self.recoSubject = "Ntuplet"
            self.isNtuplets = True
        elif isParticles:
            self.simSubject = "TrackingParticle"
            self.recoSubject = "Track"
            self.isParticles = True
        
        if self.type is not None and self.simSubject != "":

            if "1D" in self.type and self.yLabel is None:
                self.yLabel = "#TrackingParticles or #Tracks" if self.isParticles else ("%ss" % self.recoSubject)
                self.yLabelSim = "%ss" % self.simSubject
                self.yLabelReco = "%ss" % self.recoSubject
            elif "2D" in self.type and self.zLabel is None:
                self.zLabel = "#TrackingParticles or #Tracks" if self.isParticles else ("%ss" % self.recoSubject)

    def getYLabelSim(self):
        if self.yLabelSim is not None:
            return self.yLabelSim
        else:
            return self.yLabel

    def getYLabelReco(self):
        if self.yLabelReco is not None:
            return self.yLabelReco
        else:
            return self.yLabel

    def getYLabel(self, which="Sim"):
        if self.isDoublets:
            if which=="Fake":
                return "#RecoDoublets of consecutive\nRecHits from fake tracks"
            elif which=="True":
                return "#RecoDoublets of consecutive\nRecHits from true tracks"
            elif which=="Sim":
                return "#SimDoublets"
        elif self.isParticles:
            if which=="Fake":
                return "#FakePixelTracks"
            elif which=="True":
                return "#TruePixelTracks"
            elif which=="Sim":
                return "#TrackingParticles"
        elif self.isNtuplets:
            if which=="Fake":
                return "#Ntuplets of consecutive\nRecHits from fake tracks"
            elif which=="True":
                return "#Ntuplets of consecutive\nRecHits from true tracks"
            elif which=="Sim":
                return "#TSimNtuplets"