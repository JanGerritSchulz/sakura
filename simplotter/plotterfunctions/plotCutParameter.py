import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from simplotter.utils.histtools import getHist, findXLimits
from simplotter.utils.plotttools import savefig, cmslabel, Colors, legend, plotPercentageBoxSim, ColorMap
from simplotter.utils.utils import valToLatexStr, limitXNone, toRGBA
from simplotter.plotterfunctions.plot2D import plot2D_
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

    subject = "Doublet" if cellCut.isDoubletCut else (
              "Triplet" if cellCut.isTripletCut else (
              "Quadruplet" if cellCut.isQuadrupletCut else (
              "Doublet pair" if cellCut.isFishbone else (
              "Track"
              ))))
        
    # load histograms
    histFake = getHist(rootFile, "FakePixelTracks/%s%s" % (subfolder,cellCut.histname))
    histTrue = getHist(rootFile, "TruePixelTracks/%s%s" % (subfolder,cellCut.histname))

    alpha = 0.25
    if histTrue.sum() > 0:
        histTrue.plot1d(ax=ax, histtype="fill", label="%ss of true PixelTracks" % subject, facecolor=toRGBA(Colors.true,alpha)) 
        histTrue.plot1d(ax=ax, histtype="step", label="%ss of true PixelTracks" % subject, color=Colors.true, linestyle="dashed")
    else:
        ax.axhline(0, label="no %ss of true PixelTracks" % subject, color=Colors.true, linestyle="dashed")
        
    if histTrue.sum() > 0:
        histFake.plot1d(ax=ax, histtype="fill", label="%ss of fake PixelTracks" % subject, facecolor=toRGBA(Colors.fake,alpha))
        histFake.plot1d(ax=ax, histtype="step", label="%ss of fake PixelTracks" % subject, color=Colors.fake, linestyle="dashed")
    else:
        ax.axhline(0, label="no %ss of fake PixelTracks" % subject, color=Colors.fake, linestyle="dashed")

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
    
    subject  = "SimDoublet" if cellCut.isDoubletCut else (
               "SimTriplet" if cellCut.isTripletCut else (
               "SimQuadruplet" if cellCut.isQuadrupletCut else (
               "SimDoublet pair" if cellCut.isFishbone else (
               "TrackingParticle"
               ))))

    # load histograms
    histTotal = getHist(rootFile, "SimPixelTracks/%s%s" % (subfolder,cellCut.histname))
    histPass = getHist(rootFile, "SimPixelTracks/%s%s" % (subfolder,cellCut.histname), isPass=True)
    fracPassThisCut = getHist(rootFile, "SimPixelTracks/%s%s_passThisCut" % (subfolder,cellCut.histname))
    
    # find the edges and values of the doublets passing this cut
    # x = histTotal.axes.edges[0]
    # y = histTotal.values()
    #passValues, passEdges = findPassValuesEdges(y, x, cellCut)

    # plot: passing this cut, passing all cuts, all
    if histTotal.sum() > 0:
        #ax.stairs(passValues, passEdges, fill=True, color='#5790fc', alpha=0.5, label="SimDoublets (pass this cut)")
        if histPass.sum() > 0:
            histPass.plot1d(ax=ax, histtype="fill", label="%ss (pass all cuts)" % subject, hatch='//', facecolor="w", edgecolor=Colors.passed)
            histPass.plot1d(ax=ax, histtype="step", label="%ss (pass all cuts)" % subject, color=Colors.passed, linewidth=2)
        else:
            ax.axhline(0, label="no %s passed all cuts" % subject, color=Colors.passed, linewidth=2)
        histTotal.plot1d(ax=ax, histtype="step", label="%ss (all)" % subject, color=Colors.total, linewidth=2)
    else:
        ax.axhline(0, label="no %ss" % subject, color=Colors.total, linewidth=2)
    
    # set fix axes
    ax.set_ylabel("#%ss" % subject + ("" if nEvents is None else " / event") + cellCut.yLabelAddition)

    # scale according to number of events if given
    if nEvents is not None:
        ticks = mpl.ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/nEvents))
        ax.yaxis.set_major_formatter(ticks)

    # plot the percentage box for passing this cut
    plotPercentageBoxSim(ax, fracPassThisCut.values()[0] / fracPassThisCut.counts()[0])

    # plot the ratio if wanted
    if axRatio is not None:
        if histTotal.sum() > 0:
            plotRatioEfficiency(histPass, histTotal, cellCut=cellCut, ax=axRatio, fmt=".", color=Colors.passed)
        axRatio.set_ylabel("%s\nefficiency" % subject, fontsize="x-small", color=Colors.passed)
    
    return findXLimits(histTotal, log=ax.get_xscale() == "log")



