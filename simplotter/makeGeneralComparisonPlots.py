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
def makeGeneralComparisonPlots(CONFIG, DIR="plots", num_events=None):

    DIRgeneral = DIR + "/general"
    DIRsimNtuplets = DIR + "/simNtuplets"

    # open the DQM files and get the legend labels
    ROOTFile = []
    Labels = []
    for key in CONFIG.keys():
        ROOTFile.append(uproot.open(CONFIG[key]["path"])["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"])
        Labels.append(CONFIG[key]["label"])

    # plot the layerPairs
    plotLayerPairs(ROOTFile[0], directory=DIRgeneral, num_events=num_events)

    # produce discrete distributions
    # discreteDict = {
    #     "numSimDoubletsPerTrackingParticle" : {"x_label" : "Number of SimDoublets per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
    #     "numLayersPerTrackingParticle" : {"x_label" : "Number of hit layers per TrackingParticle", "y_label" : "Number of TrackingParticles", "x_lim": (-0.5, 10.5)},
    #     "numSkippedLayers" : {"x_label" : "Number of skipped layers", "y_label" : "Number of SimDoublets", "x_lim": (-1.5, 5.5)},
    # }
    # for h in discreteDict.keys():
    #     p = discreteDict[h]
    #     plotDiscreteHist(ROOTFile, h, directory=DIRgeneral, num_events=num_events, 
    #                      x_label=p["x_label"], y_label=p["y_label"], x_lim=p["x_lim"])
        
    
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
                         x_label=p["x_label"], y_label=p["y_label"], labels=Labels)
    
    # produce rate plots
    # ratesDict = {
    #     "eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$"},
    #     "pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]"}
    # }
    # for h in ratesDict.keys():
    #     p = ratesDict[h]
    #     plotSimNtuplets(ROOTFile, h, directory=DIRsimNtuplets, 
    #                      x_label=p["x_label"])
    
    # produce efficiency plots (SimNtuplets)
    # efficiencyDict = {
    #     "simNtuplets/alive_fracNumRecHits_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    #     "simNtuplets/alive_fracNumRecHits_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    # }
    # for h in efficiencyDict.keys():
    #     p = efficiencyDict[h]
    #     plotEfficiency(ROOTFile, h, directory=DIR, 
    #                      x_label=p["x_label"], y_label=p["y_label"])



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce general plots for SimDoublets.")
parser.add_argument("PLOTTERCONFIG", type=str, help="Path to plotter config file that contains the DQM file names and their legend labels.")
parser.add_argument("-p", "--path", default="", type=str, help="Path to the upper folder if config file contains relative paths. Default is nothing.")
parser.add_argument("-d", "--directory", type=str, default="plots", help="Directory to save the plots in. Default is ./plots")
parser.add_argument("-n", "--nevents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")
parser.add_argument("--llabel", default="Private Work", help="label next to CMS in plot")
parser.add_argument("--rlabel", default=None, help="label displayed in upper right of plot")
parser.add_argument("--com", default=14, help="center of mass displayed in plots")

def main():
    print("="*50)
    print("  Start makeGeneralComparisonPlots()")
    print("="*50)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * config file:", args.PLOTTERCONFIG)
    print(" * output directory:", args.directory)

    # read config file to dictionary
    with open(args.PLOTTERCONFIG, "r") as f_:
        CONFIG = yaml.load(f_, Loader=yaml.FullLoader)
    
    # add the global path to every individual path and save one file name
    lastFilePath = ""
    for key in CONFIG.keys():
        CONFIG[key]["path"] = args.path + "/" + CONFIG[key]["path"]
        lastFilePath = CONFIG[key]["path"]

    # set number of events
    with uproot.open(lastFilePath) as ROOTfile:
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

    cmsconfig = {"llabel" : args.llabel,
                 "rlabel" : args.rlabel,
                 "com" : args.com}
    # produce the plots
    makeGeneralComparisonPlots(CONFIG, DIR=args.directory, num_events=nevents, cmsconfig=cmsconfig)

    print("="*50)
    print("  End makeGeneralComparisonPlots()")
    print("="*50)

if __name__ == "__main__":
    main()