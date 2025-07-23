import uproot
import matplotlib.pyplot as plt
from simplotter.utils.plotttools import cmslabel, savefig, Colors
from simplotter.utils.histtools import getHist


def plotProfile(rootFile, plotConfig, directory="plots", cmsConfig=None, saveas="png", plotReco=True, plotSim=True):
    
    # create new figure
    fig, ax = plt.subplots()
    
    if plotReco:
        histTrue = getHist(rootFile, "TruePixelTracks/%s" % (plotConfig.histname))
        histFake = getHist(rootFile, "FakePixelTracks/%s" % (plotConfig.histname))

        histTrue.plot1d(ax=ax, histtype="errorbar", color=Colors.true, marker=".",
                    label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
        histFake.plot1d(ax=ax, histtype="errorbar", facecolor=Colors.fake, marker="v",
                    label="fake PixelTracks" if plotConfig.isParticles else ("%ss of fake PixelTracks" % plotConfig.recoSubject))

    if plotSim:
        histTotal = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname))

        histTotal.plot1d(ax=ax, histtype="errorbar", marker="^",
                    label="%ss (all)" % plotConfig.simSubject, color=Colors.total)
        
    # fix axes
    ax.legend()
    ax.set_ylabel(plotConfig.yLabel)
    ax.set_xlabel(plotConfig.xLabel)
    plt.ylim(0,1.1)
    if "vs_pt" in plotConfig.histname:
        plt.xscale("log")
    
    # add the CMS label
    if cmsConfig is not None:
        cmslabel(llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
    
    # save and show the figure
    savefig("%s/%s.%s" % (directory, plotConfig.plotname, saveas))
    plt.close()
