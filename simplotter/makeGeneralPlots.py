# import packages
import uproot
import multiprocessing
import functools

from simplotter.utils.PlotConfig import PlotConfig
from simplotter.utils.plotttools import setStyle
from simplotter.plotterfunctions.plotHistogram import plotHistogram
# from simplotter.plotterfunctions.plotSimNtuplets import plotSimNtuplets
# from simplotter.plotterfunctions.plotEfficiency import plotEfficiency
# from simplotter.plotterfunctions.plotEfficiency2D import plotEfficiency2D
# from simplotter.plotterfunctions.plotDiscreteHist import plotDiscreteHist
# from simplotter.plotterfunctions.plotLayerPairs import plotLayerPairs
# from simplotter.plotterfunctions.plotHist import plotHist
# from simplotter.plotterfunctions.plotPdgId import plotPdgId


# ------------------------------------------------------------------------------------------
# configure the plots
# ------------------------------------------------------------------------------------------

GENERALPLOTLIST = [
    # discrete 1D plots
    PlotConfig("general/numSimDoublets",       type="discrete1D", isParticles=True, xLabel="#Doublets / TrackingObject",         plotCumSumReco=True),
    PlotConfig("general/numLayers",            type="discrete1D", isParticles=True, xLabel="#(hit layers) / TrackingObject",     plotCumSumReco=True),
    PlotConfig("general/numRecHits",           type="discrete1D", isParticles=True, xLabel="#RecHits / TrackingObject",          plotCumSumReco=True),
    PlotConfig("general/numSkippedLayers",     type="discrete1D", isParticles=True, xLabel="#(skipped layers) / TrackingObject", plotCumSumReco=True),
    PlotConfig("SimDoublets/numSkippedLayers", type="discrete1D", isDoublets=True,  xLabel="#(skipped layers) / Doublet"                            ),

    # 1D plots
    PlotConfig("general/num_vs_eta", type="1D", isParticles=True,  xLabel=r"$\eta$"),
    PlotConfig("general/num_vs_pt",  type="1D", isParticles=True,  xLabel=r"$p_\text{T}$ [GeV]", isLogX=True),
    PlotConfig("general/num_vs_phi", type="1D", isParticles=True,  xLabel=r"$\phi$ [rad]"),
    PlotConfig("general/num_vs_dxy", type="1D", isParticles=True,  xLabel=r"Transverse IP to beamspot $d_{xy}$ [cm]", isLogY=True),
    PlotConfig("general/num_vs_dz",  type="1D", isParticles=True,  xLabel=r"Longitudinal IP to beamspot $\text{d} z$ [cm]"),
    PlotConfig("general/num_vs_chi2",type="1D", isParticles=True,  xLabel=r"Normalized $\chi^2/\text{ndof}$", onlyReco=True, plotCumSumReco=True),

    # profiles
    PlotConfig("SimNtuplets/mostAlive/fracNumRecHits_vs_eta",type="profile", isParticles=True, xLabel=r"$\eta$",             yLabel="Average fractional number of RecHits in\nlongest surviving SimNtuplet\ncompared to the longest one", onlySim=True, plotname="SimNtuplets/fracNumRecHits_vs_eta"),
    PlotConfig("SimNtuplets/mostAlive/fracNumRecHits_vs_pt", type="profile", isParticles=True, xLabel=r"$p_\text{T}$ [GeV]", yLabel="Average fractional number of RecHits in\nlongest surviving SimNtuplet\ncompared to the longest one", onlySim=True, plotname="SimNtuplets/fracNumRecHits_vs_pt", isLogX=True),

    # 2D plots
    PlotConfig("SimDoublets/layerPairs",                 type="2D", isDoublets=True,  xLabel="Inner layer", yLabel="Outer layer",  hasLayerPairsOnXY=True),
    PlotConfig("SimNtuplets/longest/firstVsSecondLayer", type="2D", isParticles=True, xLabel="First layer", yLabel="Second layer", hasLayerPairsOnXY=True, useStartingPairs=True, plotname="general/startingPairs"),
    PlotConfig("general/numSkippedLayers_vs_numLayers",  type="2D", isParticles=True, xLabel="#layers",     yLabel="#(skipped layers)"),
    PlotConfig("general/numSkippedLayers_vs_numRecHits", type="2D", isParticles=True, xLabel="#RecHits",    yLabel="#(skipped layers)"),
    PlotConfig("SimNtuplets/longest/layerSpan",          type="2D", isParticles=True, xLabel="First layer", yLabel="Last layer",   plotname="general/layerSpan"),

    # 2D ratios
    PlotConfig("SimDoublets/layerPairs",                 type="ratio2D", isDoublets=True,  xLabel="Inner layer", yLabel="Outer layer",  hasLayerPairsOnXY=True),
    PlotConfig("SimNtuplets/longest/firstVsSecondLayer", type="ratio2D", isParticles=True, xLabel="First layer", yLabel="Second layer", hasLayerPairsOnXY=True, useStartingPairs=True, plotname="general/startingPairs"),
    PlotConfig("SimNtuplets/longest/layerSpan",          type="ratio2D", isParticles=True, xLabel="First layer", yLabel="Last layer",   plotname="general/layerSpan"),
    PlotConfig("general/numSkippedLayers_vs_numLayers",  type="ratio2D", isParticles=True, xLabel="#layers",     yLabel="#(skipped layers)"),
    PlotConfig("general/numSkippedLayers_vs_numRecHits", type="ratio2D", isParticles=True, xLabel="#RecHits",    yLabel="#(skipped layers)"),

    # SimNtuplet plots
    PlotConfig("mostAlive", type="SimNtuplet", xLabel=r"$p_\text{T}$ [GeV]", plotname="SimNtuplets/mostAliveRate_vs_pt", isLogX=True),
    PlotConfig("mostAlive", type="SimNtuplet", xLabel=r"$\eta$",             plotname="SimNtuplets/mostAliveRate_vs_eta"),
    PlotConfig("longest",   type="SimNtuplet", xLabel=r"$p_\text{T}$ [GeV]", plotname="SimNtuplets/longestRate_vs_pt",   isLogX=True),
    PlotConfig("longest",   type="SimNtuplet", xLabel=r"$\eta$",             plotname="SimNtuplets/longestRate_vs_eta"),
]

# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

# define function that performs the plotting of all cuts
def makeGeneralPlots(dqmFile, nThreads=20, layerPairs=None, startingPairs=None, **kwargs):

    # open the DQM file
    rootFile = uproot.open(dqmFile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth"]

    print("setup multiprocessing...")
    pool = multiprocessing.Pool(nThreads)
    producePlot = functools.partial(plotHistogram, rootFile, layerPairs=layerPairs, startingPairs=startingPairs, **kwargs)

    # -------------------------------------
    #  general plots
    # -------------------------------------
    print("-"*30)
    print(" General plots")
    print("-"*30)

    pool.map(producePlot, GENERALPLOTLIST)
    # print("make LayerPair plots...")
    # # plot the layerPairs
    # plotLayerPairs(rootFile, "SimDoublets/layerPairs", 
    #                y_label="Outer layer ID", x_label="Inner layer ID", z_label="#SimDoublets",
    #                directory=DIR + "/SimDoublets", num_events=num_events, cmsconfig=cmsconfig, layerPairs=layerPairs)
    # plotLayerPairs(rootFile, "SimNtuplets/longest/firstVsSecondLayer", 
    #                y_label="Second layer ID", x_label="First layer ID", z_label="#TrackingParticles",
    #                directory=DIRgeneral, num_events=num_events, cmsconfig=cmsconfig, layerPairs=startingPairs, plotname="startingPairs")


    # produce discrete distributions
       
    

    

    # # plot distributions
    # print("make histogram plots...")
    # histDict = {
    #     "general/num_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "#TrackingParticles"},
    #     "general/num_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "#TrackingParticles"},
    #     "general/num_vs_phi" : {"x_label" : r"TrackingParticle $\phi$ [rad]", "y_label" : "#TrackingParticles"},
    #     "general/num_vs_dxy" : {"x_label" : r"TrackingParticle transverse IP to beamspot $d_{xy}$ [cm]", "y_label" : "#TrackingParticles"},
    #     "general/num_vs_dz" : {"x_label" : r"TrackingParticle longitudinal IP to beamspot $\text{d} z$ [cm]", "y_label" : "#TrackingParticles"},
    # }
    # for h in histDict.keys():
    #     p = histDict[h]
    #     plotHist(rootFile, h, directory=DIR, num_events=num_events, 
    #                      x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    

    # # produce efficiency plots
    # print("make efficiency plots...")

    # efficiencyDict = {
    #     "general/effSimDoubletsPerTP_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
    #     "general/effSimDoubletsPerTP_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Average fraction of SimDoublets \nper TrackingParticle passing all cuts"},
    #     "general/eff_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
    #     "general/eff_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
    #     "general/eff_vs_phi" : {"x_label" : r"TrackingParticle $\phi$ [rad]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
    #     "general/eff_vs_dxy" : {"x_label" : r"TrackingParticle transverse IP to beamspot $d_{xy}$ [cm]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
    #     "general/eff_vs_dz" : {"x_label" : r"TrackingParticle longitudinal IP to beamspot $\text{d} z$ [cm]", "y_label" : "Efficiency for TrackingParticles \n(having an alive SimNtuplet)"},
    #     "SimDoublets/eff_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Total fraction of SimDoublets passing all cuts"},
    #     "SimDoublets/eff_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Total fraction of SimDoublets passing all cuts"},
    #     "general/effConfigLimit_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Maximum efficiency possible\nbased on layerPairs, startingPairs\nand minNumLayers"},
    #     "general/effConfigLimit_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Maximum efficiency possible\nbased on layerPairs, startingPairs\nand minHitsPerNtuplet"},
    # }
    # for h in efficiencyDict.keys():
    #     p = efficiencyDict[h]
    #     plotEfficiency(rootFile, h, directory=DIR, 
    #                      x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
    

    # # produce 2D efficiency plots
    # print("make 2D efficiency plots...")

    # efficiency2DDict = {
    #     "SimDoublets/eff_vs_layerPair" : {"x_label" : "Inner layer ID", "y_label" : "Outer layer ID", "z_label":"Total fraction of SimDoublets passing all cuts", "x_layer":True, "y_layer":True},
    # }
    # for h in efficiency2DDict.keys():
    #     p = efficiency2DDict[h]
    #     plotEfficiency2D(rootFile, h, directory=DIR, 
    #                      x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"], cmsconfig=cmsconfig)
    
    # # produce rate plots
    # print("make rate plots...")

    # ratesDict = {
    #     "eta" : {"x_label" : "TrackingParticle $\eta$"},
    #     "pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]"}
    # }
    # for ntuplet in ["longest", "mostAlive"]:
    #     for h in ratesDict.keys():
    #         p = ratesDict[h]
    #         plotSimNtuplets(rootFile, ntuplet, h, directory=DIRsimNtuplets, 
    #                         x_label=p["x_label"], cmsconfig=cmsconfig)
        
    
    # # plot pdgId
    # plotPdgId(rootFile, directory=DIR, num_events=num_events, cmsconfig=cmsconfig)
    

    # -------------------------------------
    #  SimNtuplet plots
    # -------------------------------------
    # print("-"*30)
    # print(" SimNtuplet plots")
    # print("-"*30)

    # # produce discrete distributions
    # print("make discrete plots...")

    # discreteDict = {
    #     "SimNtuplets/longest/firstLayerId" : {"x_label" : "First layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
    #     "SimNtuplets/longest/lastLayerId" : {"x_label" : "Last layer ID of longest SimNtuplet", "y_label" : "#TrackingParticles"},
    #     "SimNtuplets/longest/numRecHits" : {"x_label" : "#RecHits in longest SimNtuplet", "y_label" : "#TrackingParticles"},
    # }
    # for h in discreteDict.keys():
    #     p = discreteDict[h]
    #     plotDiscreteHist(ROOTFile, h, directory=DIR, num_events=num_events, 
    #                      x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)


    # # produce efficiency plots (SimNtuplets)
    # print("make efficiency plots...")

    # efficiencyDict = {
    #     "SimNtuplets/mostAlive/fracNumRecHits_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    #     "SimNtuplets/mostAlive/fracNumRecHits_vs_pt" : {"x_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "y_label" : "Average fractional number of RecHits in \nlongest surviving SimNtuplet \ncompared to the longest one"},
    # }
    # for h in efficiencyDict.keys():
    #     p = efficiencyDict[h]
    #     plotEfficiency(ROOTFile, h, directory=DIR, 
    #                      x_label=p["x_label"], y_label=p["y_label"], cmsconfig=cmsconfig)
        
            
    # # produce 2D efficiency plots
    # print("make 2D efficiency plots...")

    # efficiency2DDict = {
    #     "SimNtuplets/longest/layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":True, "y_layer":True},
    #     "SimNtuplets/mostAlive/pass_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":True, "y_layer":True},
    #     "SimNtuplets/longest/fracAlive_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":True, "y_layer":True},
    #     "SimNtuplets/longest/fracLost_layerSpan" : {"x_label" : "First layer ID", "y_label" : "Last layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":True, "y_layer":True},
    #     "SimNtuplets/longest/firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Longest SimNtuplet of TPs", "x_layer":False, "y_layer":True},
    #     "SimNtuplets/mostAlive/pass_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Longest alive SimNtuplet of TPs", "x_layer":False, "y_layer":True},
    #     "SimNtuplets/longest/fracAlive_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing reconstructed", "x_layer":False, "y_layer":True},
    #     "SimNtuplets/longest/fracLost_firstLayer_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "First layer ID", "z_label":"Fraction of longest SimNtuplet of TPs\nbeing lost in reconstruction", "x_layer":False, "y_layer":True},
    #     "general/eff_vs_etaPhi" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "TrackingParticle azimuthal angle $\phi$ [rad]", "z_label":"Efficiency for TrackingParticles \n(having an alive SimNtuplet)", "x_layer":False, "y_layer":False},
    #     "general/numLayers_vs_etaPt" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"TrackingParticle $p_\text{T}$ [GeV]", "z_label":r"$\langle$#layers$\rangle$ hit by TrackingParticle", "x_layer":False, "y_layer":False},
    #     "general/numLayers_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"#layers hit by TrackingParticle", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
    #     "general/numRecHits_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : r"#hits per TrackingParticle", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
    #     "general/numRecHits_vs_layer" : {"x_label" : "Layer Id", "y_label" : r"#hits per TP and layer", "z_label":"#TrackingParticles", "x_layer":True, "y_layer":False, "plot_ymean":True, "ignore_zero":True},
    #     "general/numSkippedLayers_vs_eta" : {"x_label" : "TrackingParticle $\eta$", "y_label" : "#(skipped layers)", "z_label":"#TrackingParticles", "x_layer":False, "y_layer":False},
    # }
    # for h in efficiency2DDict.keys():
    #     p = efficiency2DDict[h]
    #     plot_ymean = p["plot_ymean"] if "plot_ymean" in p else False
    #     ignore_zero = p["ignore_zero"] if "ignore_zero" in p else False
    #     plotEfficiency2D(ROOTFile, h, directory=DIR, cmsconfig=cmsconfig, 
    #                      x_label=p["x_label"], y_label=p["y_label"], z_label=p["z_label"], x_layer=p["x_layer"], y_layer=p["y_layer"],
    #                     plot_ymean=plot_ymean, ignore_zero=ignore_zero)



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce general plots for SimDoublets.")
parser.add_argument("DQM", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("config", type=str, help="Path to the cmssw config file that ran the SimDoubletsAnalyzer "+
                    "(please specify the module name of the analyzer under `-a ANALYZERNAME` if it differs from the default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("-d", "--directory", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("-n", "--nEvents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")
parser.add_argument("-a", "--analyzer", type=str, default="simDoubletsAnalyzerPhase2", help="Name of the analyzer module "+
                    "(needs to be given if the config file is cmssw config, default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("--llabel", default="Private Work", help="label next to CMS in plot")
parser.add_argument("--rlabel", default=None, help="label displayed in upper right of plot")
parser.add_argument("--com", default=14, help="center of mass displayed in plots")
parser.add_argument("--fullXRange", default=False, action='store_true', help="flag to have full x range displayed in plots (including all empty bins)")
parser.add_argument("--onlySim", default=False, action='store_true', help="flag to plot only the Sim distribtuions (no Reco)")
parser.add_argument("--onlyReco", default=False, action='store_true', help="flag to plot only the Reco distribtuions (no Sim)")
parser.add_argument("--pdf", default=False, action='store_true', help="flag to save the plots in pdf instead of png")
parser.add_argument("-t", "--nThreads", default=20, type=int,  help="Number of threads used for parallel plotting")

def main():
    print("="*30)
    print("  Start makeGeneralPlots()")
    print("="*30)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * DQM file:", args.DQM)

    
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
        layerPairs = list(getattr(simDoubletsAnalyzer.geometry, "pairGraph"))
        layerPairs = [layerPairs[2*i:2*i+2] for i in range(int(len(layerPairs)/2))]
        startingPairsIndex = list(getattr(simDoubletsAnalyzer.geometry, "startingPairs"))
        startingPairs = [layerPairs[i] for i in startingPairsIndex]
        nEventsFromConfig = config_module.process.maxEvents.input.value()
    
    # else, something's wrong
    else:
        raise ValueError("Invalid parameter `config`! Please give either a yaml file with the cut parameters (.yml) or the cmssw config directly (.py).")

    print(" * output directory:", args.directory)

    # set number of events
    with uproot.open(args.DQM) as ROOTfile:
        if "DQMData/Run 1/EventInfo/processedEvents" in ROOTfile:
            hist = ROOTfile["DQMData/Run 1/EventInfo/processedEvents"]
            nEvents = hist.values()[0]
        elif nEventsFromConfig > 0:
            nEvents = nEventsFromConfig
        elif args.nEvents > 0:
            nEvents = args.nEvents
        else:
            nEvents = None
    
    if nEvents is None:
        print(" * do not scale plots to number of events")
    else:
        print(" * determined number of events:", nEvents)
        print("   (scale accordingly)")
    if args.onlySim and args.onlyReco:
        raise ValueError("Both `--onlySim` and `--onlyReco` are specified. They are mutually exclusive. Please remove one of the two flags.")
    elif args.onlySim:
        plotSim, plotReco = True, False
        print(" * plot only the Sim distributions")
    elif args.onlyReco:
        plotSim, plotReco = False, True
        print(" * plot only the Reco distributions")
    else:
        plotSim, plotReco = True, True
        print(" * plot both the Sim and Reco distributions")
    
    if args.fullXRange:
        limitXRange = False
    else:
        limitXRange = True
        print(" * limit the x range of the plots to the non-empty bins")

    print(" * plot with %i threads in parallel" % args.nThreads)
    print(" * output directory for plots:", args.directory)
    print("\n")        

    cmsConfig = {"llabel" : args.llabel,
                 "rlabel" : args.rlabel,
                 "com" : args.com}
    # produce the plots
    makeGeneralPlots(args.DQM, layerPairs=layerPairs, startingPairs=startingPairs, 
                     nThreads=args.nThreads, directory=args.directory, 
                     nEvents=nEvents, cmsConfig=cmsConfig, limitXRange=limitXRange,
                     plotSim=plotSim, plotReco=plotReco
                     )

    print("="*30)
    print("  End makeGeneralPlots()")
    print("="*30)

if __name__ == "__main__":
    main()