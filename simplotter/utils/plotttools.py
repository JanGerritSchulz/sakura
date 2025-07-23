# packages that are needed
import mplhep as hep
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# colors used for plots
class Colors:
    true = "#1ca01c"
    fake = "#FF0000"
    passed = '#51BBFE'
    total = "#00008B"

class ColorMaps:
    true = mpl.pyplot.get_cmap("Greens")
    fake = mpl.pyplot.get_cmap("Reds")
    passed = mpl.pyplot.get_cmap("Blues")
    total = mpl.pyplot.get_cmap("plasma")

    true.set_under('w')
    fake.set_under('w')
    passed.set_under('w')
    total.set_under('w')
    
    def get(self, which="Sim"):
        if which == "Sim":
            return self.passed
        elif which == "Fake":
            return self.fake
        elif which == "True":
            return self.true
        elif which == "pass":
            return self.passed
        elif which == "total":
            return self.total

ColorMap = ColorMaps()

# setting the default plotting style based on mplhep
def setStyle(customized=True):
    """This function sets the default style for plotting with matplotlib. The style is in line with the CMS style of the mplhep package. It also includes a customized version with my personal style preferences.

    Args:
        customized (bool, optional): If False, the style follows exactly the mplhep.cms style. If True, some personal customizations are applied. Defaults to True.
    """    
    plt.style.use(hep.style.CMS)
    if customized:
        plt.rcParams['legend.fancybox'] = True
        plt.rcParams['legend.frameon'] = True
        plt.rcParams['xaxis.labellocation'] = "right"
        plt.rcParams['yaxis.labellocation'] = "top"
        plt.rcParams['mathtext.default'] = "it"
        plt.rcParams['mathtext.fontset'] = 'cm'
        plt.rcParams['figure.figsize'] = (12, 9)


def cmslabel(**kwargs):
    """Wrapper for the CMS label in plots. Reason for this is to avoid having to import hep each and every time.
    """    
    hep.cms.label(**kwargs)


def lumilabel(**kwargs):
    """Wrapper for the lumi label in upper right in plots. Reason for this is to avoid having to import hep each and every time.
    """    
    hep.cms.lumitext(**kwargs)


def savefig(filename, dpi=165, bbox_inches="tight", **kwargs):
    """Wrapper for the savefig function of matplotlib with better default settings for dpi and bbox_inches. It also produces eventually not existing sub-directies of rthe plot.

    Args:
        filename (string): Name of the file to save the plot.
        dpi (float, optional): The resolution in dots per inch. If 'figure', use the figure's dpi value.. Defaults to 300.
        bbox_inches (str, optional): Bounding box in inches: only the given portion of the figure is saved. If 'tight', try to figure out the tight bbox of the figure. Defaults to "tight".
    """    
    # if the filename contains a path, check if the directory exists and if not create it
    if "/" in filename:
        directory = "/".join(filename.split("/")[:-1])
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # save the plot
    plt.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, **kwargs)


def combineSubplotHandlesLabels(axs):
    """Combines the handles and labels from multiple matplotlib axes provided as a list.
    
    Args:
        axs (list(plt.axes)): list of matplotlib axes from which to combine the handles and labels for the legend.
    """
    # get all handles and labels from given list of axs
    handlesLabels = [ax.get_legend_handles_labels() for ax in axs]
    handles, labels = [sum(lol, []) for lol in zip(*handlesLabels)]
    # find the unique labels
    uniqueLabels = np.unique(labels)
    labels = np.array(labels)
    # get all handles for the unique labels
    uniqueHandles = [tuple([handles[i] for i in np.where(label==labels)[0]]) for label in uniqueLabels]

    # return the list of combined handles and labels
    return uniqueHandles, uniqueLabels

def legend(ax, axs=None, **kwargs):
    """Plot a global legend for all axs of the list axs in the given subplot ax.

    Args:
        ax (plt.axes): the axes where the legend is plotted.
        axs (list(plt.axes)): list of matplotlib axes from which to combine the handles and labels for the plotted legend.
    """
    # if no list is provided plot the labels for ax only
    if axs is None:
        axs = [ax]
    # get handles, labels and plot the legend
    handles, labels = combineSubplotHandlesLabels(axs)
    ax.legend(handles, labels, **kwargs)