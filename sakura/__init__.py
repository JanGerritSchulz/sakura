# A small Python module:
# - for my personal plotting preferences
# - some helper function and classes
#
# Author: Jan Schulz
# Date: January 8 2025
#

# import dictionaries
from sakura.dictionaries.label_dictionary import LABEL_DICT
from sakura.dictionaries.hist_dictionary import HIST_NAME

# import plotting tools
from sakura.tools.plotting_helpers import setStyle, xlabel, ylabel, cmslabel, savefig

# import Histogram classes
from sakura.histograms.Hist import Hist
from sakura.histograms.Hist2D import Hist2D