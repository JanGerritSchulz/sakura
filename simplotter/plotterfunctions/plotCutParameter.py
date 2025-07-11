import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from simplotter.utils.histtools import getHist, findXLimits
from simplotter.utils.plotttools import savefig, cmslabel
from simplotter.utils.utils import valToLatexStr, limitXNone, toRGBA
from simplotter.plotterfunctions.plotRatio import plotRatioEfficiency


def findPassValuesEdges(values, edges, cellCut):
    """
    Function to find the values and edges of a tailored histogram after applying a cut.
    That is to say, find the part of the histogram that passes the given cut.
    """
    passEdges = edges.copy()
    passValues = values.copy()

    # set upper limits of edges and corresponding values
    if (cellCut.type=="max" or cellCut.type=="both") & (passEdges[-1] > cellCut.max):
        # if the max value lies within the bounds of the histogram
        iMax = np.argmax(passEdges>=cellCut.max)
        passEdges = np.append(passEdges[:iMax], [min(cellCut.max,passEdges[iMax])]) 
        passValues = passValues[:iMax]

    # set lower limits of edges and corresponding values
    if (cellCut.type=="min" or cellCut.type=="both") & (passEdges[0] < cellCut.min):
        # if the min value lies within the bounds of the histogram
        iMin = np.argmax(passEdges>cellCut.min) - 1
        passEdges = np.append([max(cellCut.min,passEdges[iMin])], passEdges[iMin+1:]) 
        passValues = passValues[iMin:]
        
    return passValues, passEdges


def labelCutValues(cutType, val, CAThetaAddition=""):
    """
    Aranges the label for the cut value.
    """
    valStr = valToLatexStr(val)
    return r"$\text{cut}_\text{" + cutType + "} = " + CAThetaAddition + valStr + "$"


def plotCutValues(ax, cellCut):
    """
    Plot the vertical, dashed line for the cut with corresponding label.
    If the x-value of the cut is out of range, draw an arrow instead.
    """
    # if cellCut is not used don't do anything
    if cellCut.type is None:
        return 

    # get xlim() and ylim()
    xMin, xMax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ymid = (ymax + ymin) / 2
    if ax.get_xscale() == "log":
        factor = 10 ** (np.log10(xMax / xMin) / 20 *0.75)
        dxMin = xMin * factor
        dxMax = xMax / factor
    else:
        dxMin = dxMax = (xMax-xMin) / 20 *0.75

    # case "min"
    if cellCut.type=="min" or cellCut.type=="both":
        cutLabel = labelCutValues("min", cellCut.min, CAThetaAddition=cellCut.cutLabelAddition)
        # if the value is in the plotting range
        if (cellCut.min <= xMax) & (cellCut.min >= xMin):
            ax.axvline(cellCut.min, color="darkblue", linestyle="--", label=cutLabel)
        # if the value is out of bounce
        elif (cellCut.min > xMax):
            ax.scatter(xMax-dxMax, ymid, c='darkblue',marker=r'$\rightarrow$',s=200, label=cutLabel )
        elif (cellCut.min < xMin):
            ax.scatter(xMin+dxMin, ymid, c='darkblue',marker=r'$\leftarrow$',s=200, label=cutLabel )
    
    # case "max"
    if cellCut.type=="max" or cellCut.type=="both":
        cutLabel = labelCutValues("max", cellCut.max, CAThetaAddition=cellCut.cutLabelAddition)
        # if the value is in the plotting range
        if (cellCut.max <= xMax) & (cellCut.max >= xMin):
            ax.axvline(cellCut.max, color="darkblue", linestyle="--", label=cutLabel)
        # if the value is out of bounce
        elif (cellCut.max > xMax):
            ax.scatter(xMax-dxMax, ymid, c='darkblue',marker=r'$\rightarrow$',s=200, label=cutLabel )
        elif (cellCut.max < xMin):
            ax.scatter(xMin+dxMin, ymid, c='darkblue',marker=r'$\leftarrow$',s=200, label=cutLabel )

    ax.set_xlim(xMin, xMax)


