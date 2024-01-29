from skimage.feature import graycomatrix, graycoprops
import pandas as pd 
import numpy as np 
import cv2 
import os
import glob


angles = ['0', '45', '90','135']
properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']
df_rows = []

folder = r"C:\Users\Haile\OneDrive\Documents\EEE515\56133_to_56249\patches61"
n=0
for imgfile in glob.glob(folder+'\*.png'):
    img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)
    columns = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']

    glcm = graycomatrix(img, 
                        distances=[5], 
                        angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], 
                        levels=256,
                        symmetric=True, 
                        normed=True)

    dissimilarity = np.max(graycoprops(glcm, prop='dissimilarity'))
    correlation   = np.max(graycoprops(glcm, prop='correlation'))
    homogeneity   = np.max(graycoprops(glcm, prop='homogeneity'))
    contrast      = np.max(graycoprops(glcm, prop='contrast'))
    ASM           = np.max(graycoprops(glcm, prop='ASM'))
    energy        = np.max(graycoprops(glcm, prop='energy'))

    df_row = [dissimilarity, correlation, homogeneity, contrast, ASM, energy]
    df_rows.append(df_row)
    n+=1

glcm_df = pd.DataFrame(df_rows, columns=columns)
glcm_df.to_csv(folder+'\glcm_stats.csv')