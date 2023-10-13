import glob
import os
import shutil
import xml.etree.ElementTree as et

def get_img_time(xmlfile):

    '''
    get_img_time : Parses military time value from .xml files that accompany IceSat-2 survery campaign
                   imagery, then converts to UTC decimal seconds per day.

                   Coordinate is roughly the geometric center of the image.
                   (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/is2olvis1bcv/versions/1))

    :xml_file: path to .xml file.
    :return: time (hhmmss).
    '''

    tree = et.parse(xmlfile)
    root = tree.getroot()
    military = str(root[2][7][0].text).replace(':','')
    #print(military)
    utc = float(military[0:2])*3600 + float(military[2:4])*60 + float(military[4:6])

    return utc

def get_txtxml_time(xmlfile):

    '''
    get_xml_time : Parses military time value from .xml files that accompany IceSat-2 survery campaign
                   imagery, then converts to UTC decimal seconds per day.

                   Coordinate is roughly the geometric center of the image.
                   (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/is2olvis1bcv/versions/1))

    :xml_file: path to .xml file.
    :return: time (hhmmss).
    '''

    tree = et.parse(xmlfile)
    root = tree.getroot()
    start_military = str(root[2][7][2].text).replace(':','')
    end_military   = str(root[2][7][0].text).replace(':','')
    #print(start_military)
    #print(end_military)
    t0 = float(start_military[0:2])*3600 + float(start_military[2:4])*60 + float(start_military[4:6])
    tn = float(end_military[0:2])*3600 + float(end_military[2:4])*60 + float(end_military[4:6])

    return t0, tn



def get_txt_time(txtfile):

    '''
    get_txt_time : Parses LVISF2 TXT files for start and end time of segment in UTC decimal seconds per day.

                   (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/lvisf2/versions/1))

    :xml_file: path to .TXT file.
    :return:   (t0, tn)
    '''

    with open(txtfile, 'rb') as f:
        for i, line in enumerate(f):
            if i == 14:
                t0 = float(line[22:33])
        try:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        tn = float(f.readline().decode()[22:33])

    return t0, tn

def get_txtxml_lon_lat(xmlfile):
    '''
    get_xml_time : Parses military time value from .xml files that accompany IceSat-2 survery campaign
                   imagery, then converts to UTC decimal seconds per day.

                   Coordinate is roughly the geometric center of the image.
                   (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/is2olvis1bcv/versions/1))

    :xml_file: path to .xml file.
    :return: time (hhmmss).
    '''

    tree = et.parse(xmlfile)
    root = tree.getroot()
    lat = float(root[2][8][0][0][0][0][1].text)
    lon = float(root[2][8][0][0][0][0][0].text)
    return lat, lon

#################################################################################################################################

HOME_DIR = r'D:\lvis images + altimetry\eo imagery\2022.07.11-2022.07.26'

for txtxml_file in glob.glob(r'D:\lvis images + altimetry\altimetry\*.TXT.xml'):
    txt_file = txtxml_file[:-7]+'txt'

    index = txtxml_file[-14:-8]
    day   = txtxml_file[-23:-21]
    h5file = '*.'+index+'.h5'
    folder = ''

    lat, lon = get_txtxml_lon_lat(txtxml_file)
    new_folder = ('E:\paired_altimetry_and_images\lat'+str(lat)+'_lon'+str(lon)+'\\')
    if os.path.exists(new_folder) == False:
        os.mkdir(new_folder)
    else: continue

    print(txtxml_file)
    if os.path.exists(new_folder+os.path.basename(txtxml_file)) == False:
        shutil.copy(txtxml_file, new_folder+os.path.basename(txtxml_file))
        print(new_folder+os.path.basename(txtxml_file))
    if os.path.exists(new_folder+os.path.basename(txt_file)) == False:
        shutil.copy(txt_file, new_folder+os.path.basename(txt_file))
        print(new_folder+os.path.basename(txt_file))

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

    t0, tn = get_txtxml_time(txtxml_file)
    #print('Range: '+str(t0)+', '+str(tn))

    num_matches = 0
    for imgxml_file in glob.glob(folder+'\*CAM150MP*.xml'):
        #print(imgxml_file)
        img_file = imgxml_file[:-4]
        utc = get_img_time(imgxml_file)
        #print('UTC: '+str(utc))

        if (t0-60 <= utc <= tn+60):
            num_matches += 1
            
            if os.path.isfile(new_folder+os.path.basename(imgxml_file)) == False:
                shutil.copy(imgxml_file, new_folder+os.path.basename(imgxml_file))
                print(new_folder+os.path.basename(imgxml_file))
            if os.path.isfile(new_folder+os.path.basename(img_file)) == False:
                shutil.copy(img_file, new_folder+os.path.basename(img_file))
                print(new_folder+os.path.basename(img_file))
    
    print(num_matches)







