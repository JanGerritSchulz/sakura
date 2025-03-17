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

from simplotter.plotterfunctions.plotSimNtuplets import plotSimNtuplets
from simplotter.plotterfunctions.plotEfficiency import plotEfficiency
from simplotter.plotterfunctions.plotDiscreteHist import plotDiscreteHist
from simplotter.plotterfunctions.plotLayerPairs import plotLayerPairs

# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

# define function that performs the plotting of all cuts
def makeGeneralPlots(DQMfile, DIR="plots", num_events=None):

    DIRgeneral = DIR + "/general"
    DIRsimNtuplets = DIR + "/simNtuplets"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"]

    # plot the layerPairs
    plotLayerPairs(ROOTFile, directory=DIRgeneral, num_events=num_events)

    # produce discrete distributions
    discreteDict = {
        "numSimDoubletsPerTrackingParticle" : {"x_label" : "Number of SimDoublets per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
        "numLayersPerTrackingParticle" : {"x_label" : "Number of hit layers per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
        "numSkippedLayers" : {"x_label" : "Number of skipped layers", "y_label" : "Number of SimDoublets", "x_lim": (-1.5, 5.5)},
    }
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIRgeneral, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], x_lim=p["x_lim"])
        
    
    # produce efficiency plots
    efficiencyDict = {
        "general/efficiencyPerTP_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "general/efficiencyPerTP_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "general/efficiencyTP_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/efficiencyTP_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/efficiency_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Total fraction of SimDoublets passing all cuts"},
        "general/efficiency_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Total fraction of SimDoublets passing all cuts"},
    }
    for h in efficiencyDict.keys():
        p = efficiencyDict[h]
        plotEfficiency(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"])
    
    # produce rate plots
    ratesDict = {
        "eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$"},
        "pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]"}
    }
    for h in ratesDict.keys():
        p = ratesDict[h]
        plotSimNtuplets(ROOTFile, h, directory=DIRsimNtuplets, 
                         x_label=p["x_label"])
    
    # produce efficiency plots (SimNtuplets)
    efficiencyDict = {
        "simNtuplets/alive_fracNumRecHits_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
        "simNtuplets/alive_fracNumRecHits_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
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