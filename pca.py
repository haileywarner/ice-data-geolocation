import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

glcm_stats_df = pd.read_csv(r'E:\spatially_sorted_lvisf2_is2olvis1bcv\all_patches\glcm_statistics.csv')
glcm_stats_df.drop(glcm_stats_df.tail(1).index,inplace=True)
glcm_stats_df.drop('z_maxamp',axis=1,inplace=True)
features = glcm_stats_df.columns
print(glcm_stats_df)

pca = PCA(n_components=6)
X = pca.fit(glcm_stats_df)
print(X.explained_variance_ratio_)