def plotCutRecoDoublets(rootFile, cellCut, subfolder, ax=None, axRatio=None, nEvents=None):
    """
    Plot a given cut parameter for true/fake RecoPixelTracks.
    """
    if ax is None:
        ax = plt.gca()

    subject = "Doublet" if cellCut.isDoubletCut else "Connection"
        
    # load histograms
    histFake = getHist(rootFile, "FakePixelTracks/%s%s" % (subfolder,cellCut.histname))
    histTrue = getHist(rootFile, "TruePixelTracks/%spass_%s" % (subfolder,cellCut.histname))

    trueColor = "#1ca01c"
    fakeColor = "#FF0000"
    alpha = 0.25
    if histTrue.sum() > 0:
        histTrue.plot1d(ax=ax, histtype="fill", label="%ss of true PixelTracks" % subject, facecolor=toRGBA(trueColor,alpha)) 
        histTrue.plot1d(ax=ax, histtype="step", label="%ss of true PixelTracks" % subject, color=trueColor, linestyle="dashed")
    else:
        ax.axhline(0, label="no %ss of true PixelTracks" % subject, color=trueColor, linestyle="dashed")
        
    if histTrue.sum() > 0:
        histFake.plot1d(ax=ax, histtype="fill", label="%ss of fake PixelTracks" % subject, facecolor=toRGBA(fakeColor,alpha))
        histFake.plot1d(ax=ax, histtype="step", label="%ss of fake PixelTracks" % subject, color=fakeColor, linestyle="dashed")
    else:
        ax.axhline(0, label="no %ss of fake PixelTracks" % subject, color=fakeColor, linestyle="dashed")

    # scale according to number of events if given
    if nEvents is not None:
        ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/nEvents))
        ax.yaxis.set_major_formatter(ticks)

    ax.set_ylabel("#%ss from\nRecoTracks" % subject + ("" if nEvents is None else " / event") + cellCut.yLabelAddition)

    # plot the ratio if wanted
    if axRatio is not None:
        if (histTrue+histFake).sum() > 0:
            plotRatioEfficiency(histFake, histTrue+histFake, cellCut=cellCut, ax=axRatio, fmt=".", color="r")
        axRatio.set_ylabel("Reco%s\nfake rate" % subject, fontsize="x-small", color="r")

    trueXLimits = findXLimits(histTrue, log=ax.get_xscale() == "log")
    fakeXLimits = findXLimits(histFake, log=ax.get_xscale() == "log")
    

    return limitXNone(trueXLimits, fakeXLimits)



def plotCutSimDoublets(rootFile, cellCut, subfolder, ax=None, axRatio=None, nEvents=None):
    """
    Plot a given cut parameter for the true SimDoublets.
    """
    if ax is None:
        ax = plt.gca()
    
    subject  = "SimDoublet" if cellCut.isDoubletCut else "SimConnection"

    # load histograms
    histTotal = getHist(rootFile, "SimPixelTracks/%s%s" % (subfolder,cellCut.histname))
    histPass = getHist(rootFile, "SimPixelTracks/%spass_%s" % (subfolder,cellCut.histname))
    
    # find the edges and values of the doublets passing this cut
    x = histTotal.axes.edges[0]
    y = histTotal.values()
    #passValues, passEdges = findPassValuesEdges(y, x, cellCut)

    # plot: passing this cut, passing all cuts, all
    passColor = '#51BBFE'
    allColor = "#00008B"
    if histTotal.sum() > 0:
        #ax.stairs(passValues, passEdges, fill=True, color='#5790fc', alpha=0.5, label="SimDoublets (pass this cut)")
        if histPass.sum() > 0:
            histPass.plot1d(ax=ax, histtype="fill", label="%ss (pass all cuts)" % subject, hatch='//', facecolor="w", edgecolor=passColor)
            histPass.plot1d(ax=ax, histtype="step", label="%ss (pass all cuts)" % subject, color=passColor, linewidth=2)
        else:
            ax.axhline(0, label="no %s passed all cuts" % subject, color=passColor, linewidth=2)
        histTotal.plot1d(ax=ax, histtype="step", label="%ss (all)" % subject, color=allColor, linewidth=2)
    else:
        ax.axhline(0, label="no %ss" % subject, color=allColor, linewidth=2)
    
    # set fix axes
    ax.set_ylabel("#%ss" % subject + ("" if nEvents is None else " / event") + cellCut.yLabelAddition)

    # scale according to number of events if given
    if nEvents is not None:
        ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/nEvents))
        ax.yaxis.set_major_formatter(ticks)

    # plot the ratio if wanted
    if axRatio is not None:
        if histTotal.sum() > 0:
            plotRatioEfficiency(histPass, histTotal, cellCut=cellCut, ax=axRatio, fmt=".", color=passColor)
        axRatio.set_ylabel("%s\nefficiency" % subject, fontsize="x-small", color=passColor)
    
    return findXLimits(histTotal, log=ax.get_xscale() == "log")



# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

