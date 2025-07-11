# import packages
import uproot
import numpy as np
import yaml
from pathlib import Path
import multiprocessing
import functools
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs
from simplotter.plotterfunctions.plotCutParameter import plotCutParameter
from simplotter.utils.CellCut import CellCut
from simplotter.utils.plotttools import setStyle
from simplotter.utils.utils import valToLatexStr

CUTlist_vectors = ["cellMinz", "cellMaxz", "cellPhiCuts", "cellMaxr", "CAThetaCuts", "dcaCuts"]
CUTlist_scalars = ["cellMinYSizeB1", "cellMinYSizeB2", 
                   "cellMaxDYSize12", "cellMaxDYSize", "cellMaxDYPred", "cellZ0Cut", "cellPtCut",
                   "ptmin", "hardCurvCut"]

# ------------------------------------------------------------------------------------------

# function for get the global and layer-pair dependent cuts
def getCutParameters(cutFile="cutParameters/currentCuts.yml"):
    """
    In this function, the CA parameter cuts are configured. The actual cut values are taken from a given
    yaml file.
    """
    with open(cutFile, "r") as f_:
        CUTS = yaml.load(f_, Loader=yaml.FullLoader)

    layerPairs = CUTS["layerPairs"]
    nLayers = len(CUTS["CAThetaCuts"])

    GlobalCellCuts = {
        # doublet cuts
        "z0" :      CellCut("z0",       isDoubletCut=True, max=CUTS["cellZ0Cut"],       label="Longitudinal impact parameter $z_0$ [cm]"),
        "pTFromR" : CellCut("pTFromR",  isDoubletCut=True, min=CUTS["cellPtCut"],       label=r"Transverse momentum $p_\text{T}$ of circle" + "\nthrough SimDoublet and beamspot [GeV]", isLog=True),
        "DYPred":   CellCut("DYPred",   isDoubletCut=True, max=CUTS["cellMaxDYPred"],   label="Absolute difference between\nactual and expected inner cluster size [pixels]"),
        "DYsize12": CellCut("DYsize12", isDoubletCut=True, max=CUTS["cellMaxDYSize12"], label="Absolute difference between sizes \n of inner and outer cluster [pixels]"),
        "DYsize":   CellCut("DYsize",   isDoubletCut=True, max=CUTS["cellMaxDYSize"],   label="Absolute difference between sizes \n of inner and outer cluster [pixels]"),
        "YsizeB1":  CellCut("YsizeB1",  isDoubletCut=True, min=CUTS["cellMinYSizeB1"],  label="Size in $z$-direction of inner cluster [pixels]"),
        "YsizeB2":  CellCut("YsizeB2",  isDoubletCut=True, min=CUTS["cellMinYSizeB2"],  label="Size in $z$-direction of inner cluster [pixels]"),
        # connection cuts
        "hardCurv" : CellCut("hardCurv", isConnectionCut=True, max=CUTS["hardCurvCut"], label=r"Curvature $\frac{1}{|R|}$ [1/cm]"),
    }

    LayerCellCuts = {
        # doublet cuts
        "dr":       [CellCut("dr",      isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1], max=CUTS["cellMaxr"][i],                          label=r"$\text{d}r$ between outer and inner RecHit [cm]") for i, lp in enumerate(layerPairs)],
        "dz":       [CellCut("dz",      isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1],                                                   label=r"$\text{d}z$ between outer and inner RecHit [cm]") for i, lp in enumerate(layerPairs)],
        "idphi":    [CellCut("idphi",   isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1], max=CUTS["cellPhiCuts"][i],                       label=r"Absolute integer $\text{d}\phi$ between outer and inner RecHit") for i, lp in enumerate(layerPairs)],
        "innerZ":   [CellCut("innerZ",  isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1], min=CUTS["cellMinz"][i], max=CUTS["cellMaxz"][i], label="$z$-coordinate of inner RecHit [cm]") for i, lp in enumerate(layerPairs)],
        "innerR":   [CellCut("innerR",  isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1],                                                   label="$r$-coordinate of inner RecHit [cm]") for i, lp in enumerate(layerPairs)],
        "outerZ":   [CellCut("outerZ",  isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1],                                                   label="$z$-coordinate of outer RecHit [cm]") for i, lp in enumerate(layerPairs)],
        "outerR":   [CellCut("outerR",  isDoubletCut=True, isLayerDependent=True, innerLayer=lp[0], outerLayer=lp[1],                                                   label="$r$-coordinate of outer RecHit [cm]") for i, lp in enumerate(layerPairs)],
        # connection cuts
        "CAThetaCut_over_ptmin" :   [CellCut("CAThetaCut_over_ptmin",   isLog=True, isConnectionCut=True, isLayerDependent=True, innerLayer=l, max=CUTS["CAThetaCuts"][l] / CUTS["ptmin"],  label=r"CATheta cut variable $\frac{2 A}{|d\cdot \text{d} r|}$",                yLabelAddition="\n(with centered RecHit in layer %i)" % l, cutLabelAddition=r"\text{CATheta/ptmin}$" + "\n $= " + valToLatexStr(CUTS["CAThetaCuts"][l]) +" / " + valToLatexStr(CUTS["ptmin"]) + "=") for l in range(nLayers)],
        "dcaCut" :                  [CellCut("dcaCut",                  isLog=True, isConnectionCut=True, isLayerDependent=True, innerLayer=l, max=CUTS["dcaCuts"][l],                      label="Transverse distance to the beamspot\nat point of closest approach [cm]", yLabelAddition="\n(with inner RecHit in layer %i)" % l) for l in range(nLayers)],
    }

    return GlobalCellCuts, LayerCellCuts


