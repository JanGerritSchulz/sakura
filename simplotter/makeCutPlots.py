# import packages
import uproot
import matplotlib.pyplot as plt
import numpy as np
from sakura.tools.plotting_helpers import setStyle, xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path
import yaml
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs

CUTlist_vectors = ["cellMinz", "cellMaxz", "cellPhiCuts", "cellMaxr"]
CUTlist_scalars = ["cellMinYSizeB1", "cellMinYSizeB2", 
           "cellMaxDYSize12", "cellMaxDYSize", "cellMaxDYPred", "cellZ0Cut", "cellPtCut",
           "CAThetaCutBarrel", "CAThetaCutForward", "ptmin", "hardCurvCut", 
           "dcaCutInnerTriplet", "dcaCutOuterTriplet"]


# ------------------------------------------------------------------------------------------
# main function for plotting
# ------------------------------------------------------------------------------------------

def plotCutParameter(ROOTfile, histname, cellCutType, cellCutMin=-np.inf, cellCutMax=np.inf, innerLayer=None, outerLayer=None, x_label="", directory="plots", num_events=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"
    
    if innerLayer is not None:
        subfolder = "lp_%i_%i/" % (innerLayer, outerLayer)
    else:
        subfolder = "global/"
    
    # load histograms
    hTot = Hist(ROOTfile, "cutParameters/" + subfolder + histname, scale_for_values = 1/num_events)
    hPass = Hist(ROOTfile, "cutParameters/%spass_%s" % (subfolder,histname), scale_for_values = 1/num_events)
    
    # create new figure
    fig, ax = plt.subplots()
    
    # plot
    y = hTot.values
    x = hTot.edges
    icutMax = np.argmax(x>cellCutMax) if (cellCutType=="max" or cellCutType=="both") else None
    icutMin = np.argmin(x<cellCutMin) if (cellCutType=="min" or cellCutType=="both") else None
    
    if (cellCutType=="max"):
        plt.stairs(y[icutMin:icutMax],np.append(x[icutMin:icutMax], [cellCutMax]), fill=True, color='#5790fc', alpha=0.5, label="doublets passing this cut")
    elif (cellCutType=="min"):
        plt.stairs(y[icutMin-1:icutMax],np.append([cellCutMin], x[icutMin:icutMax]), fill=True, color='#5790fc', alpha=0.5, label="doublets passing this cut")
    elif (cellCutType=="both"):
        plt.stairs(y[icutMin-1:icutMax],np.append(np.append([cellCutMin], x[icutMin:icutMax]), [cellCutMax]), fill=True, color='#5790fc', alpha=0.5, label="doublets passing this cut")
    plt.stairs(hPass.values, x, fill=True, color='#5790fc', label="doublets passing all cuts")
    plt.stairs(y, x, color="darkblue", label="all doublets")
    #plt.stairs(y[icut-1:icut],x[icut-1:icut+1], color="darkblue", alpha=0.3, fill=True)
    
    if (cellCutType=="max"):
        plt.axvline(cellCutMax, color="darkblue", linestyle="--", label="cut value")
    elif (cellCutType=="min"):
        plt.axvline(cellCutMin, color="darkblue", linestyle="--", label="cut value")
    elif (cellCutType=="both"):
        plt.axvline(cellCutMax, color="darkblue", linestyle="--")
        plt.axvline(cellCutMin, color="darkblue", linestyle="--", label="cut values")
    
    # fix axes
    ylabel("Number of SimDoublets" + ylabel_suff)
    xlabel(x_label)
    if "pT" in histname:
        plt.xscale("log")
    
    # add the CMS label
    cmslabel(llabel="Private Work", com=14)
    
    # save and show the figure
    if innerLayer is not None:
        plt.legend(title = "Layer pair (%i,%i)" % (innerLayer, outerLayer))
        Path("%s/%s" % (directory, histname)).mkdir(parents=True, exist_ok=True)
        savefig("%s/%s/%s.png" % (directory, histname, subfolder[:-1]))
    else:
        plt.legend()
        Path("%s" % (directory)).mkdir(parents=True, exist_ok=True)
        savefig("%s/%s.png" % (directory, histname))
    plt.close()

# ------------------------------------------------------------------------------------------

def plotConnectionCutParameter(ROOTfile, histname, cellCutType, cellCutMin=-np.inf, cellCutMax=np.inf, innerLayer=None, outerLayer=None, x_label="", y_label_add="", directory="plots", num_events=None):
    if num_events is None:
        num_events = 1
        ylabel_suff = ""
    else:
        ylabel_suff = " / event"
    
    if innerLayer is not None:
        subfolder = "lp_%i_%i/" % (innerLayer, outerLayer)
    else:
        subfolder = "connectionCuts/"
    
    # load histograms
    hTot = Hist(ROOTfile, "cutParameters/" + subfolder + histname, scale_for_values = 1/num_events)
    hPass = Hist(ROOTfile, "cutParameters/%spass_%s" % (subfolder,histname), scale_for_values = 1/num_events)
    
    # create new figure
    fig, ax = plt.subplots()

    legend_title = None
    if "CATheta" in histname:
        legend_title = "cut at CATheta / ptmin\n= %.4f / %.2f = %.4f" % (cellCutMax[0], cellCutMax[1], cellCutMax[0] / cellCutMax[1])
        cellCutMax = cellCutMax[0] / cellCutMax[1]
    
    # plot
    y = hTot.values
    x = hTot.edges
    icutMax = np.argmax(x>cellCutMax) if (cellCutType=="max" or cellCutType=="both") else None
    icutMin = np.argmin(x<cellCutMin) if (cellCutType=="min" or cellCutType=="both") else None
    
    if (cellCutType=="max"):
        plt.stairs(y[icutMin:icutMax],np.append(x[icutMin:icutMax], [cellCutMax]), fill=True, color='#5790fc', alpha=0.5, label="connections passing this cut")
    elif (cellCutType=="min"):
        plt.stairs(y[icutMin-1:icutMax],np.append([cellCutMin], x[icutMin:icutMax]), fill=True, color='#5790fc', alpha=0.5, label="connections passing this cut")
    elif (cellCutType=="both"):
        plt.stairs(y[icutMin-1:icutMax],np.append(np.append([cellCutMin], x[icutMin:icutMax]), [cellCutMax]), fill=True, color='#5790fc', alpha=0.5, label="connections passing this cut")
    plt.stairs(hPass.values, x, fill=True, color='#5790fc', label="connections passing all cuts")
    plt.stairs(y, x, color="darkblue", label="all connections")
    #plt.stairs(y[icut-1:icut],x[icut-1:icut+1], color="darkblue", alpha=0.3, fill=True)
    
    if (cellCutType=="max"):
        plt.axvline(cellCutMax, color="darkblue", linestyle="--", label="cut value")
    elif (cellCutType=="min"):
        plt.axvline(cellCutMin, color="darkblue", linestyle="--", label="cut value")
    elif (cellCutType=="both"):
        plt.axvline(cellCutMax, color="darkblue", linestyle="--")
        plt.axvline(cellCutMin, color="darkblue", linestyle="--", label="cut values")
    
    # fix axes
    ylabel("Number of SimDoublet connections" + y_label_add + ylabel_suff)
    xlabel(x_label)
    if "hardCurv" not in histname:
        plt.xscale("log")
    
    # add the CMS label
    cmslabel(llabel="Private Work", com=14)
    
    # save and show the figure
    if innerLayer is not None:
        plt.legend(title = "Layer pair (%i,%i)" % (innerLayer, outerLayer) + " " + legend_title)
        Path("%s/connectionCuts/%s" % (directory, histname)).mkdir(parents=True, exist_ok=True)
        savefig("%s/connectionCuts/%s/%s.png" % (directory, histname, subfolder[:-1]))
    else:
        plt.legend(title=legend_title)
        Path("%s/connectionCuts" % (directory)).mkdir(parents=True, exist_ok=True)
        savefig("%s/connectionCuts/%s.png" % (directory, histname))
    plt.close()

# ------------------------------------------------------------------------------------------

# function for get the global and layer-pair dependent cuts
def getCutParameters(CUTfile="cutParameters/currentCuts.yml"):
    with open(CUTfile, "r") as f_:
        CUTS = yaml.load(f_, Loader=yaml.FullLoader)

    GlobalCutParameters = {
        "z0" : ["max", -np.inf, CUTS["cellZ0Cut"], "Longitudinal impact parameter $z_0$ [cm]"],
        "pTFromR" : ["min", CUTS["cellPtCut"], np.inf, r"Transverse momentum $p_\text{T}$ of circle" + "\nthrough SimDoublet and beamspot [GeV]"],
        "DYPred": ["max", -np.inf, CUTS["cellMaxDYPred"], "Absolute difference between\nactual and expected inner cluster size [pixels]"],
        "DYsize12": ["max", -np.inf, CUTS["cellMaxDYSize12"], "Absolute difference between sizes \n of inner and outer cluster [pixels]"],
        "DYsize": ["max", -np.inf, CUTS["cellMaxDYSize"], "Absolute difference between sizes \n of inner and outer cluster [pixels]"],
        "YsizeB1": ["min", CUTS["cellMinYSizeB1"], np.inf, "Size in $z$-direction of inner cluster [pixels]"],
        "YsizeB2": ["min", CUTS["cellMinYSizeB2"], np.inf, "Size in $z$-direction of inner cluster [pixels]"],
    }

    LayerPairCutParameters = {
        "dr": ["max", None, CUTS["cellMaxr"], r"$\text{d}r$ between outer and inner RecHit [cm]"],
        "idphi": ["max", None, CUTS["cellPhiCuts"], r"Absolute integer $\text{d}\phi$ between outer and inner RecHit"],
        "innerZ": ["both", CUTS["cellMinz"], CUTS["cellMaxz"], "$z$-coordinate of inner RecHit [cm]"],
    }

    ConnectionCutParameters = {
        "CAThetaBarrel_over_ptmin" : ["max", -np.inf, (CUTS["CAThetaCutBarrel"], CUTS["ptmin"]), r"CATheta cut variable $\frac{2 A}{|d\cdot \text{d} r|}$", "\nwith centered RecHit in barrel"],
        "CAThetaForward_over_ptmin" : ["max", -np.inf, (CUTS["CAThetaCutForward"], CUTS["ptmin"]), r"CATheta cut variable $\frac{2 A}{|d\cdot \text{d} r|}$", "\nwith centered RecHit in endcap"],
        "hardCurv" : ["max", -np.inf, CUTS["hardCurvCut"], r"Curvature $\frac{1}{|R|}$ [1/cm]", ""],
        "dcaInner" : ["max", -np.inf, CUTS["dcaCutInnerTriplet"], "Transverse distance to the beamspot\nat point of closest approach [cm]", ""],
        "dcaOuter" : ["max", -np.inf, CUTS["dcaCutOuterTriplet"], "Transverse distance to the beamspot\nat point of closest approach [cm]", ""],
    }

    return GlobalCutParameters, LayerPairCutParameters, ConnectionCutParameters


# define function that performs the plotting of all cuts
def makeCutPlots(DQMfile, CUTfile="cutParameters/currentCuts.yml", DIR="plots", cut=None, num_events=None):

    DIR += "/cutParameters"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"]

    # get cut parameters and values
    GlobalCutParameters, LayerPairCutParameters, ConnectionCutParameters = getCutParameters(CUTfile)

    # if no cut is given, plot all of them
    if cut is None:
        for histname in GlobalCutParameters.keys():
            cutType, cutMin, cutMax, label = GlobalCutParameters[histname]
            plotCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax, x_label=label, 
                             directory=DIR, num_events=num_events)

        for histname in LayerPairCutParameters.keys():
            cutType, cutMinArr, cutMaxArr, label = LayerPairCutParameters[histname]
            for i, pair in enumerate(simplePixelLayerPairs):
                cutMin = -np.inf if cutMinArr is None else cutMinArr[i]
                cutMax = cutMaxArr[i]
                plotCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax, 
                                innerLayer=pair[0], outerLayer=pair[1], x_label=label, directory=DIR, num_events=num_events)
        
        for histname in ConnectionCutParameters.keys():
            cutType, cutMin, cutMax, label, label_add = ConnectionCutParameters[histname]
            plotConnectionCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax, 
                                x_label=label, y_label_add=label_add, directory=DIR, num_events=num_events)
    
    # otherwise just plot the given cut parameter
    else:
        if cut in GlobalCutParameters.keys():
            histname = cut
            cutType, cutMin, cutMax, label = GlobalCutParameters[histname]
            plotCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax, x_label=label, 
                             directory=DIR, num_events=num_events)
        
        elif cut in LayerPairCutParameters.keys():
            histname = cut
            cutType, cutMinArr, cutMaxArr, label = LayerPairCutParameters[histname]
            for i, pair in enumerate(simplePixelLayerPairs):
                cutMin = -np.inf if cutMinArr is None else cutMinArr[i]
                cutMax = cutMaxArr[i]
                plotCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax, 
                                innerLayer=pair[0], outerLayer=pair[1], x_label=label, directory=DIR, num_events=num_events)
        
        elif cut in ConnectionCutParameters.keys():
            histname = cut
            cutType, cutMin, cutMax, label, label_add = ConnectionCutParameters[histname]
            plotConnectionCutParameter(ROOTFile, histname, cutType, cellCutMin=cutMin, cellCutMax=cutMax,
                                       x_label=label, y_label_add=label_add, directory=DIR, num_events=num_events)
        
        else:
            raise ValueError('Invalid parameter `cut`! Specify the cut parameter you want to plot from the list below or `None` to plot all of them.'
                             +'\nList of valid `cut` parameters: ' + str(list(GlobalCutParameters.keys()) + list(LayerPairCutParameters.keys()) + list(ConnectionCutParameters.keys())))



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Produce cut distribution plots for SimDoublets including total and passing doublets + cut value.")
parser.add_argument("DQMfile", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("config", type=str, help="Path to config file for applied cut values. "+
                    "Supports yaml file with all cuts or the cmssw config file that ran the SimDoubletsAnalyzer "+
                    "(please specify the module name of the analyzer under `-a ANALYZERNAME` if it differs from the default `simDoubletsAnalyzerPhase2`)")
parser.add_argument("-d", "--directory", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("-c", "--cut", default=None, help="cut parameter to be plotted (by default all are plotted)")
parser.add_argument("-n", "--nevents", default=-1, type=int,  help="Number of events (used for scaling to numbers per event if given)")
parser.add_argument("-a", "--analyzer", type=str, default="simDoubletsAnalyzerPhase2", help="Name of the analyzer module "+
                    "(needs to be given if the config file is cmssw config, default `simDoubletsAnalyzerPhase2`)")

def main():
    print("="*30)
    print("  Start makeCutPlots()")
    print("="*30)

    setStyle()
    args = parser.parse_args()

    print("Run the simplotter with the following settings:")
    print(" * DQM file:", args.DQMfile)

    # if the given config is yaml, it should already contain the cut values in the correct format
    if args.config[-4:] == ".yml":
        print(" * provided config file for cuts (yaml):", args.config)
        CUTfile = args.config
        neventsFromConfig = -1

    # elif python format, assume it is a cmssw config file
    elif args.config[-3:] == ".py":
        CUTfile = args.directory + '/cutValues.yml'
        print(" * provided config file for cuts (CMSSW config):", args.config)
        print("   -> read cut parameters from CMSSW config and create yaml config here:")
        print("     ", CUTfile)
        print(" * for that use the cuts set in the analyzer module named:", args.analyzer)

        # in this case write your own yml based on the given config
        import importlib.util
        import sys
        spec = importlib.util.spec_from_file_location("process", args.config)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        # get the analyzer
        simDoubletsAnalyzer = getattr(config_module.process, args.analyzer, None)
        if simDoubletsAnalyzer is None:
            raise ValueError("Invalid parameter `analyzer`! In the given CMSSW config, no module with the name `%s` was found" % args.analyzer)
        CUTdict = {
            cutname: getattr(simDoubletsAnalyzer, cutname).value() for cutname in CUTlist_scalars
        } | {
            cutname: list(getattr(simDoubletsAnalyzer, cutname)) for cutname in CUTlist_vectors
        }

        neventsFromConfig = config_module.process.maxEvents.input.value()

        Path(args.directory).mkdir(parents=True, exist_ok=True)
        with open(CUTfile, 'w') as outfile:
            yaml.dump(CUTdict, outfile, default_flow_style=False)
    
    # else, something's wrong
    else:
        raise ValueError("Invalid parameter `config`! Please give either a yaml file with the cut parameters (.yml) or the cmssw config directly (.py).")

    print(" * output directory:", args.directory)

    # set number of events
    with uproot.open(args.DQMfile) as ROOTfile:
        if "DQMData/Run 1/EventInfo/processedEvents" in ROOTfile:
            hist = ROOTfile["DQMData/Run 1/EventInfo/processedEvents"]
            nevents = hist.values()[0]
        elif neventsFromConfig > 0:
            nevents = neventsFromConfig
        elif args.nevents > 0:
            nevents = args.nevents
        else:
            nevents = None
    
    if nevents is None:
        print(" * do not scale plots to number of events")
    else:
        print(" * determined number of events:", nevents)

    if args.cut is None:
        print(" * plot all distributions of cut parameters")
    else:
        print(" * plot only the distribution for the cut:", args.cut)

    print("\n")        
    # produce the plots
    makeCutPlots(args.DQMfile, CUTfile=CUTfile,
                 DIR=args.directory, cut=args.cut, num_events=nevents)

    print("="*30)
    print("  End makeCutPlots()")
    print("="*30)

if __name__ == "__main__":
    main()