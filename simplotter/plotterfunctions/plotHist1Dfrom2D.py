import matplotlib.pyplot as plt
import matplotlib as mpl
import re
from simplotter.utils.utils import valToLatexStr, toRGBA, limitXNone
from simplotter.utils.plotttools import cmslabel, savefig, legend, Colors
from simplotter.utils.histtools import getHist, histSlice1DFrom2D, findXLimits
from simplotter.plotterfunctions.plotRatio import plotRatioEfficiency

def plotContineousHistSim(plotConfig, histTotal=None, histPass=None, ax=None, axRatio=None, nEvents=None):
    """
    Plot a given contineous 1D histogram of sim objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    if histPass is not None:
        histPass.plot1d(ax=ax, histtype="fill", hatch='//', facecolor="w", edgecolor=Colors.passed,  
                        label="TrackingParticles (w/ alive SimNtuplet)" if plotConfig.isParticles else "%ss (pass all cuts)" % plotConfig.simSubject % plotConfig.simSubject)
        histPass.plot1d(ax=ax, histtype="step",color=Colors.passed, linewidth=2,
                        label="TrackingParticles (w/ alive SimNtuplet)" if plotConfig.isParticles else "%ss (pass all cuts)" % plotConfig.simSubject % plotConfig.simSubject)

    if histTotal is not None:
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
        axRatio.set_ylabel("%s\nefficiency" % plotConfig.simSubject, fontsize="xx-small", color=Colors.passed)

    return findXLimits(histTotal, log=ax.get_xscale() == "log")


def plotContineousHistReco(plotConfig, histTrue=None, histFake=None, ax=None, axRatio=None, axCumSum=None, nEvents=None):
    """
    Plot a given contineous 1D histogram of reco objects with given plotConfig.
    """
    if ax is None:
        ax = plt.gca()

    alpha = 0.25
    if histTrue is not None:
        histTrue.plot1d(ax=ax, histtype="fill", facecolor=toRGBA(Colors.true,alpha),
                        label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
        histTrue.plot1d(ax=ax, histtype="step", color=Colors.true, linestyle="dashed",
                        label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))

    if histFake is not None:
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
            
        axRatio.set_ylabel("Reco%s\nfake rate" % plotConfig.recoSubject, fontsize="xx-small", color=Colors.fake)

    if axCumSum is not None:
        axCumSum.errorbar(histTrue.axes.centers[0], histTrue.values().cumsum() / histTrue.sum(), xerr=histTrue.axes.widths[0]/2, fmt="+", color=Colors.true, linewidth=0.75)
        axCumSum.set_ylabel("Cum. sum of\ntrue Reco%ss" % plotConfig.recoSubject, fontsize="xx-small", color=Colors.true)

    return findXLimits(histTrue, log=ax.get_xscale() == "log")



def plotHist1Dfrom2D(rootFile, plotConfig, directory="plots", 
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

    # get the number of subplots
    nPlots = len(plotConfig.slices)

    # create new figure
    fig, axs = plt.subplots(2*nPlots, 1, sharex=True, height_ratios=[3, 1]*nPlots, figsize=(12, 6*nPlots))

    # make copy of the axes
    axsc = [ax.twinx() if (plotSim and plotReco) else ax for ax in axs]
    axsCumSum = [ax.twinx() if plotConfig.plotCumSumReco else None for ax in axs[1::2]]

    # set x axis to log
    if plotConfig.isLogX:
        axs[0].set_xscale("log")

    # set y axis to log
    if plotConfig.isLogY:
        for i in range(0, len(axs), 2):
            axs[i].set_yscale("log")
            axsc[i].set_yscale("log")

    # get histograms
    histTrue = getHist(rootFile, "TruePixelTracks/%s" % (plotConfig.histname)) if plotReco else None
    histFake = getHist(rootFile, "FakePixelTracks/%s" % (plotConfig.histname)) if plotReco else None
    histTotal = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname)) if plotSim else None
    histPass  = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname), isPass=True) if plotSim else None

    xLim = (None, None)

    # plot the histograms
    for i, bin in enumerate(plotConfig.slices):
        if plotSim:
            # get slices
            histTotal_, slice = histSlice1DFrom2D(histTotal, bin, axis=plotConfig.axis, axisIsDiscrete=plotConfig.axisIsDiscrete)
            histPass_,  slice = histSlice1DFrom2D(histPass, bin, axis=plotConfig.axis, axisIsDiscrete=plotConfig.axisIsDiscrete)

            # plot histogram
            xLim_ = plotContineousHistSim(plotConfig, histTotal=histTotal_, histPass=histPass_, ax=axs[2*i], axRatio=axs[2*i+1], nEvents=nEvents)
            xLim = limitXNone(xLim, xLim_)
            
        if plotReco:
            # get slices
            histTrue_, slice = histSlice1DFrom2D(histTrue, bin, axis=plotConfig.axis, axisIsDiscrete=plotConfig.axisIsDiscrete)
            histFake_, slice = histSlice1DFrom2D(histFake, bin, axis=plotConfig.axis, axisIsDiscrete=plotConfig.axisIsDiscrete)

            # plot histogram
            xLim_ = plotContineousHistReco(plotConfig, histTrue=histTrue_, histFake=histFake_, ax=axsc[2*i], axRatio=axsc[2*i+1], axCumSum=axsCumSum[i], nEvents=nEvents)
            xLim = limitXNone(xLim, xLim_)

        x_ = 0.04
        y_ = 0.85
        x_ = x_ if plotConfig.sliceLabelAlignment=="left" else (1-x_)
        if plotConfig.axisIsDiscrete:
            label_ = plotConfig.sliceLabel + r"$=" + valToLatexStr(slice) + r"$"
        else:
            label_ = r"$" + valToLatexStr(slice[0]) + r"<$ " + plotConfig.sliceLabel + r" $<" + valToLatexStr(slice[1]) + r"$"

        label_ = re.sub("$$",'', label_)
        axs[2*i].text(x_, y_, label_, horizontalalignment=plotConfig.sliceLabelAlignment, transform=axs[2*i].transAxes)

    # if limit x range
    if limitXRange:
        axs[0].set_xlim(xLim)

    # plot legend
    axs_ = [axs[0], axsc[0]] if (plotReco and plotSim) else [axs[0]]
    legend(axs[0], axs_, loc='upper left', bbox_to_anchor=(1.2, 1))

    for ax in axs[:-1]:
        ax.set_xlabel("")
    axs[-1].set_xlabel(plotConfig.xLabel)
    for ax in axs[1::2]:
        ax.axhline(0, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
        ax.axhline(1, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
        ax.set_ylim(-0.15, 1.15)
    for ax in axsc[1::2]:
        ax.set_ylim(-0.15, 1.15)
    for axCumSum in axsCumSum:
        if axCumSum is not None:
            axCumSum.set_ylim(-0.15, 1.15)
            if (plotSim and plotReco):
                axCumSum.spines['right'].set_position(('outward', 80))
    plt.subplots_adjust(hspace=0.)

    # add the CMS label
    if cmsConfig is not None:
        cmslabel(ax=axs[0], llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
    
    # save and show the figure
    savefig("%s/%s.%s" % (directory, plotConfig.plotname, saveas))
    plt.close()