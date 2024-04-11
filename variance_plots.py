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

    fig, ax = plt.subplots()
    ax.scatter(data_array[:,2],data_array[:,1],s=2)

    ax.set_xlabel('patch variance')
    ax.set_ylabel('ice freeboard')

    plt.show()

varfile = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\variance_statistics.csv"
var = pd.read_csv(varfile)
data_array = var.to_numpy(dtype=float,copy=True)
scatter_plots(data_array)
    
varfile = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\variance_statistics.csv"
df = pd.read_csv(varfile)
data_array = df.to_numpy(dtype=float,copy=True)
corr_matrix = df.corr().to_numpy(dtype=float,copy=True)