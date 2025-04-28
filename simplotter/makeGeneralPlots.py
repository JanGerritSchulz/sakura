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
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs

from simplotter.plotterfunctions.plotSimNtuplets import plotSimNtuplets
from simplotter.plotterfunctions.plotEfficiency import plotEfficiency
from simplotter.plotterfunctions.plotEfficiency2D import plotEfficiency2D
from simplotter.plotterfunctions.plotDiscreteHist import plotDiscreteHist
from simplotter.plotterfunctions.plotLayerPairs import plotLayerPairs
from simplotter.plotterfunctions.plotHist import plotHist
from simplotter.plotterfunctions.plotPdgId import plotPdgId

# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

# define function that performs the plotting of all cuts
def makeGeneralPlots(DQMfile, DIR="plots", num_events=None, cmsconfig=None, layerPairs=simplePixelLayerPairs):

    DIRgeneral = DIR + "/general"
    DIRsimNtuplets = DIR + "/simNtuplets"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"]

    # -------------------------------------
    #  general plots
    # -------------------------------------

    # plot the layerPairs
    plotLayerPairs(ROOTFile, directory=DIRgeneral, num_events=num_events, cmsconfig=cmsconfig, layerPairs=layerPairs)

    # produce discrete distributions
    discreteDict = {
        "general/numSimDoubletsPerTrackingParticle" : {"x_label" : "#SimDoublets / TrackingParticle", "y_label" : "#TrackingParticles", "x_lim": (-0.5, 10.5)},
        "general/numLayersPerTrackingParticle" : {"x_label" : "#(hit layers / TrackingParticle)", "y_label" : "#TrackingParticles", "x_lim": (-0.5, 10.5)},
        "general/numSkippedLayers" : {"x_label" : "#(skipped layers)", "y_label" : "#SimDoublets", "x_lim": (-1.5, 5.5)},
}
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], x_lim=p["x_lim"], cmsconfig=cmsconfig)
    
    # plot distributions
    histDict = {
        "general/numTPVsEta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Number of TrackingParticles"},
        "general/numTPVsPt" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Number of TrackingParticles"},
    }
    for h in histDict.keys():
        p = histDict[h]
        plotHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    
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
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    
    # produce 2D efficiency plots
    efficiency2DDict = {
        "general/efficiency_vs_layerPair" : {"x_label" : "Inner layer ID", "y_label" : "Outer layer ID", "z_label":"Total fraction of SimDoublets passing all cuts", "x_layer":True, "y_layer":True},
    }
    for h in efficiency2DDict.keys():
        p = efficiency2DDict[h]
        plotEfficiency2D(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"], cmsconfig=cmsconfig)
    
    # produce rate plots
    ratesDict = {
        "eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$"},
        "pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]"}
    }
    for h in ratesDict.keys():
        p = ratesDict[h]
        plotSimNtuplets(ROOTFile, h, directory=DIRsimNtuplets, 
                         x_label=p["x_label"], cmsconfig=cmsconfig)
        
    
    # plot pdgId
    plotPdgId(ROOTFile, directory=DIR, num_events=num_events, cmsconfig=cmsconfig)
    

    # -------------------------------------
    #  SimNtuplet plots
    # -------------------------------------

    # produce discrete distributions
    discreteDict = {
        "simNtuplets/firstLayerId" : {"x_label" : "First layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
        "simNtuplets/lastLayerId" : {"x_label" : "Last layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
        "simNtuplets/numRecHits" : {"x_label" : "#RecHits in longest SimNtuplet", "y_label" : "#TrackingParticles"},
    }
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)

    # produce efficiency plots (SimNtuplets)
    efficiencyDict = {
        "simNtuplets/alive_fracNumRecHits_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
        "simNtuplets/alive_fracNumRecHits_vs_pT" : {"x_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    }
    for h in efficiencyDict.keys():
        p = efficiencyDict[h]
        plotEfficiency(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
        
            
    # produce 2D efficiency plots
    efficiency2DDict = {
        "simNtuplets/layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":True, "y_layer":True},
        "simNtuplets/alive_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":True, "y_layer":True},
        "simNtuplets/fracAlive_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":True, "y_layer":True},
        "simNtuplets/fracLost_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":True, "y_layer":True},
        "simNtuplets/firstLayerVsEta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "First layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":False, "y_layer":True},
        "simNtuplets/alive_firstLayerVsEta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "First layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":False, "y_layer":True},
        "simNtuplets/fracAlive_firstLayer_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":False, "y_layer":True},
        "simNtuplets/fracLost_firstLayer_vs_eta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":False, "y_layer":True},
        "general/efficiencyTP_vs_eta_phi" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "TrackingParticle azimuthal angle $\phi$ [rad]", "z_label":"Efficiency for TrackingParticles \n(having an alive SimNtuplet)", "x_layer":False, "y_layer":False},
        "general/numLayersVsEtaPt" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : r"TrackingParticle transverse momentum $p_\text{T}$ [GeV]", "z_label":r"$\langle$#layers$\rangle$ hit by TrackingParticle", "x_layer":False, "y_layer":False},
        "general/numLayersVsEta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : r"#layers hit by TrackingParticle", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
        "general/numSkippedLayersVsEta" : {"x_label" : "TrackingParticle pseudorapidity $\eta$", "y_label" : "#(skipped layers)", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
    }
    for h in efficiency2DDict.keys():
        p = efficiency2DDict[h]
        plotEfficiency2D(ROOTFile, h, directory=DIR, cmsconfig=cmsconfig, 
                         x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"])



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce general plots for SimDoublets.")
parser.add_argument("DQMfile", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("config", type=str, help="Path to the cmssw config file that ran the SimDoubletsAnalyzer "+
                    "(please specify the module name of the analyzer under `-a ANALYZERNAME` if it differs from the default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("-d", "--directory", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("-n", "--nevents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")
parser.add_argument("-a", "--analyzer", type=str, default="simDoubletsAnalyzerPhase2", help="Name of the analyzer module "+
                    "(needs to be given if the config file is cmssw config, default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("--llabel", default="Private Work", help="label next to CMS in plot")
parser.add_argument("--rlabel", default=None, help="label displayed in upper right of plot")
parser.add_argument("--com", default=14, help="center of mass displayed in plots")

def main():
    print("="*30)
    print("  Start makeGeneralPlots()")
    print("="*30)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * DQM file:", args.DQMfile)
    print(" * output directory:", args.directory)

    
    if args.config[-3:] == ".py":
        CUTfile = args.directory + '/cutValues.yml'
        print(" * provided config file for cuts (CMSSW config):", args.config)
        print("   -> read layer pairs from CMSSW config")
        print(" * for that use the layer pairs set in the analyzer module named:", args.analyzer)

        # in this case write your own yml based on the given config
        import importlib.util
        #import sys
        spec = importlib.util.spec_from_file_location("process", args.config)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        # get the analyzer
        simDoubletsAnalyzer = getattr(config_module.process, args.analyzer, None)
        if simDoubletsAnalyzer is None:
            raise ValueError("Invalid parameter `analyzer`! In the given CMSSW config, no module with the name `%s` was found" % args.analyzer)
        layerPairs = np.reshape(list(getattr(simDoubletsAnalyzer, "layerPairs")), (-1, 2))
    
    # else, something's wrong
    else:
        raise ValueError("Invalid parameter `config`! Please give either a yaml file with the cut parameters (.yml) or the cmssw config directly (.py).")

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

    cmsconfig = {"llabel" : args.llabel,
                 "rlabel" : args.rlabel,
                 "com" : args.com}
    # produce the plots
    makeGeneralPlots(args.DQMfile, DIR=args.directory, num_events=nevents, cmsconfig=cmsconfig, layerPairs=layerPairs)

    print("="*30)
    print("  End makeGeneralPlots()")
    print("="*30)

if __name__ == "__main__":
    main()