def plotCutParameter(rootFile, cellCut, directory="plots", 
                     nEvents=None, cmsConfig=None, limitXRange=False,
                     plotSimDoublets=True, plotRecoDoublets=True, saveas="png"):
    """
    Produces and saves the full plot for a given cut parameter.
    
    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        cellCut (CellCut object): This object contains all information specifying the cut:
                                  histname, label, type, min/max values, innerLayer, ...
        directory (str, optional): directory where to save the plot.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
        cmsConfig (dict, optional): Dictionary containing specifications for the CMS label on top of the plot.
        limitXRange (bool, optional): If True, the x range of the plot is tailored to the non-empty bins of the histograms.
        plotSimDoublets (bool, optional): To enable/disable the plotting of the SimDoublets distribution.
        plotRecoDoublets (bool, optional): To enable/disable the plotting of the reconstructed doublets used in RecoTracks.
    """
    # specify subfolder depending on layer-pair dependence
    subfolder = "CAParameters/" + ("doubletCuts/" if cellCut.isDoubletCut else "connectionCuts/")
    if (cellCut.isLayerDependent) and (cellCut.isDoubletCut):
        subfolder += "lp_%i_%i/" % (cellCut.innerLayer, cellCut.outerLayer)
    elif cellCut.isDoubletCut:
        subfolder += "global/"
    elif (cellCut.isLayerDependent) and (cellCut.isConnectionCut):
        subfolder += "layer_%i/" % cellCut.innerLayer
    elif not cellCut.isConnectionCut:
        raise ValueError('Provided cut "%s" is neither DoubletCut nor ConnectionCut. ' % cellCut.histname +
                         'If it is, please specify this in its CellCut object ' +
                         'by setting the respective isXXXXCut to True.')
    
    # create new figure
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

    # set x axis to log for pt
    if cellCut.isLog:
        ax1.set_xscale("log")

    # plot the SimDoublet distribution
    if plotSimDoublets:
        xLim1 = plotCutSimDoublets(rootFile, cellCut, subfolder,
                                   ax=ax1, axRatio=ax2, nEvents=nEvents)
    else:
        xLim1 = (None, None)

    # make copy of the axes
    if plotSimDoublets and plotRecoDoublets:
        ax1c = ax1.twinx()
        ax2c = ax2.twinx()
    else:
        ax1c, ax2c = ax1, ax2
        
    # plot the true and fake PixelTrack distributions
    if plotRecoDoublets:
        xLim2 = plotCutRecoDoublets(rootFile, cellCut, subfolder, ax=ax1c, axRatio=ax2c, nEvents=nEvents)
    else:
        xLim2 = (None, None)

    # if limit x range
    if limitXRange:
        xLim = limitXNone(xLim1, xLim2)
        ax2.set_xlim(xLim)
    
    # plot the cut values
    plotCutValues(ax1, cellCut)

    ax1.set_xlabel("")
    ax2.set_xlabel(cellCut.label)
    ax2.axhline(0, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
    ax2.axhline(1, color="k", linestyle="dashed", alpha=0.5, linewidth=1)
    ax2.set_ylim(-0.15, 1.15)
    ax2c.set_ylim(-0.15, 1.15)
    plt.subplots_adjust(hspace=0.)
    
    # add the CMS label
    if cmsConfig is not None:
        cmslabel(ax=ax1, llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
    
    # save and show the figure
    axsToCheck = [ax1, ax1c] if (plotCutRecoDoublets and plotCutSimDoublets) else [ax1]
    handlesLabels = [ax.get_legend_handles_labels() for ax in axsToCheck]
    handles, labels = [sum(lol, []) for lol in zip(*handlesLabels)]
    uniqueLabels = np.unique(labels)
    labels = np.array(labels)
    uniqueHandles = [tuple([handles[i] for i in np.where(label==labels)[0]]) for label in uniqueLabels]
    directory += "/CAParameters/" + ("doubletCuts" if cellCut.isDoubletCut else "connectionCuts")
    if (cellCut.isLayerDependent) and (cellCut.isDoubletCut):
        ax1.legend(uniqueHandles, uniqueLabels, title = "Layer pair (%i,%i)" % (cellCut.innerLayer, cellCut.outerLayer), loc='upper left', bbox_to_anchor=(1.2, 1))
        savefig("%s/%s/lp_%i_%i.%s" % (directory, cellCut.histname, cellCut.innerLayer, cellCut.outerLayer, saveas))
    elif (cellCut.isLayerDependent) and (cellCut.isConnectionCut):
        ax1.legend(uniqueHandles, uniqueLabels, title = "Layer %i" % (cellCut.innerLayer), loc='upper left', bbox_to_anchor=(1.2, 1))
        savefig("%s/%s/layer_%i.%s" % (directory, cellCut.histname, cellCut.innerLayer, saveas))
    else:
        ax1.legend(uniqueHandles, uniqueLabels, loc='upper left', bbox_to_anchor=(1.2, 1))
        savefig("%s/%s.%s" % (directory, cellCut.histname, saveas))
    plt.close()