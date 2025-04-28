import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import binomtest
from sakura.tools.plotting_helpers import xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path
from simplotter.dataconfig.pdgIdDict import pdgIdDict


def plotPdgId(ROOTfile, directory="plots", num_events=None, cmsconfig=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"

    histname = "general/numTPVsPdgId"
    pass_histname = "general/pass_numTPVsPdgId"
    
    # load histograms
    hTot = Hist(ROOTfile, histname, scale_for_values = 1/num_events)
    hPass = Hist(ROOTfile, pass_histname, scale_for_values = 1/num_events)

    # loop over the particles in the dict and fill
    x = np.arange(len(pdgIdDict.keys()))
    x_labels = []
    yTot= np.array([])
    yPass= np.array([])
    yEff = []
    yEffErrUp = []
    yEffErrLow = []
    for pdgid in pdgIdDict.keys():
        i = np.argwhere(hTot.edges == pdgid)[0]
        yTot = np.append(yTot, hTot.values[i])
        yPass = np.append(yPass, hPass.values[i])
        x_labels.append(pdgIdDict[pdgid])

        # error calculation with eff
        result = binomtest(k=int(yPass[-1]*num_events), n=int(yTot[-1]*num_events))
        yEff.append(result.statistic)
        yEffErrLow.append(result.proportion_ci(0.683).low)
        yEffErrUp.append(result.proportion_ci(0.683).high)
    

    # create new figure
    fig, (ax, ax2) = plt.subplots(2, height_ratios=[2, 1], sharex=True)
    
    # plot
    xTot = x - 1 / 6
    xPass = x + 1 / 6
    
    ax.bar(xTot, yTot, 1/3, color='darkblue', label="total")
    ax.bar(xPass, yPass, 1/3, color='#5790fc', label="passing")
    ax.legend()

    ax2.axhline(0, linestyle="dashed", linewidth=1.)
    ax2.axhline(1, linestyle="dashed", linewidth=1.)
    ax2.errorbar(x, yEff, xerr=1/3, fmt=".", lolims=yEffErrLow, uplims=yEffErrUp, color='darkblue')

    # fix axes
    ax2.set_ylabel("Efficiency")
    ax2.set_xticks(x, x_labels)
    ax.xaxis.set_tick_params(which='minor',bottom=False,top=False)
    ax2.xaxis.set_tick_params(which='both',bottom=False,top=False)
    ax2.xaxis.set_tick_params(labelbottom=False, labeltop=True)
    ylabel("#TrackingParticles" + ylabel_suff, ax=ax)
    plt.subplots_adjust(hspace=0.15)
    
    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"], ax=ax)
    
    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()