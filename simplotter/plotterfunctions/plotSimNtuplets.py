import matplotlib.pyplot as plt
import numpy as np
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotSimNtuplets(ROOTfile, x_quantity="eta", directory="plots", x_label=""):
    
    # load histograms
    categories = {
        "Alive" : {"label" : "alive", "color" : "#C0FB2D"},
        "MissingLayerPair" : {"label" : "is missing a layer pair", "color" : "#1B2021"},
        "KilledDoublets" : {"label" : "has killed doublets", "color" : "#016FB9"},
        "KilledConnections" : {"label" : "has killed connections", "color" : "#61E8E1"},
        "TooShort" : {"label" : "has 3+ RecHits but is shorter\nthan reco threshold", "color" : "#88958D"},
        "UndefDoubletCuts" : {"label" : "has undef doublet cuts", "color" : "sun yellow"},
        "UndefConnectionCuts" : {"label" : "has undef connection cuts", "color" : "magenta"},
    }
    hists = {
        c : Hist(ROOTfile, "simNtuplets/rate%s_vs_%s" % (c, x_quantity)) for c in categories
        }
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot    
    y_baseline = np.zeros_like(hists[list(categories.keys())[0]].values)
    for c in categories.keys():
        if (c == "UndefDoubletCuts" or c == "UndefConnectionCuts"):
            if np.sum(hists[c].values) == 0:
                continue
        ax.stairs(hists[c].values + y_baseline, hists[c].edges, baseline=y_baseline, 
                  fill=True, label=categories[c]["label"],
            color=categories[c]["color"])
        y_baseline += hists[c].values
    
    plt.legend(reverse=True, loc='center left', bbox_to_anchor = (1.03, 0.5))

    # fix axes
    ylabel("Rates of longest SimNtuplets\nof TrackingParticles")
    xlabel(x_label)
    plt.ylim(0,1)
    if "pT" in x_quantity:
        plt.xscale("log")
    
    # add the CMS label
    cmslabel(llabel="Private Work", com=14)
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/simNtupletsRate_vs_%s.png" % (directory, x_quantity))
    plt.close()