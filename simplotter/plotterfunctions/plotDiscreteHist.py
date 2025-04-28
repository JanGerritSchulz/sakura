import matplotlib.pyplot as plt
from scipy.stats import binomtest
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path


def plotDiscreteHist(ROOTfile, histname, directory="plots", num_events=None, x_label="", y_label="", x_lim=(None, None), cmsconfig=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"

    
    # load histograms
    hTot = Hist(ROOTfile, histname, scale_for_values = 1/num_events)
    pass_histname = histname.split("/")
    pass_histname[-1] = "pass_"+pass_histname[-1]
    pass_histname = "/".join(pass_histname)
    hPass = Hist(ROOTfile, pass_histname, scale_for_values = 1/num_events)
    
    yEff = []
    yEffErrUp = []
    yEffErrLow = []
    for yPass, yTot in zip(hPass.values, hTot.values):
        if yTot>0:
            # error calculation with eff
            result = binomtest(k=int(yPass*num_events), n=int(yTot*num_events))
            yEff.append(result.statistic)
            yEffErrLow.append(result.proportion_ci(0.683).low)
            yEffErrUp.append(result.proportion_ci(0.683).high)
        else:
            yEff.append(0)
            yEffErrLow.append(0)
            yEffErrUp.append(0)

    # create new figure
    fig, (ax, ax2) = plt.subplots(2, height_ratios=[3, 1], sharex=True)
    
    # plot
    y = hTot.values
    x = (hTot.edges[1:] + hTot.edges[:-1])/2
    xTot = x - (hTot.edges[1:]-hTot.edges[:-1]) / 6
    xPass = x + (hTot.edges[1:]-hTot.edges[:-1]) / 6
    
    ax.bar(xTot, hTot.values, 1/3, color='darkblue', label="total")
    ax.bar(xPass, hPass.values, 1/3, color='#5790fc', label="passing")
    ax.legend()

    ax2.axhline(0, linestyle="dashed", linewidth=1.)
    ax2.axhline(1, linestyle="dashed", linewidth=1.)
    ax2.errorbar(x, yEff, xerr=1/3, fmt=".", lolims=yEffErrLow, uplims=yEffErrUp, color='darkblue')


    # fix axes
    stride = 1 + (int(len(x) / 15) if x_lim[1] is None else int((x < x_lim[1]).sum() / 15))
    ax2.set_xticks(x, [(str(int(x_)) if (x_%stride==0) else "") for x_ in x])
    ax.xaxis.set_tick_params(which='minor',bottom=False,top=False)
    ax2.xaxis.set_tick_params(which='minor',bottom=False,top=False)
    ylabel(y_label + ylabel_suff, ax=ax)
    xlabel(x_label, ax=ax2)
    ax2.set_ylabel("Efficiency")
    ax.set_xlim(x_lim)
    plt.subplots_adjust(hspace=0.)
    if "pT" in histname:
        ax.xscale("log")
    
    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"], ax=ax)
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()