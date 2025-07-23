import matplotlib.pyplot as plt

from simplotter.plotterfunctions.plot2D import plot2D_
from simplotter.utils.histtools import getHist
from simplotter.utils.plotttools import ColorMap, cmslabel, savefig
from simplotter.utils.markLayers import markLayers

def plotHist2D_(rootFile, plotConfig, directory="plots", nEvents=None, cmsConfig=None, layerPairs=None, which="Sim", saveas="png"):
    
    # load correct histograms
    if which=="pass":
        theHist = getHist(rootFile, "SimPixelTracks/%s" % (which, plotConfig.histname), isPass=True)
    else:
        theHist = getHist(rootFile, "%sPixelTracks/%s" % (which, plotConfig.histname))
    
    # create new figure
    fig, ax = plt.subplots()
    
        # plot the histogram
    plot2D_(theHist, fig, ax, zLabel=plotConfig.getYLabel(which), nEvents=nEvents, logZ=plotConfig.isLogZ, cmap=ColorMap.get(which))

    ax.set_xlabel(plotConfig.xLabel)
    ax.set_ylabel(plotConfig.yLabel)

    # draw the boxes to mark barrel and endcaps plus the dots for used layerPairs
    markLayers(ax, plotConfig, layerPairs=layerPairs)

    # add the CMS label
    if cmsConfig is not None:
        cmslabel(llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])

    # save and show the figure
    savefig("%s/%s_%s.%s" % (directory, plotConfig.plotname, which, saveas))
    plt.show()
    plt.close()



# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

def plotHist2D(rootFile, plotConfig, directory="plots", nEvents=None, cmsConfig=None, 
               layerPairs=None, startingPairs=None, plotSim=True, plotReco=True, saveas="png"):
    """
    Plots a 2D histogram for given PlotConfig.

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        plotConfig (PlotConfig object): This object contains all information specifying the histogram:
                                        histname, xLabel, yLabel, type, ...
        directory (str, optional): directory where to save the plot.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
        cmsConfig (dict, optional): Dictionary containing specifications for the CMS label on top of the plot.
        layerPairs (array, optional): Array of the layer pairs to be marked in the plot. Depends on plotConfig.
        startingPairs (array, optional): Array of the layer pairs to be marked in the plot. Depends on plotConfig.
        plotSim (bool, optional): To enable/disable the plotting of the SimPixelTracks distribution. Depends on plotConfig.
        plotReco (bool, optional): To enable/disable the plotting of the reconstructed PixelTracks used in RecoTracks.
        saveas (str, optional): To decide in which format to save the figure. Default is "png".
    """
    # choose correct set of layerPairs
    layerPairs = startingPairs if plotConfig.useStartingPairs else layerPairs

    if plotSim:
        plotHist2D_(rootFile, plotConfig, directory=directory, nEvents=nEvents, 
                    cmsConfig=cmsConfig, layerPairs=layerPairs, which="Sim", saveas=saveas)
    
    if plotReco:
        for which in ["True", "Fake"]:
            plotHist2D_(rootFile, plotConfig, directory=directory, nEvents=nEvents, 
                        cmsConfig=cmsConfig, layerPairs=layerPairs, which=which, saveas=saveas)