import matplotlib as mpl
from matplotlib.colors import Normalize, LogNorm
import numpy as np

def plot2D_(theHist, fig, ax, zLabel="", logZ=False, nEvents=None, cmap="plasma", vmax=None):
    # get histogram data
    w, x, y = theHist.to_numpy()
    if nEvents is not None:
        w /= nEvents

    # set limits
    vmin = np.nanmin(np.ma.masked_equal(w, 0.0, copy=False)) * 0.999
    vmax = np.nanmax(w) if vmax is None else vmax
    if logZ:
        ax.pcolormesh(x, y, w.T, norm=LogNorm(vmin=vmin, vmax=vmax), cmap=cmap)
        fig.colorbar(mpl.cm.ScalarMappable(norm=LogNorm(vmin=vmin, vmax=vmax), cmap=cmap), 
                    ax=ax, extend='min', label=zLabel + ("" if nEvents is None else " / event"))

    else:
        ax.pcolormesh(x, y, w.T, norm=Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
        fig.colorbar(mpl.cm.ScalarMappable(norm=Normalize(vmin=vmin, vmax=vmax),cmap=cmap), 
                    ax=ax, extend='min', label=zLabel)