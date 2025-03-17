import matplotlib.pyplot as plt
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotDiscreteHist(ROOTfile, histname, directory="plots", num_events=None, x_label="", y_label="", x_lim=(None, None)):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"

    
    # load histograms
    hTot = Hist(ROOTfile, "general/%s" % (histname), scale_for_values = 1/num_events)
    hPass = Hist(ROOTfile, "general/pass_%s" % (histname), scale_for_values = 1/num_events)
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot
    y = hTot.values
    x = (hTot.edges[1:] + hTot.edges[:-1])/2
    xTot = x - (hTot.edges[1:]-hTot.edges[:-1]) / 6
    xPass = x + (hTot.edges[1:]-hTot.edges[:-1]) / 6
    
    plt.bar(xTot, hTot.values, 1/3, color='darkblue', label="total")
    plt.bar(xPass, hPass.values, 1/3, color='#5790fc', label="passing")
    plt.legend()

    # fix axes
    plt.xticks(x, [(str(int(x_)) if (x_%1==0) else "") for x_ in x])
    ax.xaxis.set_tick_params(which='minor',bottom=False,top=False)
    ylabel(y_label + ylabel_suff)
    xlabel(x_label)
    ax.set_xlim(x_lim)
    if "pT" in histname:
        plt.xscale("log")
    
    # add the CMS label
    cmslabel(llabel="Private Work", com=14)
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()