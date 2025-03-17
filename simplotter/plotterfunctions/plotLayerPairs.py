import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sakura.tools.plotting_helpers import ylabel, cmslabel, savefig
from sakura.histograms.Hist2D import Hist2D
from pathlib import Path
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs, NonSkippingLayerPairs

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