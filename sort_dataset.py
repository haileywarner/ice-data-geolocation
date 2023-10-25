import glob
import os
import shutil
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt

from lvisf2_processing import plot_altimetry_track


#################################################################################################################################

HOME_DIR = r'D:\lvis images + altimetry\eo imagery\2022.07.11-2022.07.26'

for txtxmlfile in glob.glob(r'D:\lvis images + altimetry\altimetry\*.TXT.xml'):
    txtfile = txtxmlfile[:-7]+'txt'
    index = txtxmlfile[-14:-8]
    day   = txtxmlfile[-23:-21]
    h5file = '*.'+index+'.h5'
    folder = ''

    plot_altimetry_track(txtxmlfile)

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






