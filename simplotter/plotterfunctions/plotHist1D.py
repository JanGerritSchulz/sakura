import matplotlib.pyplot as plt
from simplotter.plotterfunctions.plotDiscreteHist import plotDiscreteHist
from simplotter.plotterfunctions.plotContineousHist import plotContineousHist
from simplotter.utils.plotttools import cmslabel, savefig, legend

def plotHist1D(rootFile, plotConfig, directory="plots", 
                nEvents=None, cmsConfig=None, limitXRange=False, 
                plotSim=True, plotReco=True, saveas="png"):
    """
    Plots a 1D histogram for given PlotConfig. Decides which plotting function to use based on the given plotConfig.type.

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
    """

    # create new figure
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

    # make copy of the axes
    ax1c = ax1.twinx() if (plotSim and plotReco) else ax1
    ax2c = ax2.twinx() if (plotSim and plotReco) else ax2
    axCumSum = ax2.twinx() if plotConfig.plotCumSumReco else None

    # set x axis to log
    if plotConfig.isLogX:
        ax1.set_xscale("log")

    # set y axis to log
    if plotConfig.isLogY:
        ax1.set_yscale("log")
        ax1c.set_yscale("log")
    

    # plot the histograms
    if "discrete" in plotConfig.type:
        # if its a discrete 1D histogram, use plotDiscreteHist
        xLim = plotDiscreteHist(rootFile, plotConfig, axSim=ax1, axReco=ax1c, 
                                axRatioSim=ax2, axRatioReco=ax2c, axCumSumReco=axCumSum,
                                nEvents=nEvents, limitXRange=limitXRange,
                                plotSim=plotSim, plotReco=plotReco)
        
    else:
        # if it's a contineous histogram, use plotContineousHist
        xLim = plotContineousHist(rootFile, plotConfig, axSim=ax1, axReco=ax1c, 
                                axRatioSim=ax2, axRatioReco=ax2c, axCumSumReco=axCumSum,
                                nEvents=nEvents, limitXRange=limitXRange,
                                plotSim=plotSim, plotReco=plotReco)

    # if limit x range
    if limitXRange:
        ax2.set_xlim(xLim)

    # plot legend
    axs = [ax1, ax1c] if (plotReco and plotSim) else [ax1]
    legend(ax1, axs, loc='upper left', bbox_to_anchor=(1.2, 1))
    
    ax1.set_xlabel("")
    ax2.set_xlabel(plotConfig.xLabel)
    ax2.axhline(0, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
    ax2.axhline(1, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
    ax2.set_ylim(-0.15, 1.15)
    ax2c.set_ylim(-0.15, 1.15)
    if axCumSum is not None:
        axCumSum.set_ylim(-0.15, 1.15)
        if (plotSim and plotReco):
            axCumSum.spines['right'].set_position(('outward', 80))
    plt.subplots_adjust(hspace=0.)

    # add the CMS label
    if cmsConfig is not None:
        cmslabel(ax=ax1, llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
    
    # save and show the figure
    savefig("%s/%s.%s" % (directory, plotConfig.plotname, saveas))
    plt.close()