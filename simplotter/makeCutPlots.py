# import packages
import uproot
import matplotlib.pyplot as plt
import numpy as np
from sakura.tools.plotting_helpers import setStyle, xlabel, ylabel, cmslabel, savefig
from sakura.histograms.Hist import Hist
from pathlib import Path
import yaml
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs


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

    return GlobalCutParameters, LayerPairCutParameters


# define function that performs the plotting of all cuts
def makeCutPlots(DQMfile, CUTfile="cutParameters/currentCuts.yml", DIR="plots", cut=None, num_events=None):

    DIR += "/cutParameters"

    # open the DQMfile
    ROOTFile = uproot.open(DQMfile)["DQMData/Run 1/Tracking/Run summary/TrackingMCTruth/SimDoublets"]

    # get cut parameters and values
    GlobalCutParameters, LayerPairCutParameters = getCutParameters(CUTfile)

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
        
        else:
            raise ValueError('Invalid parameter `cut`! Specify the cut parameter you want to plot from the list below or `None` to plot all of them.'
                             +'\nList of valid `cut` parameters: ' + str(list(GlobalCutParameters.keys()) + list(LayerPairCutParameters.keys())))



#########################################################################################
# For usage from command line
#########################################################################################

import argparse
parser = argparse.ArgumentParser(description="Process MC PFNano files to the PAIReD data format for training.")
parser.add_argument("DQMfile", type=str, help="Path to the ROOT DQM input file")
parser.add_argument("-c", "--CUTfile", type=str, default="cutParameters/currentCuts.yml", help="Path to config file for applied cut values")
parser.add_argument("-d", "--DIR", type=str, default="plots", help="directory to save the plots in")
parser.add_argument("--cut", default=None, help="cut parameter to be plotted (by default all are plotted)")
parser.add_argument("-n", "--nevents", default=None,  help="Number of events (used for scaling to numbers per event if given)")

def main():
    setStyle()
    args = parser.parse_args()
    makeCutPlots(args.DQMfile, CUTfile=args.CUTfile,
                 DIR=args.DIR, cut=args.cut, num_events=args.nevents)
    

if __name__ == "__main__":
    main()