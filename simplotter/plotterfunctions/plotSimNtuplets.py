import numpy as np
import matplotlib.pyplot as plt
from simplotter.utils.histtools import getHist
from simplotter.utils.plotttools import cmslabel, savefig


def plotSimNtuplets(rootFile, plotConfig, directory="plots", cmsConfig=None, saveas="png", rootFileMTV=None):

    colorPalette1 = ["#C0FB2D", "#1B2021", "#016FB9", "#61E8E1", "#773FF8", "#336346", "#88958D", "#ff00ff", "#ff00ff", "#DEDEDE"]
    colorPalette2 = ["#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000", "#FFB000", "#ff00ff", "#ff00ff", "#DEDEDE"]

    xQuantity = "eta" if "eta" in plotConfig.xLabel else "pt"

    colorPalette = colorPalette1
    
    # load histograms
    categories = {
        "Alive" : {"label" : "built", "color" : colorPalette[0]},
        "NotStartingPair" : {"label" : "Ntuplet does not start in a starting pair", "color" : colorPalette[5]},
        "KilledTripletConnections" : {"label" : "has killed triplet connections", "color" : colorPalette[4]},
        "KilledDoubletConnections" : {"label" : "has killed doublet connections", "color" : colorPalette[3]},
        "KilledDoublets" : {"label" : "has killed doublets", "color" : colorPalette[2]},
        "MissingLayerPair" : {"label" : "is missing a layer pair", "color" : colorPalette[1]},
        "TooShort" : {"label" : "shorter than reco threshold", "color" : colorPalette[6]},
        "UndefDoubletCuts" : {"label" : "has undef doublet cuts", "color" : colorPalette[7]},
        "UndefConnectionCuts" : {"label" : "has undef connection cuts", "color" : colorPalette[8]},
    }
    hists = {
        c : getHist(rootFile, "SimPixelTracks/SimNtuplets/%s/frac%s_vs_%s" % (plotConfig.histname, c, xQuantity)) for c in categories
        }
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot    
    y_baseline = np.zeros_like(hists[list(categories.keys())[0]].values())
    edges = hists[list(categories.keys())[0]].axes.edges[0]
    for c in categories.keys():
        if (c == "UndefDoubletCuts" or c == "UndefConnectionCuts"):
            if np.sum(hists[c].values()) == 0:
                continue
        if c == "Alive":
            ax.stairs(hists[c].values() + y_baseline, edges, baseline=y_baseline, 
                  fill=True, label=categories[c]["label"],
                  fc=categories[c]["color"], edgecolor="#648B03", linewidth=0.7)
        else:
            ax.stairs(hists[c].values() + y_baseline, edges, baseline=y_baseline, 
                  fill=True, label=categories[c]["label"],
                  color=categories[c]["color"])
        y_baseline += hists[c].values()
    
    ax.stairs(np.ones_like(hists[list(categories.keys())[0]].values()), 
              edges, baseline=y_baseline, 
                label="has 2 or less RecHits",
                edgecolor=colorPalette[9], hatch='//')
    
    if rootFileMTV is not None:
        recoEff = getHist(rootFileMTV, "hltPhase2Pixel_hltAssociatorByHits/effic")
        recoEff.plot1D(ax=ax, histtype="errorbar", color="#FF0000", fmt=".", label="actual RecoTrack efficiency")

    ax.legend(title="Status of TP's %s SimNtuplet" % ("longest" if plotConfig.histname=="longest" else "most alive"),
               reverse=True, loc='center left', bbox_to_anchor = (1.03, 0.5))

    # fix axes
    ax.set_ylabel("Fractions of TrackingParticles")
    ax.set_xlabel(plotConfig.xLabel)
    ax.set_ylim(0,1)
    if plotConfig.isLogX:
        ax.set_xscale("log")
    
    # add the CMS label
    if cmsConfig is not None:
        cmslabel(ax=ax, llabel=cmsConfig["llabel"], rlabel=cmsConfig["rlabel"], com=cmsConfig["com"])
    
    # save and show the figure
    savefig("%s/%s.%s" % (directory, plotConfig.plotname, saveas))
    plt.close()