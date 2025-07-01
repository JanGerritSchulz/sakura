import matplotlib.pyplot as plt
import numpy as np
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotSimNtuplets(ROOTfile, ntuplet, x_quantity="eta", directory="plots", x_label="", cmsconfig=None):

    colorPalette1 = ["#C0FB2D", "#1B2021", "#016FB9", "#61E8E1", "#336346", "#88958D", "sun yellow", "magenta", "#DEDEDE"]
    colorPalette2 = ["#648FFF", "#785EF0", "#DC267F", "#FE6100", "#FFB000", "#FFB000", "sun yellow", "magenta", "#DEDEDE"]

    colorPalette = colorPalette1
    
    # load histograms
    categories = {
        "Alive" : {"label" : "built", "color" : colorPalette[0]},
        "NotStartingPair" : {"label" : "Ntuplet starts not in a starting pair", "color" : colorPalette[4]},
        "KilledConnections" : {"label" : "has killed connections", "color" : colorPalette[3]},
        "KilledDoublets" : {"label" : "has killed doublets", "color" : colorPalette[2]},
        "MissingLayerPair" : {"label" : "is missing a layer pair", "color" : colorPalette[1]},
        "TooShort" : {"label" : "shorter than reco threshold", "color" : colorPalette[5]},
        "UndefDoubletCuts" : {"label" : "has undef doublet cuts", "color" : colorPalette[6]},
        "UndefConnectionCuts" : {"label" : "has undef connection cuts", "color" : colorPalette[7]},
    }
    hists = {
        c : Hist(ROOTfile, "SimNtuplets/%s/frac%s_vs_%s" % (ntuplet, c, x_quantity)) for c in categories
        }
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot    
    y_baseline = np.zeros_like(hists[list(categories.keys())[0]].values)
    for c in categories.keys():
        if (c == "UndefDoubletCuts" or c == "UndefConnectionCuts"):
            if np.sum(hists[c].values) == 0:
                continue
        if c == "Alive":
            ax.stairs(hists[c].values + y_baseline, hists[c].edges, baseline=y_baseline, 
                  fill=True, label=categories[c]["label"],
                  fc=categories[c]["color"], edgecolor="#648B03", linewidth=0.7)
        else:
            ax.stairs(hists[c].values + y_baseline, hists[c].edges, baseline=y_baseline, 
                  fill=True, label=categories[c]["label"],
                  color=categories[c]["color"])
        y_baseline += hists[c].values
    
    ax.stairs(np.ones_like(hists[list(categories.keys())[0]].values), 
              hists[list(categories.keys())[0]].edges, baseline=y_baseline, 
                label="has 2 or less RecHits",
                edgecolor=colorPalette[8], hatch='//')
    
    plt.legend(title="Status of TP's %s SimNtuplet" % ("longest" if ntuplet=="longest" else "most alive"),
               reverse=True, loc='center left', bbox_to_anchor = (1.03, 0.5))

    # fix axes
    ylabel("Fractions of TrackingParticles")
    xlabel(x_label)
    plt.ylim(0,1)
    if "pt" in x_quantity:
        plt.xscale("log")
    
    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"])
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s/simNtupletsRate_vs_%s.png" % (directory, ntuplet, x_quantity))
    plt.close()