def plot2DCutRecoDoublets(rootFile, cellCut, subfolder, fig, ax=None, nEvents=None, which="True"):
    """
    Plots the 2D cut histogram for a given cellCut for true/fake RecoPixelTracks.

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        cellCut (CellCut object): This object contains all information specifying the cut:
                                  histname, label, type, min/max values, innerLayer, ...
        subfolder (str): subfolder of the histogram in the DQM file.
        fig (plt figure): figure to put the histogram in.
        ax (plt axes, optional): _description_. Defaults to None.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
    """
    if ax is None:
        ax = plt.gca()
    
    subject = "Doublet" if cellCut.isDoubletCut else (
              "Triplet" if cellCut.isTripletCut else (
              "Quadruplet" if cellCut.isQuadrupletCut else (
              "Track"
              )))
        
    # load histograms
    histTotal = getHist(rootFile, "%sPixelTracks/%s%s" % (which,subfolder,cellCut.histname))

    # plot the histogram
    plot2D_(histTotal, fig, ax, zLabel="#%ss of %s PixelTracks" % (subject, which) + cellCut.yLabelAddition, # + ("" if nEvents is None else " / event")
            nEvents=nEvents, logZ=cellCut.isLogZ, cmap=ColorMap.get(which))
    
    return (histTotal.axes[0].edges[0], histTotal.axes[0].edges[-1])
    

    
def plot2DCutSimDoublets(rootFile, cellCut, subfolder, fig, ax=None, nEvents=None):
    """
    Plots the 2D cut histogram for a given cellCut for the true SimDoublets.

    Args:
        rootFile (opened ROOT file): The object returned by `uproot.open(filename.root)`.
        cellCut (CellCut object): This object contains all information specifying the cut:
                                  histname, label, type, min/max values, innerLayer, ...
        subfolder (str): subfolder of the histogram in the DQM file.
        fig (plt figure): figure to put the histogram in.
        ax (plt axes, optional): _description_. Defaults to None.
        nEvents (int, optional): Number of events used for the histograms. If provided, the histograms are plotted
                                 in numbers per event.
    """
    if ax is None:
        ax = plt.gca()
    
    subject  = "SimDoublet" if cellCut.isDoubletCut else (
               "SimTriplet" if cellCut.isTripletCut else (
               "SimQuadruplet" if cellCut.isQuadrupletCut else (
               "TrackingParticle"
               )))

    # load histograms
    histTotal = getHist(rootFile, "SimPixelTracks/%s%s" % (subfolder,cellCut.histname))

    # plot the histogram
    plot2D_(histTotal, fig, ax, zLabel="#%ss" % subject + cellCut.yLabelAddition, 
            nEvents=nEvents, logZ=cellCut.isLogZ, cmap=ColorMap.get("Sim"))
    
    return (histTotal.axes[0].edges[0], histTotal.axes[0].edges[-1])



