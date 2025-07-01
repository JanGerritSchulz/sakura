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
def makeGeneralPlots(DQMfile, DIR="plots", num_events=None, cmsconfig=None, layerPairs=simplePixelLayerPairs, startingPairs=np.array([])):

    DIRgeneral = DIR + "/general"
    DIRsimNtuplets = DIR + "/SimNtuplets"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimPixelTracks"]

    # -------------------------------------
    #  general plots
    # -------------------------------------
    print("-"*30)
    print(" General plots")
    print("-"*30)

    print("make LayerPair plots...")
    # plot the layerPairs
    plotLayerPairs(ROOTFile, "SimDoublets/layerPairs", 
                   y_label="Outer layer ID", x_label="Inner layer ID", z_label="#SimDoublets",
                   directory=DIR + "/SimDoublets", num_events=num_events, cmsconfig=cmsconfig, layerPairs=layerPairs)
    plotLayerPairs(ROOTFile, "SimNtuplets/longest/firstVsSecondLayer", 
                   y_label="Second layer ID", x_label="First layer ID", z_label="#TrackingParticles",
                   directory=DIRgeneral, num_events=num_events, cmsconfig=cmsconfig, layerPairs=startingPairs, plotname="startingPairs")


    # produce discrete distributions
    print("make discrete plots...")

    discreteDict = {
        "general/numSimDoublets" : {"x_label" : "#SimDoublets / TrackingParticle", "y_label" : "#TrackingParticles", "x_lim": (-0.5, 10.5)},
        "general/numLayers" : {"x_label" : "#(hit layers) / TrackingParticle", "y_label" : "#TrackingParticles", "x_lim": (-0.5, 10.5)},
        "general/numSkippedLayers" : {"x_label" : "#(skipped layers) / TrackingParticle", "y_label" : "#TrackingParticles", "x_lim": (-1.5, 5.5)},
        "SimDoublets/numSkippedLayers" : {"x_label" : "#(skipped layers) / SimDoublet", "y_label" : "#SimDoublets", "x_lim": (-1.5, 5.5)},
}
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], x_lim=p["x_lim"], cmsconfig=cmsconfig)
    

    # plot distributions
    print("make histogram plots...")
    histDict = {
        "general/num_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "#TrackingParticles"},
        "general/num_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "#TrackingParticles"},
        "general/num_vs_phi" : {"x_label" : r"TrackingParticle $\phi$ [rad]", "y_label" : "#TrackingParticles"},
        "general/num_vs_dxy" : {"x_label" : r"TrackingParticle transverse IP to beamspot $d_{xy}$ [cm]", "y_label" : "#TrackingParticles"},
        "general/num_vs_dz" : {"x_label" : r"TrackingParticle longitudinal IP to beamspot $\text{d} z$ [cm]", "y_label" : "#TrackingParticles"},
    }
    for h in histDict.keys():
        p = histDict[h]
        plotHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    

    # produce efficiency plots
    print("make efficiency plots...")

    efficiencyDict = {
        "general/effSimDoubletsPerTP_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "general/effSimDoubletsPerTP_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
        "general/eff_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/eff_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/eff_vs_phi" : {"x_label" : r"TrackingParticle $\phi$ [rad]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/eff_vs_dxy" : {"x_label" : r"TrackingParticle transverse IP to beamspot $d_{xy}$ [cm]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "general/eff_vs_dz" : {"x_label" : r"TrackingParticle longitudinal IP to beamspot $\text{d} z$ [cm]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
        "SimDoublets/eff_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Total fraction of SimDoublets passing all cuts"},
        "SimDoublets/eff_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Total fraction of SimDoublets passing all cuts"},
        "general/effConfigLimit_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Maximum efficiency possible\nbased on layerPairs, startingPairs\nand minNumLayers"},
        "general/effConfigLimit_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Maximum efficiency possible\nbased on layerPairs, startingPairs\nand minHitsPerNtuplet"},
    }
    for h in efficiencyDict.keys():
        p = efficiencyDict[h]
        plotEfficiency(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    

    # produce 2D efficiency plots
    print("make 2D efficiency plots...")

    efficiency2DDict = {
        "SimDoublets/eff_vs_layerPair" : {"x_label" : "Inner layer ID", "y_label" : "Outer layer ID", "z_label":"Total fraction of SimDoublets passing all cuts", "x_layer":True, "y_layer":True},
    }
    for h in efficiency2DDict.keys():
        p = efficiency2DDict[h]
        plotEfficiency2D(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"], cmsconfig=cmsconfig)
    
    # produce rate plots
    print("make rate plots...")

    ratesDict = {
        "eta" : {"x_label" : "TrackingParticle $\eta$"},
        "pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]"}
    }
    for ntuplet in ["longest", "mostAlive"]:
        for h in ratesDict.keys():
            p = ratesDict[h]
            plotSimNtuplets(ROOTFile, ntuplet, h, directory=DIRsimNtuplets, 
                            x_label=p["x_label"], cmsconfig=cmsconfig)
        
    
    # plot pdgId
    plotPdgId(ROOTFile, directory=DIR, num_events=num_events, cmsconfig=cmsconfig)
    

    # -------------------------------------
    #  SimNtuplet plots
    # -------------------------------------
    print("-"*30)
    print(" SimNtuplet plots")
    print("-"*30)

    # produce discrete distributions
    print("make discrete plots...")

    discreteDict = {
        "SimNtuplets/longest/firstLayerId" : {"x_label" : "First layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
        "SimNtuplets/longest/lastLayerId" : {"x_label" : "Last layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
        "SimNtuplets/longest/numRecHits" : {"x_label" : "#RecHits in longest SimNtuplet", "y_label" : "#TrackingParticles"},
    }
    for h in discreteDict.keys():
        p = discreteDict[h]
        plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)


    # produce efficiency plots (SimNtuplets)
    print("make efficiency plots...")

    efficiencyDict = {
        "SimNtuplets/mostAlive/fracNumRecHits_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
        "SimNtuplets/mostAlive/fracNumRecHits_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    }
    for h in efficiencyDict.keys():
        p = efficiencyDict[h]
        plotEfficiency(ROOTFile, h, directory=DIR, 
                         x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
        
            
    # produce 2D efficiency plots
    print("make 2D efficiency plots...")

    efficiency2DDict = {
        "SimNtuplets/longest/layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":True, "y_layer":True},
        "SimNtuplets/mostAlive/pass_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":True, "y_layer":True},
        "SimNtuplets/longest/fracAlive_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":True, "y_layer":True},
        "SimNtuplets/longest/fracLost_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":True, "y_layer":True},
        "SimNtuplets/longest/firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":False, "y_layer":True},
        "SimNtuplets/mostAlive/pass_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":False, "y_layer":True},
        "SimNtuplets/longest/fracAlive_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":False, "y_layer":True},
        "SimNtuplets/longest/fracLost_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":False, "y_layer":True},
        "general/eff_vs_etaPhi" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "TrackingParticle azimuthal angle $\phi$ [rad]", "z_label":"Efficiency for TrackingParticles \n(having an alive SimNtuplet)", "x_layer":False, "y_layer":False},
        "general/numLayers_vs_etaPt" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "z_label":r"$\langle$#layers$\rangle$ hit by TrackingParticle", "x_layer":False, "y_layer":False},
        "general/numLayers_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"#layers hit by TrackingParticle", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
        "general/numRecHits_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"#hits per TrackingParticle", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
        "general/numRecHits_vs_layer" : {"x_label" : "Layer Id", "y_label" : r"#hits per TP and layer", "z_label":"#TrackingParticles", "x_layer":True, "y_layer":False, "plot_ymean":True, "ignore_zero":True},
        "general/numSkippedLayers_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "#(skipped layers)", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
    }
    for h in efficiency2DDict.keys():
        p = efficiency2DDict[h]
        plot_ymean = p["plot_ymean"] if "plot_ymean" in p else False
        ignore_zero = p["ignore_zero"] if "ignore_zero" in p else False
        plotEfficiency2D(ROOTFile, h, directory=DIR, cmsconfig=cmsconfig, 
                         x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"],
                        plot_ymean=plot_ymean, ignore_zero=ignore_zero)



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
        startingPairs = layerPairs[list(getattr(simDoubletsAnalyzer, "startingPairs"))]
    
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
    makeGeneralPlots(args.DQMfile, DIR=args.directory, num_events=nevents, cmsconfig=cmsconfig, layerPairs=layerPairs, startingPairs=startingPairs)

    print("="*30)
    print("  End makeGeneralPlots()")
    print("="*30)

if __name__ == "__main__":
    main()