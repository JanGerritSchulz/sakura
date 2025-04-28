import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sakura.tools.plotting_helpers import ylabel, cmslabel, savefig
from sakura.histograms.Hist2D import Hist2D
from pathlib import Path
from simplotter.dataconfig.layerPairs import simplePixelLayerPairs, NonSkippingLayerPairs
from simplotter.utils.markLayers import markLayersXY

def plotLayerPairs(ROOTfile, directory="plots", num_events=None, cmsconfig=None, layerPairs=simplePixelLayerPairs):
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
    cax = h.plot(ax, True, log=True, cmap=cmap)
    fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.LogNorm(vmin=np.ma.masked_equal(h.values, 0.0, copy=False).min(), 
                                                                vmax=np.max(h.values)), 
                                    cmap=cmap), ax=ax, extend='min',
                label="Number of SimDoublets" + ylabel_suff)
    ylabel("Outer layer ID")

    # draw the boxes to mark barrel and endcaps plus the dots for used layerPairs
    markLayersXY(ax, layerPairs=layerPairs)

    Ntot = np.sum(h.values)
    Nrec = 0
    NrecNoSkip = 0
    for pair in layerPairs:
        innerLayer, outerLayer = pair
        Nrec += h.values[innerLayer, outerLayer]
    for pair in NonSkippingLayerPairs:
        innerLayer, outerLayer = pair
        NrecNoSkip += h.values[innerLayer, outerLayer]

    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"])

    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/layerPairs.png" % (directory))
    plt.close()

    print("\nStatistics from layerPairs:")
    print("Nrec / Ntot = %f / %f = %f" % (Nrec, Ntot, Nrec/Ntot))
    print("Nrec (no skip) / Ntot = %f / %f = %f" % (NrecNoSkip, Ntot, NrecNoSkip/Ntot))
    print("")