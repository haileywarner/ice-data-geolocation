from skimage.feature import graycomatrix, graycoprops
import pandas as pd 
import numpy as np 
import cv2 
import os
import re
import glob

# -------------------- load dataset ------------------------
 
# dir = "E:\spatially_sorted_lvisf2_is2olvis1bcv"
# imgs = [] #list image matrix 
# labels = []
# descs = []
# for folder in os.listdir(dir):
#     for imgfile in glob.glob(os.path.join(dir, folder)+'\*CAM150MP*.tif'):
#             img = cv2.imread(os.path.join(dir, folder, imgfile))
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             h, w = gray.shape
#             ymin, ymax, xmin, xmax = h//3, h*2//3, w//3, w*2//3
#             crop = gray[ymin:ymax, xmin:xmax]
#             resize = cv2.resize(crop, (0,0), fx=0.5, fy=0.5)

# ---------- calculate graycomatrix() & graycoprops() for angle 0, 45, 90, 135 (rotational invariance) -------------------
def calc_glcm_all_agls(img, label, props, dists=[5], agls=[0, np.pi/4, np.pi/2, 3*np.pi/4], lvl=256, sym=True, norm=True):
    
    print(img.shape)

    glcm = graycomatrix(img, 
                        distances=dists, 
                        angles=agls, 
                        levels=lvl,
                        symmetric=sym, 
                        normed=norm)
    feature = []
    glcm_props = [propery for name in props for propery in graycoprops(glcm, name)[0]]
    for item in glcm_props:
            feature.append(item)
    feature.append(label) 
    
    return feature


# ----------------- call calc_glcm_all_agls() for all properties ------------------------
properties = ['dissimilarity', 'correlation', 'homogeneity', 'contrast', 'ASM', 'energy']

imgs = cv2.imread('aerial.png', cv2.IMREAD_GRAYSCALE)
labels = ['test']*512
print(imgs)

glcm_all_agls = []
for img, label in zip(imgs, labels): 
    glcm_all_agls.append(
            calc_glcm_all_agls(img, 
                                label, 
                                props=properties)
                            )
 
columns = []
angles = ['0', '45', '90','135']
for name in properties :
    for ang in angles:
        columns.append(name + "_" + ang)


# Create the pandas DataFrame for GLCM features data
glcm_df = pd.DataFrame(glcm_all_agls, 
                      columns = columns)

glcm_df.head(15)