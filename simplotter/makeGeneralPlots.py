# import packages
import uproot
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sakura.tools.plotting_helpers import setStyle, xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from sakura.histograms.Hist2D import Hist2D
from pathlib import Path
import yaml
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs, NonSkippingLayerPairs

# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

def plotLayerPairs(ROOTfile, directory="plots", num_events=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"
    
    # load histograms
    h = Hist2D(ROOTfile["general"], "layerPairs", "Outer layer ID", "Inner layer ID", scale_for_values = 1/num_events)
    
    # create new figure
    fig, ax = plt.subplots()
    
    cmap = mpl.pyplot.get_cmap("plasma")
    cmap.set_under('w')
    cax = h.plot(ax, True, cmap=cmap)
    fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=0, 
                                                                vmax=np.max(h.values)), 
                                    cmap=cmap), ax=ax, extend='min',
                label="Number of SimDoublets" + ylabel_suff)
    ylabel("Outer layer ID")

    Ntot = np.sum(h.values)
    Nrec = 0
    NrecNoSkip = 0
    for pair in simplePixelLayerPairs:
        innerLayer, outerLayer = pair
        plt.plot(np.array([-0.5, -0.5, 0.5, 0.5, -0.5]) * 0. + innerLayer, 
                np.array([-0.5, 0.5, 0.5, -0.5, -0.5]) * 0. + outerLayer, ".r", linewidth=1)
        Nrec += h.values[innerLayer, outerLayer]
    for pair in NonSkippingLayerPairs:
        innerLayer, outerLayer = pair
        NrecNoSkip += h.values[innerLayer, outerLayer]
    plt.plot([-0.5, -0.5, 3.5, 3.5, -0.5], 
            [-0.5, 3.5, 3.5, -0.5, -0.5], "-k")
    plt.plot([3.5, 3.5, 15.5, 15.5, 3.5], 
            [3.5, 15.5, 15.5, 3.5, 3.5], "-k")
    plt.plot([27.5, 27.5, 15.5, 15.5, 27.5], 
            [27.5, 15.5, 15.5, 27.5, 27.5], "-k")
    plt.plot([-0.5, -0.5, 3.5, 3.5, -0.5], 
            [-0.5, 3.5, 3.5, -0.5, -0.5], "w", linestyle=(0,(3,3)))
    plt.plot([3.5, 3.5, 15.5, 15.5, 3.5], 
            [3.5, 15.5, 15.5, 3.5, 3.5], "w", linestyle=(0,(3,3)))
    plt.plot([27.5, 27.5, 15.5, 15.5, 27.5], 
            [27.5, 15.5, 15.5, 27.5, 27.5], "w", linestyle=(0,(3,3)))

    # add the CMS label
    cmslabel(llabel="Private Work", com=14)

    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/layerPairs.png" % (directory))
    plt.close()

    print("\nStatistics from layerPairs:")
    print("Nrec / Ntot = %f / %f = %f" % (Nrec, Ntot, Nrec/Ntot))
    print("Nrec (no skip) / Ntot = %f / %f = %f" % (NrecNoSkip, Ntot, NrecNoSkip/Ntot))
    print("")

# ------------------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------------------

def plotEfficiency(ROOTfile, histname, directory="plots", x_label="", y_label=""):
    
    # load histograms
    hist = Hist(ROOTfile, "general/%s" % (histname))
    
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

# ------------------------------------------------------------------------------------------

# define function that performs the plotting of all cuts
def makeGeneralPlots(DQMfile, DIR="plots", num_events=None):

    DIR += "/general"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"]

    # plot the layerPairs
    plotLayerPairs(ROOTFile, directory=DIR, num_events=num_events)

    # produce discrete distributions
    discreteDict = {
        "numSimDoubletsPerTrackingParticle" : {"x_label" : "Number of SimDoublets per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
        "numLayersPerTrackingParticle" : {"x_label" : "Number of hit layers per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
        "numSkippedLayers" : {"x_label" : "Number of skipped layers", "y_label" : "Number of SimDoublets", "x_lim": (-1.5, 5.5)},
    }
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], x_lim=p["x_lim"])
        
    
    # produce efficiency plots
    efficiencyDict = {
        "efficiencyPerTP_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "efficiencyPerTP_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "efficiencyTP_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Efficiency for TrackingParticles \n(at least 2 passing and connected SimDoublets)"},
        "efficiencyTP_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Efficiency for TrackingParticles \n(at least 2 passing and connected SimDoublets)"},
        "efficiency_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Total fraction of SimDoublets passing all cuts"},
        "efficiency_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Total fraction of SimDoublets passing all cuts"},
    }
    for h in efficiencyDict.keys():
        p = efficiencyDict[h]
        plotEfficiency(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"])



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce general plots for SimDoublets.")
parser.add_argument("DQMfile", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("-d", "--directory", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("-n", "--nevents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")

def main():
    print("="*30)
    print("  Start makeGeneralPlots()")
    print("="*30)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * DQM file:", args.DQMfile)
    print(" * output directory:", args.directory)

    # set number of events
    with uproot.open(args.DQMfile) as ROOTfile:
        if "DQMData/Run 1/EventInfo/processedEvents" in ROOTfile:
            hist = ROOTfile["DQMData/Run 1/EventInfo/processedEvents"]
            nevents = hist.values()[0]
        elif args.nevents > 0:
            nevents = args.nevents
        else:
            nevents = None
    
    if nevents is None:
        print(" * do not scale plots to number of events")
    else:
        print(" * determined number of events:", nevents)
        print("   (scale accordingly)")

    print("\n")        
    # produce the plots
    makeGeneralPlots(args.DQMfile, DIR=args.directory, num_events=nevents)

    print("="*30)
    print("  End makeCutPlots()")
    print("="*30)

if __name__ == "__main__":
    main()