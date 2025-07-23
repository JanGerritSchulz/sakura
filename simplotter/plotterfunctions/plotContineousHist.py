import matplotlib.pyplot as plt
import matplotlib as mpl
from simplotter.utils.histtools import getHist, findXLimits
from simplotter.utils.plotttools import Colors
from simplotter.utils.utils import limitXNone, toRGBA
from simplotter.plotterfunctions.plotRatio import plotRatioEfficiency

def plotContineousHistSim(rootFile, plotConfig, ax=None, axRatio=None, nEvents=None):
    """
    Plot a given contineous 1D histogram of sim objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    # get total and pass histograms
    histTotal = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname))
    histPass  = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname), isPass=True)

    histPass.plot1d(ax=ax, histtype="fill", hatch='//', facecolor="w", edgecolor=Colors.passed,  
                    label="TrackingParticles (w/ alive SimNtuplet)" if plotConfig.isParticles else "%ss (pass all cuts)" % plotConfig.simSubject % plotConfig.simSubject)
    histPass.plot1d(ax=ax, histtype="step",color=Colors.passed, linewidth=2,
                    label="TrackingParticles (w/ alive SimNtuplet)" if plotConfig.isParticles else "%ss (pass all cuts)" % plotConfig.simSubject % plotConfig.simSubject)
    histTotal.plot1d(ax=ax, histtype="step", label="%ss (all)" % plotConfig.simSubject, color=Colors.total, linewidth=2)

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


def plotContineousHistReco(rootFile, plotConfig, ax=None, axRatio=None, axCumSum=None, nEvents=None):
    """
    Plot a given contineous 1D histogram of reco objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    # get total and pass histograms
    histTrue = getHist(rootFile, "TruePixelTracks/%s" % (plotConfig.histname))
    histFake = getHist(rootFile, "FakePixelTracks/%s" % (plotConfig.histname))

    alpha = 0.25
    histTrue.plot1d(ax=ax, histtype="fill", facecolor=toRGBA(Colors.true,alpha),
                    label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
    histTrue.plot1d(ax=ax, histtype="step", color=Colors.true, linestyle="dashed",
                    label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
    histFake.plot1d(ax=ax, histtype="fill", facecolor=toRGBA(Colors.fake,alpha),
                    label="fake PixelTracks" if plotConfig.isParticles else ("%ss of fake PixelTracks" % plotConfig.recoSubject))
    histFake.plot1d(ax=ax, histtype="step", color=Colors.fake, linestyle="dashed",
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

def plotContineousHist(rootFile, plotConfig, axSim=None, axReco=None, 
                       axRatioSim=None, axRatioReco=None, axCumSumReco=None,
                       nEvents=None, limitXRange=False,
                       plotSim=True, plotReco=True):
    """
    Plots a contineous 1D histogram for given PlotConfig.

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
        xLim1, x = plotContineousHistSim(rootFile, plotConfig, ax=axSim, axRatio=axRatioSim, nEvents=nEvents)
    else:
        xLim1 = (None, None)

    # load RecoPixelTracks if wanted
    if plotReco:
        xLim2, x = plotContineousHistReco(rootFile, plotConfig, ax=axReco, axRatio=axRatioReco, axCumSum=axCumSumReco, nEvents=nEvents)
    else:
        xLim2 = (None, None)

    # find the axes
    if (axSim is None) and (axReco is None):
        ax = plt.gca()
    else:
        ax = axSim if axSim is not None else axReco
        
    # if limit x range
    xLim = limitXNone(xLim1, xLim2)
    if limitXRange:
        ax.set_xlim(xLim)

    return xLim