import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sakura.tools.plotting_helpers import ylabel, cmslabel, savefig
from sakura.histograms.Hist2D import Hist2D
from pathlib import Path
from simplotter.utils.markLayers import markLayersXY
from simplotter.utils.markLayers import markLayersY

def plotEfficiency2D(ROOTfile, histname, directory="plots", x_label="", y_label="", z_label="Efficiency", x_layer=False, y_layer=False, cmsconfig=None):
    
    # load histograms
    h = Hist2D(ROOTfile, histname, y_label, x_label)
    
    # create new figure
    fig, ax = plt.subplots()
    
    cmap = mpl.pyplot.get_cmap("plasma")
    cmap.set_under('w')
    cax = h.plot(ax, True, log=True, cmap=cmap)
    fig.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.LogNorm(vmin=np.ma.masked_equal(h.values, 0.0, copy=False).min(), 
                                                                vmax=np.max(h.values)), 
                                    cmap=cmap), ax=ax, extend='min', label=z_label)
    ylabel(y_label)

    # mark boxes of layers from barrel/endcap
    if x_layer & y_layer:
        markLayersXY(ax)
    elif y_layer:
        markLayersY(ax)
    
    if "GeV" in x_label:
        ax.set_xscale("log")
    if "GeV" in y_label:
        ax.set_yscale("log")

    # add the CMS label
    if cmsconfig is not None:
        cmslabel(llabel=cmsconfig["llabel"], rlabel=cmsconfig["rlabel"], com=cmsconfig["com"])

    # save and show the figure
    Path(directory).mkdir(parents=True, exist_ok=True)
    savefig("%s/%s.png" % (directory, histname))
    plt.close()