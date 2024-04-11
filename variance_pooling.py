import numpy as np
import cv2
import pandas as pd

meta   = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\metadata.csv"
meta_df = pd.read_csv(meta, usecols=(1,6))
variances=[]

for n in range(1640):
    imgfile = r'E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\patch'+str(n)+'.png'
    patch = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
    var = np.mean(np.square(patch), dtype=float) - np.mean(patch, dtype=float)**2
    variances.append(var)

meta_df['patch_variance'] = variances
meta_df.to_csv(r'E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\variance_statistics.csv')