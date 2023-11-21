import glob
import os
import shutil
import xml.etree.ElementTree as et
import numpy as np

from lvisf2_processing import check_altimetry_track
from lvisf2_processing import get_txtxml_time

#################################################################################################################################

# Imagery directory in original drive.
HOME_DIR = r'D:\lvis images + altimetry\eo imagery\2022.07.11-2022.07.26'

for txtxmlfile in glob.glob(r'D:\lvis images + altimetry\altimetry\*.TXT.xml'):

    # Create folder for each altimetry segment.
    t0, tn = get_txtxml_time(txtxmlfile)
    new_folder = 'E:\spatially_sorted_lvisf2_is2olvis1bcv\\'+str(t0)+'_to_'+str(tn)+'\\'
    if os.path.exists(new_folder) == True:
        continue
    else:
        print('new folder made')
        os.mkdir(new_folder)

    # Extract parameters from TXT file names.
    txtfile = txtxmlfile[:-7]+'txt'
    index = txtxmlfile[-14:-8]
    day   = txtxmlfile[-23:-21]

    # Decide whether LVISF1B files exist. If yes, save file names.
    h5file = glob.glob(r'D:\lvis images + altimetry\altimetry\LVISF1B*_'+index+'.h5')
    h5bool = True
    print(h5file)
    if h5file:
        h5file = h5file[0]
        h5xmlfile = h5file+'.xml'
    else: h5bool = False

    # Determine which folder to search for coincident imagery by date.
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
    else:
        print('Error: invalid TXT file name.')
        break

    row = 0
    img_names = []
    imgxml_names = []
    img_points = np.zeros((2006,2), dtype=float)
    for imgxmlfile in glob.glob(folder+'\*CAM150MP*.xml'):
        imgfile = imgxmlfile[:-4]
        img_names.append(imgfile)
        imgxml_names.append(imgxmlfile)

        # Get latitude and longitude of center in each image
        tree = et.parse(imgxmlfile)
        root = tree.getroot()
        lat = float(root[2][8][0][0][1].text)
        lon = float(root[2][8][0][0][0].text)
        img_points[row][0] = lon
        img_points[row][1] = lat
        row += 1

    #Check if all images in original folders are inside altimetry boundaries
    boolarr = check_altimetry_track(txtxmlfile, img_points)
    print('BOOLARR: '+str(boolarr.sum()))

    # Extract IMG file names from inlier array
    indices = boolarr.nonzero()
    print(indices)
    if indices[0].size != 0:
        for i in range(len(indices[0])):
            save = img_names[int(indices[0][i])]
            savexml = save[:-3]+'TIF.xml'

            # Save IMG XML file to new drive
            if os.path.isfile(new_folder+os.path.basename(savexml)) == False:
                shutil.copy(savexml, new_folder+os.path.basename(savexml))
                # print(new_folder+os.path.basename(savexml))
            # Save IMG TIF file to new drive
            if os.path.isfile(new_folder+os.path.basename(save)) == False:
                shutil.copy(save, new_folder+os.path.basename(save))
                # print(new_folder+os.path.basename(save))
    
    # Save LVISF2 TXT XML file to new drive
    if os.path.isfile(new_folder+os.path.basename(txtxmlfile)) == False:
        shutil.copy(txtxmlfile, new_folder+os.path.basename(txtxmlfile))
        # print(new_folder+os.path.basename(txtxmlfile))

    # Save LVISF2 TXT file to new drive
    if os.path.isfile(new_folder+os.path.basename(txtfile)) == False:
        shutil.copy(txtfile, new_folder+os.path.basename(txtfile))
        # print(new_folder+os.path.basename(txtfile))

    # Save LVISL1B h5 XML file to new drive
    if h5bool == True:
        if os.path.isfile(new_folder+os.path.basename(h5xmlfile)) == False:
            shutil.copy(h5xmlfile, new_folder+os.path.basename(h5xmlfile))
            # print(new_folder+os.path.basename(h5xmlfile))

    # Save LVISL1B h5 file to new drive
    if h5bool == True:
        if os.path.isfile(new_folder+os.path.basename(h5file)) == False:
            shutil.copy(h5file, new_folder+os.path.basename(h5file))
            # print(new_folder+os.path.basename(h5file))

print('Completed.')