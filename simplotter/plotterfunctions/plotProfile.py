import uproot
import matplotlib.pyplot as plt
from simplotter.utils.plotttools import cmslabel, savefig, Colors
from simplotter.utils.histtools import getHist


def plotProfile(rootFile, plotConfig, directory="plots", cmsConfig=None, saveas="png", plotReco=True, plotSim=True):
    
    # create new figure
    fig, ax = plt.subplots(1)
    
    if plotReco:
        histTrue = getHist(rootFile, "TruePixelTracks/%s" % (plotConfig.histname))
        histFake = getHist(rootFile, "FakePixelTracks/%s" % (plotConfig.histname))

        ax.errorbar(histTrue.axes.centers[0], histTrue.values(), yerr=histTrue.variances(), xerr=histTrue.axes.widths[0] / 2,
                    color=Colors.true, fmt=".",
                    label="true PixelTracks" if plotConfig.isParticles else ("%ss of true PixelTracks" % plotConfig.recoSubject))
        ax.errorbar(histFake.axes.centers[0], histFake.values(), yerr=histFake.variances(), xerr=histFake.axes.widths[0] / 2,
                    color=Colors.fake, fmt="v",
                    label="fake PixelTracks" if plotConfig.isParticles else ("%ss of fake PixelTracks" % plotConfig.recoSubject))

    if plotSim:
        histTotal = getHist(rootFile, "SimPixelTracks/%s" % (plotConfig.histname))
        print(histTotal.counts())

        ax.errorbar(histTotal.axes.centers[0], histTotal.values(), yerr=histTotal.variances(), xerr=histTotal.axes.widths[0] / 2,
                    fmt="^", color=Colors.total, label="%ss (all)" % plotConfig.simSubject)
        
    # fix axes
    ax.legend()
    ax.set_ylabel(plotConfig.yLabel)
    ax.set_xlabel(plotConfig.xLabel)
    #ax.set_ylim(0,100)
    if plotConfig.isLogX:
        ax.set_xscale("log")
    
    # add the CMS label
    if cmsConfig is not None:
        cmslabel(llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"], ax=ax)
    
    # save and show the figure
    savefig("%s/%s.%s" % (directory, plotConfig.plotname, saveas))
    plt.close()