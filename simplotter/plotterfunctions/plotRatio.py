from hist.intervals import ratio_uncertainty
import matplotlib.pyplot as plt

def plotRatio(num, denom, cellCut=None, ax=None, uncertainty_type="poisson", fmt=".", **kwargs):
    if ax is None:
        ax = plt.gca()
        
    ratio = num / denom
    ratioErr = ratio_uncertainty(
        num=num.values(),
        denom=denom.values(),
        uncertainty_type=uncertainty_type,
    )
    # if cellCut is given set the errors outside the cut limits to zero
    if cellCut is not None:
        outside = (ratio.axes.edges[0][1:] <= cellCut.min) | (ratio.axes.edges[0][:-1] >= cellCut.max) 
        zeros = ratio.values() == 0
        ratioErr[0][outside & zeros] = 0
        ratioErr[1][outside & zeros] = 0
    
    # plot the ratio
    ax.errorbar(ratio.axes.centers[0], ratio.values(), yerr=ratioErr, xerr=ratio.axes.widths[0]/2, fmt=fmt, **kwargs)

def plotRatioEfficiency(num, denom, cellCut=None, ax=None, fmt=".", **kwargs):
    plotRatio(num, denom, cellCut=cellCut, ax=ax, uncertainty_type="efficiency", fmt=fmt, **kwargs)