def plot2DCutDoublets(rootFile, cellCut, subfolder, fig, ax=None, nEvents=None, which="Sim"):
    if which == "Sim":
        return plot2DCutSimDoublets(rootFile, cellCut, subfolder, fig, ax=ax, nEvents=nEvents)
    else:
        return plot2DCutRecoDoublets(rootFile, cellCut, subfolder, fig, ax=ax, nEvents=nEvents, which=which)     



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
    subfolder = "CAParameters/" + ("doubletCuts/" if cellCut.isDoubletCut else (
                                   "tripletCuts/" if cellCut.isTripletCut else (
                                   "quadrupletCuts/" if cellCut.isQuadrupletCut else (
                                   "fishbone/" if cellCut.isFishbone else (
                                   "startingCuts/"
                                   )))))
    if (cellCut.isLayerDependent) and (cellCut.isDoubletCut):
        subfolder += "lp_%i_%i/" % (cellCut.innerLayer, cellCut.outerLayer)
    elif cellCut.isDoubletCut:
        subfolder += "global/"
    elif (cellCut.isLayerDependent) and (cellCut.isTripletCut or cellCut.isQuadrupletCut or cellCut.isStartingCut or cellCut.isFishbone):
        subfolder += "layer_%i/" % cellCut.innerLayer
    elif not (cellCut.isTripletCut or cellCut.isQuadrupletCut or cellCut.isStartingCut or cellCut.isFishbone):
        raise ValueError('Provided cut "%s" is neither DoubletCut nor ConnectionCut nor StartingCut. ' % cellCut.histname +
                         'If it is, please specify this in its CellCut object ' +
                         'by setting the respective isXXXXCut to True.')
    
    # 2D cut
    if cellCut.is2D:
        cases = ["True", "Fake"] if plotRecoDoublets else []
        cases += ["Sim"] if plotSimDoublets else []
        for which in cases:
            # create new figure
            fig, ax1 = plt.subplots()

            xLim = plot2DCutDoublets(rootFile, cellCut, subfolder, fig, ax=ax1, nEvents=nEvents, which=which)

            yLim = ax1.get_ylim()
            
            x = np.linspace(xLim[0], xLim[1], 51)
            ax1.plot(x, cellCut.func2D(x), label="cut limit", color="red", linestyle="--")

            ax1.set_xlabel(cellCut.label)
            ax1.set_ylabel(cellCut.yLabel)
            ax1.set_ylim(yLim)

            # add the CMS label
            if cmsConfig is not None:
                cmslabel(ax=ax1, llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
            
            # save and show the figure
            directory += "/CAParameters/" + ("doubletCuts" if cellCut.isDoubletCut else (
                                            "fishbone" if cellCut.isFishbone else (
                                            "tripletCuts" if cellCut.isTripletCut else (
                                            "quadrupletCuts" if cellCut.isQuadrupletCut else (
                                            "startingCuts")))))
            axs = [ax1]
            if (cellCut.isLayerDependent) and (cellCut.isDoubletCut):
                legend(ax1, axs, title = "Layer pair (%i,%i)" % (cellCut.innerLayer, cellCut.outerLayer))
                savefig("%s/%s/%s_lp_%i_%i.%s" % (directory, cellCut.histname, which, cellCut.innerLayer, cellCut.outerLayer, saveas))
            elif (cellCut.isLayerDependent) and (cellCut.isTripletCut or cellCut.isQuadrupletCut or cellCut.isStartingCut or cellCut.isFishbone):
                legend(ax1, axs, title = "Layer %i" % (cellCut.innerLayer))
                savefig("%s/%s/%s_layer_%i.%s" % (directory, cellCut.histname, which, cellCut.innerLayer, saveas))
            else:
                legend(ax1, axs)
                savefig("%s/%s_%s.%s" % (directory, which, cellCut.histname, saveas))
            plt.close()

    # 1D cut
    else: 
        # create new figure
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[3, 1])

        # set x axis to log if wanted
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
        directory += "/CAParameters/" + ("doubletCuts" if cellCut.isDoubletCut else (
                                        "fishbone" if cellCut.isFishbone else (
                                        "tripletCuts" if cellCut.isTripletCut else (
                                        "quadrupletCuts" if cellCut.isQuadrupletCut else (
                                        "startingCuts")))))
        axs = [ax1, ax1c] if (plotCutRecoDoublets and plotCutSimDoublets) else [ax1]
        if (cellCut.isLayerDependent) and (cellCut.isDoubletCut):
            legend(ax1, axs, title = "Layer pair (%i,%i)" % (cellCut.innerLayer, cellCut.outerLayer), loc='upper left', bbox_to_anchor=(1.2, 1))
            savefig("%s/%s/lp_%i_%i.%s" % (directory, cellCut.histname, cellCut.innerLayer, cellCut.outerLayer, saveas))
        elif (cellCut.isLayerDependent) and (cellCut.isTripletCut or cellCut.isQuadrupletCut or cellCut.isStartingCut or cellCut.isFishbone):
            legend(ax1, axs, title = "Layer %i" % (cellCut.innerLayer), loc='upper left', bbox_to_anchor=(1.2, 1))
            savefig("%s/%s/layer_%i.%s" % (directory, cellCut.histname, cellCut.innerLayer, saveas))
        else:
            legend(ax1, axs, loc='upper left', bbox_to_anchor=(1.2, 1))
            savefig("%s/%s.%s" % (directory, cellCut.histname, saveas))
        plt.close()