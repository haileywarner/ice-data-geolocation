import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\glcm_statistics.csv')
data_array = df.to_numpy(dtype=float,copy=True)
corr_matrix = df.corr().to_numpy(dtype=float,copy=True)

vars = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy', 'ice freeboard']

def corr_heatmap():
    # CORRELATION MATRIX HEATMAP
    fig, ax = plt.subplots()
    im = ax.imshow(corr_matrix)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(vars)), labels=vars)
    ax.set_yticks(np.arange(len(vars)), labels=vars)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(vars)):
        for j in range(len(vars)):
            text = ax.text(j, i, round(corr_matrix[i, j], 2),
                        ha="center", va="center", color="w")

    #ax.set_title("Correlation Matrix of GLCM Statistics and Ice Freeboard")
    fig.tight_layout()
    plt.show()

def scatter_plots(data_array):

    fig, axs = plt.subplots(2,3)
    axs[0, 0].scatter(data_array[:,0],data_array[:,6],s=2)
    axs[0, 1].scatter(data_array[:,1],data_array[:,6],s=2)
    axs[0, 2].scatter(data_array[:,2],data_array[:,6],s=2)
    axs[1, 0].scatter(data_array[:,3],data_array[:,6],s=2)
    axs[1, 1].scatter(data_array[:,4],data_array[:,6],s=2)
    axs[1, 2].scatter(data_array[:,5],data_array[:,6],s=2)

    axs[0,0].set_ylim((0,50))
    axs[0,1].set_ylim((0,50))
    axs[0,2].set_ylim((0,50))
    axs[0,2].set_xlim((0,0.4))
    axs[1,0].set_ylim((0,50))
    axs[1,1].set_ylim((0,50))
    axs[1,1].set_xlim((0,0.025))
    axs[1,2].set_ylim((0,50))
    axs[1,2].set_xlim((0,0.15))

    axs[0,0].set_title('(a) dissimilarity')
    axs[0,1].set_title('(b) correlation')
    axs[0,2].set_title('(c) homogeneity')
    axs[1,0].set_title('(d) contrast')
    axs[1,1].set_title('(e) ASM')
    axs[1,2].set_title('(f) energy')

    plt.show()

corr_heatmap()