import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
# https://stats.stackexchange.com/questions/361017/proper-way-of-estimating-the-covariance-error-ellipse-in-2d

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of `x` and `y`

    Parameters
    ----------
    x, y : array_like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    Returns
    -------
    matplotlib.patches.Ellipse

    Other parameters
    ----------------
    kwargs : `~matplotlib.patches.Patch` properties
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor=facecolor,
        **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

glcmfile = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\glcm_statistics.csv"

glcm = pd.read_csv(glcmfile, header=0)

def plot_ellipses():
    xs = [list(glcm.dissimilarity), list(glcm.correlation), list(glcm.homogeneity), list(glcm.contrast), list(glcm.ASM), list(glcm.energy)]
    fig, axs = plt.subplots(1, 1, figsize=(4, 4))
    n=0
    x = list(glcm.energy)
    y = list(glcm.z_maxamp)
    axs.scatter(x, y, s=0.5)

    axs.axvline(c='grey', lw=1)
    axs.axhline(c='grey', lw=1)

    confidence_ellipse(np.array(x), np.array(y), axs, edgecolor='red')
    # plt.xlim([0.1,0.5])
    # plt.ylim([-250,250])
    plt.show()

plot_ellipses()