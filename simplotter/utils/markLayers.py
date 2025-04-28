import matplotlib.pyplot as plt
import numpy as np

def markLayersXY(ax, boxes=True, layerPairs=None):
    if layerPairs is not None:
        innerLayer, outerLayer = layerPairs[0]
        ax.plot(np.array([-0.5, -0.5, 0.5, 0.5, -0.5]) * 0. + innerLayer, 
                np.array([-0.5, 0.5, 0.5, -0.5, -0.5]) * 0. + outerLayer, ".r", linewidth=1, label="layer pairs in reconstruction")
        for pair in layerPairs[1:]:
            innerLayer, outerLayer = pair
            ax.plot(np.array([-0.5, -0.5, 0.5, 0.5, -0.5]) * 0. + innerLayer, 
                    np.array([-0.5, 0.5, 0.5, -0.5, -0.5]) * 0. + outerLayer, ".r", linewidth=1)
    
    if boxes:
        ax.plot([-0.5, -0.5, 3.5, 3.5, -0.5], 
                [-0.5, 3.5, 3.5, -0.5, -0.5], "-k")
        ax.plot([3.5, 3.5, 15.5, 15.5, 3.5], 
                [3.5, 15.5, 15.5, 3.5, 3.5], "-k")
        ax.plot([27.5, 27.5, 15.5, 15.5, 27.5], 
                [27.5, 15.5, 15.5, 27.5, 27.5], "-k")
        ax.plot([-0.5, -0.5, 3.5, 3.5, -0.5], 
                [-0.5, 3.5, 3.5, -0.5, -0.5], "w", linestyle=(0,(3,3)))
        ax.plot([3.5, 3.5, 15.5, 15.5, 3.5], 
                [3.5, 15.5, 15.5, 3.5, 3.5], "w", linestyle=(0,(3,3)))
        ax.plot([27.5, 27.5, 15.5, 15.5, 27.5], 
                [27.5, 15.5, 15.5, 27.5, 27.5], "w", linestyle=(0,(3,3)))
        
def markLayersY(ax):
    ax.axhline(3.5, linestyle="-", color="k")
    ax.axhline(15.5, linestyle="-", color="k")
    ax.axhline(3.5,  color="w", linestyle=(0,(3,3)))
    ax.axhline(15.5, color="w", linestyle=(0,(3,3)))