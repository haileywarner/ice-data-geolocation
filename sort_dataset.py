import glob
import os
import shutil
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import numpy as np

from lvisf2_processing import check_altimetry_track
from img_processing import get_img_lon_lat

#################################################################################################################################

HOME_DIR = r'D:\lvis images + altimetry\eo imagery\2022.07.11-2022.07.26'

for txtxmlfile in glob.glob(r'D:\lvis images + altimetry\altimetry\*.TXT.xml'):
    txtfile = txtxmlfile[:-7]+'txt'
    print(txtxmlfile)
    index = txtxmlfile[-14:-8]
    day   = txtxmlfile[-23:-21]
    h5file = '*.'+index+'.h5'
    folder = ''
    if   day == '11':
        folder = HOME_DIR+r'\2022.07.11'
    elif day == '12':
        folder = HOME_DIR+r'\2022.07.12'
    elif day == '19':
        folder = HOME_DIR+r'\2022.07.19'
    elif day == '21':
        folder = HOME_DIR+r'\2022.07.21'
    elif day == '23':
        folder = HOME_DIR+r'\2022.07.23'
    elif day == '26':
        folder = HOME_DIR+r'\2022.07.26'
    else: print('Error: invalid TXT file name.')

    row = 0
    img_names = []
    img_points = np.zeros((2006,2), dtype=float)
    for imgxmlfile in glob.glob(folder+'\*CAM150MP*.xml'):
        imgfile = imgxmlfile[:-4]
        img_names.append(imgfile)
        tree = et.parse(imgxmlfile)
        root = tree.getroot()
        lat = float(root[2][8][0][0][1].text)
        lon = float(root[2][8][0][0][0].text)
        img_points[row][0] = lon
        img_points[row][1] = lat
        #print(lon, lat)
        row += 1
    boolarr = check_altimetry_track(txtxmlfile, img_points)
    print(boolarr.sum())
    #img_index = np.where(boolarr)[0].astype(int)
    # for i in range(len(img_index)):
    #     print(img_names[img_index[i]])
    #print(i for i in boolarr.sum())
    


    # lat, lon = get_txtxml_lon_lat(txtxmlfile)
    # new_folder = ('E:\paired_altimetry_and_images\lat'+str(lat)+'_lon'+str(lon)+'\\')
    # if os.path.exists(new_folder) == True:
    #     continue
    # else:
    #     os.mkdir(new_folder)

    #     print(txtxmlfile)
    #     if os.path.exists(new_folder+os.path.basename(txtxmlfile)) == False:
    #         shutil.copy(txtxmlfile, new_folder+os.path.basename(txtxmlfile))
    #         print(new_folder+os.path.basename(txtxmlfile))
    #     if os.path.exists(new_folder+os.path.basename(txtfile)) == False:
    #         shutil.copy(txtfile, new_folder+os.path.basename(txtfile))
    #         print(new_folder+os.path.basename(txtfile))

    #     if   day == '11':
    #         folder = HOME_DIR+r'\2022.07.11'
    #     elif day == '12':
    #         folder = HOME_DIR+r'\2022.07.12'
    #     elif day == '19':
    #         folder = HOME_DIR+r'\2022.07.19'
    #     elif day == '21':
    #         folder = HOME_DIR+r'\2022.07.21'
    #     elif day == '23':
    #         folder = HOME_DIR+r'\2022.07.23'
    #     elif day == '26':
    #         folder = HOME_DIR+r'\2022.07.26'
    #     else: print('Error: invalid TXT file name.')

    #     t0, tn = get_txtxml_time(txtxmlfile)
    #     #print('Range: '+str(t0)+', '+str(tn))

    #     num_matches = 0
    #     for imgxmlfile in glob.glob(folder+'\*CAM150MP*.xml'):
    #         #print(imgxmlfile)
    #         imgfile = imgxmlfile[:-4]
    #         utc = get_img_time(imgxmlfile)
    #         #print('UTC: '+str(utc))

    #         if (t0-60 <= utc <= tn+60):
    #             num_matches += 1
                
    #             if os.path.isfile(new_folder+os.path.basename(imgxmlfile)) == False:
    #                 shutil.copy(imgxmlfile, new_folder+os.path.basename(imgxmlfile))
    #                 print(new_folder+os.path.basename(imgxmlfile))
    #             if os.path.isfile(new_folder+os.path.basename(imgfile)) == False:
    #                 shutil.copy(imgfile, new_folder+os.path.basename(imgfile))
    #                 print(new_folder+os.path.basename(imgfile))
        
    #     print(num_matches)
    # print('Finished.')






