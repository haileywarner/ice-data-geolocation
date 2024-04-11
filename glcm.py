from skimage.feature import graycomatrix, graycoprops
import pandas as pd 
import numpy as np 
import cv2 
import os
import glob
from pathlib import Path


angles = ['0', '45', '90','135']
properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']
df_rows = []

dir = "E:\spatially_sorted_lvisf2_is2olvis1bcv"
unprocessed_folders = ['58784_to_58879','58879_to_58974','59752_to_59849','59056_to_59230','58974_to_59069','58418_to_58784','63493_to_64496','57085_to_57180','59230_to_59484','69051_to_69408',\
                       '58072_to_58328','59849_to_59985','59617_to_59713','59653_to_59752','57435_to_57540','69591_to_69925','64693_to_64794','61470_to_61717','65957_to_68185','60705_to_61356',\
                        '60059_to_60548','59881_to_60059','69408_to_69591','58227_to_58322',\
                        '65858_to_65957','58382_to_62839','64496_to_64592','65762_to_65858','64592_to_64693','60548_to_60705','68185_to_68413','61356_to_61470','59713_to_59881','58037_to_58132',\
                        '57540_to_57899','57180_to_57407','59069_to_59165','59554_to_59653','59456_to_59554','57899_to_58072','59262_to_59360','58954_to_59056','59360_to_59456','59165_to_59262',\
                        '59985_to_60212','58328_to_58954','59484_to_59617']

def calculate_glcm(dir):

    columns = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']

    # for folder in unprocessed_folders:
    #     print(folder)
    # for imgfile in glob.glob(dir+r'\all_patches\patch*.png'):

    for x in range(1641):
            imgfile = dir+r'\all_patches\patch'+str(x)+'.png'
            img = cv2.imread(imgfile, cv2.IMREAD_GRAYSCALE)

            glcm = graycomatrix(img, 
                                distances=[1, 2, 3, 4, 5], 
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

    glcm_df = pd.DataFrame(df_rows, columns=columns)
    metadata_df =  pd.read_csv(Path(dir+r'\all_patches\metadata.csv'))
    glcm_df['z_maxamp'] = metadata_df['z_maxamp']
    glcm_df.to_csv(dir+r'\all_patches\glcm_statistics.csv')