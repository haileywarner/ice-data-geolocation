import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
# https://stats.stackexchange.com/questions/361017/proper-way-of-estimating-the-covariance-error-ellipse-in-2d

def cov_ellipse2(points, cov, nstd):
    """
    Source: https://stackoverflow.com/a/39749274/1391441
    """

    vals, vecs = eigsorted(cov)
    theta = np.degrees(np.arctan2(*vecs[::-1, 0]))

    # Confidence level
    q = 2 * norm.cdf(nstd) - 1
    r2 = chi2.ppf(q, 2)

    width, height = 2 * np.sqrt(vals * r2)

    return width, height, theta


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



glcmfile = r"C:\Users\Haile\OneDrive\Documents\EEE515\56133_to_56249\patches61\glcm_stats.csv"
metafile = r"C:\Users\Haile\OneDrive\Documents\EEE515\56133_to_56249\metadata61.csv"
altfile  = r"C:\Users\Haile\OneDrive\Documents\EEE515\56133_to_56249\LVISF2_IS_GL2022_0712_R2212_056133.txt"

glcm = pd.read_csv(glcmfile, header=0)
meta = pd.read_csv(metafile, header=0)


# xs = [list(glcm.dissimilarity), list(glcm.correlation), list(glcm.homogeneity), list(glcm.contrast), list(glcm.ASM), list(glcm.energy)]
# fig, axs = plt.subplots(6, 1, figsize=(8, 4))
# n=0
# for x in xs:
#     elevations = np.genfromtxt(altfile, dtype=float, usecols=(8)).tolist()
#     indices = list(meta.row_in_altimetry_file)
#     y = [elevations[i] for i in indices]
#     axs[n].scatter(x, y, s=0.5)

#     axs[n].axvline(c='grey', lw=1)
#     axs[n].axhline(c='grey', lw=1)

#     print 

#     confidence_ellipse(np.array(x), np.array(y), axs[n], edgecolor='red')
#     n+=1

# plt.xlim([0, 0.1])
# plt.ylim([20, 100])
# plt.show()

def plot_ellipses():
    xs = [list(glcm.dissimilarity), list(glcm.correlation), list(glcm.homogeneity), list(glcm.contrast), list(glcm.ASM), list(glcm.energy)]
    fig, axs = plt.subplots(1, 1, figsize=(4, 4))
    n=0
    x = list(glcm.energy)
    elevations = np.genfromtxt(altfile, dtype=float, usecols=(8)).tolist()
    indices = list(meta.row_in_altimetry_file)
    y = [elevations[i] for i in indices]
    axs.scatter(x, y, s=0.5)

    axs.axvline(c='grey', lw=1)
    axs.axhline(c='grey', lw=1)

    confidence_ellipse(np.array(x), np.array(y), axs, edgecolor='red')
    plt.xlim([0,0.15])
    plt.ylim([29,31.5])
    plt.show()

def corr_coef():
    corr = []
    xs = [list(glcm.dissimilarity), list(glcm.correlation), list(glcm.homogeneity), list(glcm.contrast), list(glcm.ASM), list(glcm.energy)]
    elevations = np.genfromtxt(altfile, dtype=float, usecols=(8)).tolist()
    indices = list(meta.row_in_altimetry_file)
    y = [elevations[i] for i in indices]

    for x in xs:
        corr.append(np.corrcoef(x,y)[1][0])
    
    print(corr)

corr_coef()