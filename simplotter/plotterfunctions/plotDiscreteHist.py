import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from simplotter.utils.histtools import getHist, findXLimits
from simplotter.utils.plotttools import Colors
from simplotter.utils.utils import limitXNone, toRGBA
from simplotter.plotterfunctions.plotRatio import plotRatioEfficiency

def plotDiscreteHistSim(rootFile, plotConfig, ax=None, axRatio=None, nEvents=None, plotReco=True):
    """
    Plot a given discrete 1D histogram of sim objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    # get total and pass histograms
    histTotal = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname))
    histPass  = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname), isPass=True)

    # x positions + widths (if reco is also plotted, shifted to left + half the width)
    w = histTotal.axes.widths[0] / (6 if plotReco else 3)
    x = histTotal.axes.centers[0] - (w if plotReco else 0)
    xTotal = x - w/2
    xPass  = x + w/2

    ax.bar(xTotal, histTotal.values(), w, yerr=np.sqrt(histTotal.variances()), color=Colors.total, label="%ss (all)" % plotConfig.simSubject)
    ax.bar(xPass, histPass.values(), w, yerr=np.sqrt(histPass.variances()), color=Colors.passed, 
           label="Simulated particles (w/ alive SimNtuplet)" if plotConfig.isParticles else "%ss (pass all cuts)" % plotConfig.simSubject)

    # scale according to number of events if given
    if nEvents is not None:
        ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/nEvents))
        ax.yaxis.set_major_formatter(ticks)
        
    # set fix axes   
    ax.set_ylabel(plotConfig.getYLabelSim() + ("" if nEvents is None else " / event"))
    
    # plot the ratio if wanted
    if axRatio is not None:
        if histTotal.sum() > 0:
            plotRatioEfficiency(histPass, histTotal, ax=axRatio, fmt=".", color=Colors.passed)
        axRatio.set_ylabel("%s\nefficiency" % plotConfig.simSubject, fontsize="x-small", color=Colors.passed)

    return findXLimits(histTotal, log=ax.get_xscale() == "log"), histTotal.axes.centers[0]


def plotDiscreteHistReco(rootFile, plotConfig, ax=None, axRatio=None, axCumSum=None, nEvents=None, plotSim=True):
    """
    Plot a given discrete 1D histogram of reco objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    # get total and pass histograms
    histTrue = getHist(rootFile, "TruePixelTracks/%s" % (plotConfig.histname))
    histFake = getHist(rootFile, "FakePixelTracks/%s" % (plotConfig.histname))

    # x positions + widths (if reco is also plotted, shifted to left + half the width)
    w = histTrue.axes.widths[0] / (6 if plotSim else 3)
    x = histTrue.axes.centers[0] + (w if plotSim else 0)
    xTrue = x - w/2
    xFake = x + w/2

    alpha = 0.25
    ax.bar(xTrue, histTrue.values(), w, yerr=np.sqrt(histTrue.variances()), edgecolor=Colors.true, facecolor=toRGBA(Colors.true,alpha),
           label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
    ax.bar(xFake, histFake.values(), w, yerr=np.sqrt(histFake.variances()), edgecolor=Colors.fake, facecolor=toRGBA(Colors.fake,alpha), 
           label="fake PixelTracks" if plotConfig.isParticles else ("%ss of fake PixelTracks" % plotConfig.recoSubject))

    # scale according to number of events if given
    if nEvents is not None:
        ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/nEvents))
        ax.yaxis.set_major_formatter(ticks)
        
    # set fix axes    
    ax.set_ylabel(plotConfig.getYLabelReco() + ("" if nEvents is None else " / event"))
    
    # plot the ratio if wanted
    if axRatio is not None:
        if (histTrue+histFake).sum() > 0:
            plotRatioEfficiency(histFake, histTrue+histFake, ax=axRatio, fmt=".", color=Colors.fake)

        axRatio.set_ylabel("Reco%s\nfake rate" % plotConfig.recoSubject, fontsize="x-small", color=Colors.fake)

    if axCumSum is not None:
        axCumSum.errorbar(histTrue.axes.centers[0], histTrue.values().cumsum() / histTrue.sum(), xerr=histTrue.axes.widths[0]/2, fmt="+", color=Colors.true, linewidth=0.75)
        axCumSum.set_ylabel("Cum. sum of\ntrue Reco%ss" % plotConfig.recoSubject, fontsize="x-small", color=Colors.true)

    return findXLimits(histTrue, log=ax.get_xscale() == "log"), histTrue.axes.centers[0]



# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

def plotDiscreteHist(rootFile, plotConfig, axSim=None, axReco=None, 
                     axRatioSim=None, axRatioReco=None, axCumSumReco=None, 
                     nEvents=None, limitXRange=False,
                     plotSim=True, plotReco=True):
    """
    Plots a discrete 1D histogram for given PlotConfig.

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        plotConfig (PlotConfig object): This object contains all information specifying the histogram:
                                        histname, xLabel, yLabel, type, ...
        axSim (plt.ax, optional): The plt axes to plot the sim histogram on.
        axReco (plt.ax, optional): The plt axes to plot the reco histogram on.
        axRatioSim (plt.ax, optional): The plt axes to plot the sim ratio on.
        axRatioReco (plt.ax, optional): The plt axes to plot the reco ratio on.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
        limitXRange (bool, optional): If True, the x range of the plot is tailored to the non-empty bins of the histograms.
        plotSim (bool, optional): To enable/disable the plotting of the SimPixelTracks distribution.
        plotReco (bool, optional): To enable/disable the plotting of the reconstructed PixelTracks used in RecoTracks.
    """
    # load SimPixelTracks if wanted
    if plotSim:
        xLim1, x = plotDiscreteHistSim(rootFile, plotConfig, ax=axSim, axRatio=axRatioSim, nEvents=nEvents, plotReco=plotReco)
    else:
        xLim1 = (None, None)

    # load RecoPixelTracks if wanted
    if plotReco:
        xLim2, x = plotDiscreteHistReco(rootFile, plotConfig, ax=axReco, axRatio=axRatioReco, axCumSum=axCumSumReco, nEvents=nEvents, plotSim=plotSim)
    else:
        xLim2 = (None, None)

    # find the axes
    if (axSim is None) and (axReco is None):
        ax = plt.gca()
    else:
        ax = axSim if axSim is not None else axReco

    if (axRatioSim is None) and (axRatioReco is None):
        ax2 = ax
    else:
        ax2 = axSim if axRatioSim is not None else axRatioReco
        
    # if limit x range
    xLim = limitXNone(xLim1, xLim2)
    if limitXRange:
        ax.set_xlim(xLim)
        
    # fix x axis ticks
    maskX = (x < ax.get_xlim()[1])
    stride = 1 + int(maskX.sum() / 15)
    for ax_ in [axSim, axReco, axRatioReco, axRatioSim]:
        if ax_ is not None:
            ax_.xaxis.set_tick_params(which='minor',bottom=False,top=False)

    ax2.set_xticks(x[maskX], [(str(int(x[i_])) if (i_%stride==0) else "") for i_ in np.arange(len(maskX))[maskX]])

    return xLim