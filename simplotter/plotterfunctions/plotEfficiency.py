import uproot
import matplotlib.pyplot as plt
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotEfficiency(ROOTfile, histname, directory="plots", x_label="", y_label="", ):
    
    # load histograms
    hist = Hist(ROOTfile, "%s" % (histname))
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot    
    hist.plot(marker="s")

    # fix axes
    ylabel(y_label)
    xlabel(x_label)
    plt.ylim(0,1)
    if "pT" in histname:
        plt.xscale("log")
    
    # add the CMS label
    cmslabel(llabel="Private Work", com=14)
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()
