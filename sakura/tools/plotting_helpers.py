# packages that are needed
import mplhep as hep
import matplotlib.pyplot as plt
from sakura.dictionaries.label_dictionary import LABEL_DICT


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


def xlabel(label, ax=None, **kwargs):
    """Wrapper for setting the xlabel of a plot.

    Args:
        label (string): Label or label key.
    """    
    if ax is None:
        ax = plt.gca()
    # if the label is a key to another label, use that one
    # e.g. eff -> Efficiency
    if label in LABEL_DICT.keys():
        ax.set_xlabel(LABEL_DICT[label], **kwargs)
    else:
        ax.set_xlabel(label, **kwargs)


def ylabel(label, ax=None, **kwargs):
    """Wrapper for setting the ylabel of a plot.

    Args:
        label (string): Label or label key.
    """    
    if ax is None:
        ax = plt.gca()
    # if the label is a key to another label, use that one
    # e.g. eff -> Efficiency
    if label in LABEL_DICT.keys():
        ax.set_ylabel(LABEL_DICT[label], **kwargs)
    else:
        ax.set_ylabel(label, **kwargs)


def cmslabel(**kwargs):
    """Wrapper for the CMS label in plots. Reason for this is to avoid having to import hep each and every time.
    """    
    hep.cms.label(**kwargs)


def savefig(filename, dpi=165, bbox_inches="tight", **kwargs):
    """Wrapper for the savefig function of matplotlib with better default settings for dpi and bbox_inches.

    Args:
        filename (string): Name of the file to save the plot.
        dpi (float, optional): The resolution in dots per inch. If 'figure', use the figure's dpi value.. Defaults to 300.
        bbox_inches (str, optional): Bounding box in inches: only the given portion of the figure is saved. If 'tight', try to figure out the tight bbox of the figure. Defaults to "tight".
    """    
    plt.savefig(filename, dpi=dpi, bbox_inches=bbox_inches, **kwargs)