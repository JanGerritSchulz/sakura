from simplotter.plotterfunctions.plotHist1D import plotHist1D
from simplotter.plotterfunctions.plotHist2D import plotHist2D
from simplotter.plotterfunctions.plotRatio2D import plotRatio2D
from simplotter.plotterfunctions.plotProfile import plotProfile
from simplotter.plotterfunctions.plotSimNtuplets import plotSimNtuplets

def plotHistogram(rootFile, plotConfig, directory="plots", 
                  nEvents=None, cmsConfig=None, limitXRange=False, 
                  plotSim=True, plotReco=True, saveas="png",
                  layerPairs=None, startingPairs=None, **kwargs):
    """
    Plots a histogram for given PlotConfig. Decides which plotting function to use based on the given plotConfig.type.

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        plotConfig (PlotConfig object): This object contains all information specifying the histogram:
                                        histname, xLabel, yLabel, type, ...
        directory (str, optional): directory where to save the plot.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
        cmsConfig (dict, optional): Dictionary containing specifications for the CMS label on top of the plot.
        limitXRange (bool, optional): If True, the x range of the plot is tailored to the non-empty bins of the histograms.
        plotSim (bool, optional): To enable/disable the plotting of the SimPixelTracks distribution.
        plotReco (bool, optional): To enable/disable the plotting of the reconstructed PixelTracks used in RecoTracks.
        saveas (str, optional): To decide in which format to save the figure. Default is "png".
        startingPairs (array, optional): Array of the layer pairs to be marked in the plot. Depends on plotConfig.
        plotSim (bool, optional): To enable/disable the plotting of the SimPixelTracks distribution. Depends on plotConfig.
    """
    # overwrite plotSim and plotReco if specified in plotConfig
    plotReco = plotReco and not plotConfig.onlySim
    plotSim = plotSim and not plotConfig.onlyReco

    # plot the histograms
    if "1D" in plotConfig.type:
        # if its a 1D histogram, use plotHist1D
        plotHist1D(rootFile, plotConfig, directory=directory, 
                   nEvents=nEvents, cmsConfig=cmsConfig, limitXRange=limitXRange, 
                   plotSim=plotSim, plotReco=plotReco, saveas=saveas)

    elif "2D" in plotConfig.type:
        if "ratio" in plotConfig.type:
            # if it's a ratio between two histograms, use plotRatio2D
            plotRatio2D(rootFile, plotConfig, directory=directory, nEvents=nEvents, cmsConfig=cmsConfig, 
                        layerPairs=layerPairs, startingPairs=startingPairs, plotSim=plotSim, plotReco=plotReco, saveas=saveas)
        else:
            # if its a 2D histogram, use plotHist2D
            plotHist2D(rootFile, plotConfig, directory=directory, nEvents=nEvents, cmsConfig=cmsConfig, 
                       layerPairs=layerPairs, startingPairs=startingPairs, plotSim=plotSim, plotReco=plotReco, saveas=saveas)
            
    elif "SimNtuplet" in plotConfig.type:
        # if SimNtuplet, use plot SimNtuplets
        plotSimNtuplets(rootFile, plotConfig, directory=directory, cmsConfig=cmsConfig, saveas=saveas)

    elif "profile" in plotConfig.type:
        plotProfile(rootFile, plotConfig, directory=directory, cmsConfig=cmsConfig, plotSim=plotSim, plotReco=plotReco, saveas=saveas)