# define function that performs the plotting of all cuts
def makeCutPlots(dqmFile, cutFile="cutParameters/currentCuts.yml", cut=None, nThreads=20, **kwargs):


    # open the DQM file
    rootFile = uproot.open(dqmFile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth"]

    # get cut parameters and values
    GlobalCellCuts, LayerCellCuts = getCutParameters(cutFile)

    print("setup multiprocessing...")
    pool = multiprocessing.Pool(nThreads)
    producePlot = functools.partial(plotCutParameter, rootFile, **kwargs)

    # if no cut is given, plot all of them
    if cut is None:

        print("make global cell cut plots...")
        pool.map(producePlot, GlobalCellCuts.values())
        # the above is the parallelized version of:
        # for cut in GlobalCellCuts.keys():
        #     cellCut = GlobalCellCuts[cut]
        #     plotCutParameter(rootFile, cellCut, **kwargs)

        print("make layer-dependent cell cut plots")
        for cut in LayerCellCuts.keys():
            print("  for %s..." % cut)
            pool.map(producePlot, LayerCellCuts[cut])
            # the above is the parallelized version of:
            # for cellCut in LayerCellCuts[cut]:
            #     plotCutParameter(rootFile, cellCut, **kwargs)
        
        
    
    # otherwise just plot the given cut parameter
    else:
        if cut in GlobalCellCuts.keys():
            cellCut = GlobalCellCuts[cut]
            plotCutParameter(rootFile, cellCut, **kwargs)
        
        elif cut in LayerCellCuts.keys():
            pool.map(producePlot, LayerCellCuts[cut])
            # the above is the parallelized version of:
            # for cellCut in LayerCellCuts[cut]:
            #     plotCutParameter(rootFile, cellCut, **kwargs)
        
        else:
            raise ValueError('Invalid parameter `cut`! Specify the cut parameter you want to plot from the list below or `None` to plot all of them.'
                             +'\nList of valid `cut` parameters: ' + str(list(GlobalCellCuts.keys()) + list(LayerCellCuts.keys())))
    
    pool.close()



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce cut distribution plots for SimDoublets including total and passing doublets + cut value.")
parser.add_argument("DQM", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("config", type=str, help="Path to config file for applied cut values. "+
                    "Supports yaml file with all cuts and layerPairs or the cmssw config file that ran the SimDoubletsAnalyzer or the PixelTrackSoAProducer "+
                    "(please specify the module name of the analyzer under `-a ANALYZERNAME` if it differs from the default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("-d", "--directory", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("-c", "--cut", default=None, help="cut parameter to be plotted (by default all are plotted)")
parser.add_argument("-n", "--nEvents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")
parser.add_argument("-a", "--analyzer", type=str, default="simDoubletsAnalyzerPhase2", help="Name of the analyzer module "+
                    "(needs to be given if the config file is cmssw config, default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("--llabel", default="Private Work", help="label next to CMS in plot")
parser.add_argument("--rlabel", default=None, help="label displayed in upper right of plot")
parser.add_argument("--com", default=14, help="center of mass displayed in plots")
parser.add_argument("--fullXRange", default=False, action='store_true', help="flag to have full x range displayed in plots (including all empty bins)")
parser.add_argument("--onlySimDoublets", default=False, action='store_true', help="flag to plot only the SimDoublets distribtuions (no RecoDoublets)")
parser.add_argument("--onlyRecoDoublets", default=False, action='store_true', help="flag to plot only the RecoDoublets distribtuions (no SimDoublets)")
parser.add_argument("--pdf", default=False, action='store_true', help="flag to save the plots in pdf instead of png")
parser.add_argument("-t", "--nThreads", default=20, type=int,  help="Number of threads used for parallel plotting")

def main():
    print("="*30)
    print("  Start makeCutPlots()")
    print("="*30)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * DQM file:", args.DQM)

    # if the given config is yaml, it should already contain the cut values in the correct format
    if args.config[-4:] == ".yml":
        print(" * provided config file for cuts (yaml):", args.config)
        cutFile = args.config
        nEventsFromConfig = -1

    # elif python format, assume it is a cmssw config file
    elif args.config[-3:] == ".py":
        cutFile = args.directory + '/cutValues.yml'
        print(" * provided config file for cuts (CMSSW config):", args.config)
        print("   -> read cut parameters from CMSSW config and create yaml config here:")
        print("     ", cutFile)
        print(" * for that use the cuts set in the analyzer module named:", args.analyzer)

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
        layerPairs = list(getattr(simDoubletsAnalyzer, "layerPairs"))
        layerPairs = [layerPairs[2*i:2*i+2] for i in range(int(len(layerPairs)/2))]
        startingPairsIndex = list(getattr(simDoubletsAnalyzer, "startingPairs"))
        CUTdict = {
            cutname: getattr(simDoubletsAnalyzer, cutname).value() for cutname in CUTlist_scalars
        } | {
            cutname: list(getattr(simDoubletsAnalyzer, cutname)) for cutname in CUTlist_vectors
        } | {
            "layerPairs": layerPairs,
            "startingPairsIndex": startingPairsIndex,
            "startingPairs": [layerPairs[i] for i in startingPairsIndex]
        }

        nEventsFromConfig = config_module.process.maxEvents.input.value()

        Path(args.directory).mkdir(parents=True, exist_ok=True)
        with open(cutFile, 'w') as outfile:
            yaml.dump(CUTdict, outfile, default_flow_style=False)
    
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

    if args.cut is None:
        print(" * plot all distributions of cut parameters")
    else:
        print(" * plot only the distribution for the cut:", args.cut)
    
    if args.onlySimDoublets and args.onlyRecoDoublets:
        raise ValueError("Both `--onlySimDoublets` and `--onlyRecoDoublets` are specified. They are mutually exclusive. Please remove one of the two flags.")
    elif args.onlySimDoublets:
        plotSimDoublets, plotRecoDoublets = True, False
        print(" * plot only the SimDoublet distributions")
    elif args.onlyRecoDoublets:
        plotSimDoublets, plotRecoDoublets = False, True
        print(" * plot only the RecoDoublet distributions")
    else:
        plotSimDoublets, plotRecoDoublets = True, True
        print(" * plot both the SimDoublet and RecoDoublet distributions")
    
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
    makeCutPlots(args.DQM, cutFile=cutFile, cut=args.cut, nThreads=args.nThreads,
                 directory=args.directory, nEvents=nEvents,
                 cmsConfig=cmsConfig, limitXRange=limitXRange,
                 plotSimDoublets=plotSimDoublets, plotRecoDoublets=plotRecoDoublets
                 )

    print("="*30)
    print("  End makeCutPlots()")
    print("="*30)

if __name__ == "__main__":
    main()