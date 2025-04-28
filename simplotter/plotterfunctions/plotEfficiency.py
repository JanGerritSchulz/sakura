import uproot
import matplotlib.pyplot as plt
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotEfficiency(ROOTfile, histname, directory="plots", x_label="", y_label="", labels=None, cmsconfig=None):
    
    # create new figure
    fig, ax = plt.subplots()
    
    # if multiple ROOT files are handed, loop over them
    if isinstance(ROOTfile, list):
        for ROOTfile_, label_ in zip(ROOTfile, labels):
            # load histograms
            hist = Hist(ROOTfile_, histname)
            # plot    
            hist.plot(ax=ax, marker="s", label=label_)
        ax.legend()

    else:
        # load histograms
        hist = Hist(ROOTfile, "%s" % (histname))
        # plot    
        hist.plot(ax=ax, marker="s")

    # fix axes
    ylabel(y_label)
    xlabel(x_label)
    plt.ylim(0,1)
    if "pT" in histname:
        plt.xscale("log")
    
    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"])
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()
