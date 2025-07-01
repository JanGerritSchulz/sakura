import matplotlib.pyplot as plt
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotHist(ROOTfile, histname, directory="plots", num_events=None, x_label="", y_label="", cmsconfig=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"

    
    # load histogram
    hTot = Hist(ROOTfile, histname, scale_for_values = 1/num_events)
    pass_histname = histname.split("/")
    pass_histname[-1] = "pass_"+pass_histname[-1]
    pass_histname = "/".join(pass_histname)
    hPass = Hist(ROOTfile, pass_histname, scale_for_values = 1/num_events)
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot
    plt.stairs(hTot.values, hTot.edges, color='darkblue', label="total", linewidth=2)
    plt.stairs(hPass.values, hPass.edges, color='#5790fc', label="passing", fill=True)
    plt.legend()

    # fix axes
    ylabel(y_label + ylabel_suff)
    xlabel(x_label)

    if ("pt" in histname) or ("Pt" in histname):
        plt.xscale("log")

    if "vs_dxy" in histname:
        plt.yscale("log")
    
    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"])
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()