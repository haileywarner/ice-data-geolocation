import xml.etree.ElementTree as et
import h5py
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import os
import json





def xml_lon_lat_date_time(xml_file):

    '''
    xml_lon_lat_date_time : Parses longitude and latitude, timestamp and date values
                            from .xml files that accompany IceSat-2 survery campaign
                            imagery.
                            Coordinate is roughly the geometric center of the image.
                            (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/is2olvis1bcv/versions/1))

    :xml_file: path to .xml file.
    :return:   longitude(float), latitude(float), date+time (yyyymmddhhmmss).
    '''

    tree = et.parse(xml_file)
    #print(tree)
    root = tree.getroot()
    #print(root.tag)
    
    img_lon = float(root[2][8][0][0][0].text)
    img_lat  = float(root[2][8][0][0][1].text)
    img_date_time = int(str(root[2][7][1].text).replace('-','') + str(root[2][7][0].text).replace(':',''))
    #print(img_lon)
    #print(img_lat)
    #print(img_date_time)

    return img_lon, img_lat, img_date_time


def csv_overlap(csv_file):

    '''
    csv_overlap : Parses automatically generated CRYO2ICE
                  overlap .csv sheet for start/end time and
                  (lat, lon) coordinates of each corner of
                  coincident IceSat-2/CryoSat-2 measurements.

    *** Currently, this function reads manually delimited csv columns, where special chars have been removed.
        Will add a function to read the auto-generated columns, but np.char.replace() is being fussy.

    :csv_file: path to .csv file.
    :return: cryosat_start_time, cryosat_end_time, icesat_start_time, icesat_end_time,(yyyymmddhhmmss.ssssss)
             img_coords(ndarray)

    '''

    table = pd.read_csv(csv_file)

    # cryosat_start_time = table['SIR_SAR_L2_E start time'].to_numpy()
    # cryosat_end_time   = table['SIR_SAR_L2_E end time'].to_numpy()
    # icesat_start_time  = table['ATL07 start time'].to_numpy()
    # icesat_end_time    = table['ATL07 end time'].to_numpy()
    
    # bl_lat_lon        = table['(bl lat. bl lon)'].to_numpy()
    # br_lat_lon        = table['(tr lat. tr lon)'].to_numpy()
    # tl_lat_lon        = table['(tl lat. tl lon)'].to_numpy()
    # tr_lat_lon        = table['(tr lat. tr lon)'].to_numpy()
    # print(tr_lat_lon)
    # print(type(tr_lat_lon))

    # arr_cryo = np.reshape(cryosat_start_time, (1, 11198))
    # print(arr_cryo)
    # print(arr_cryo.shape)
    # print(arr_cryo)
    # print(arr_cryo[0][2])
    # print(type(arr_cryo))
    # print(type(arr_cryo[0]))
    # print(type(arr_cryo[0][2]))
    # r1 = np.char.replace(arr_cryo, '-', ' ')
    # r2 = np.char.replace(r1, ':', '')
    # r3 = np.char.replace(r2, 'T', '')
    # print(r3)
    # for i in cryosat_start_time:
    

    cryo_start_time = table['cryo_start_time'].to_numpy()
    cryo_end_time   = table['cryo_end_time'].to_numpy()
    ice_start_time  = table['ice_start_time'].to_numpy()
    ice_end_time    = table['ice_end_time'].to_numpy()
    #print(cryo_start_time)
    #print(cryo_start_time.shape)
    #print(cryo_start_time[2])
    #print(cryo_start_time[3])
    #print(cryo_start_time[4])
    #print(len(cryo_start_time))
    bl_lat = table['bl_lat'].to_numpy()
    bl_lon = table['bl_lon'].to_numpy()
    br_lat = table['br_lat'].to_numpy()
    br_lon = table['br_lon'].to_numpy()
    tl_lat = table['tl_lat'].to_numpy()
    tl_lon = table['tl_lon'].to_numpy()
    tr_lat = table['tr_lat'].to_numpy()
    tr_lon = table['tr_lon'].to_numpy()
    #print(tr_lon)
    #print(type(tr_lon[2]))

    img_coords = np.asarray([bl_lat,bl_lon, br_lat,br_lon, tl_lat,tl_lon, tr_lat,tr_lon])
    #print(img_coords)
    #print(img_coords.shape)
    #print(img_coords[0][1])

    return cryo_start_time, cryo_end_time, ice_start_time, ice_end_time, img_coords


#xml_lon_lat_date_time(r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.11\IS2OLVIS1BCV_CAM038MP_GL2022_0711_R2212_12-26-15.138.tif.xml')
#csv_overlap(r"D:\cryo2ice\7-9_7-24\SIR_SAR_L2_E_ATL07_495fbf58-4237-11ee-81ab-a966ea06ad80.csv")


def geolocate_xml_csv(csv_file, img_directories):

    print('Searching...')
    cryo_start_time, cryo_end_time, ice_start_time, ice_end_time, img_coords = csv_overlap(csv_file)
    pairs = {}

    for dir in range(0,len(img_directories)):
        print('Next Directory')
        for xml_file in os.listdir(img_directories[dir]):
            if xml_file.endswith('.xml'):
                img_lon, img_lat, img_date_time = xml_lon_lat_date_time(img_directories[dir]+'/'+xml_file)
                print(xml_file)
            for i in range(0,len(cryo_start_time)): # i = csv row index
                    # to extend range, cant just +/- 12hrs of military time (00:00:01 - 12 hours = ?)
                    if img_date_time in np.arange(cryo_start_time[i]-10**6, cryo_end_time[i]+10**6) or img_date_time in np.arange(ice_start_time[i]-10**6, ice_end_time[i]+10**6):
                        #bl_lat,bl_lon, br_lat,br_lon, tl_lat,tl_lon, tr_lat,tr_lon
                        if      (img_lat in np.arange(img_coords[0][i]-0.03, img_coords[2][i]+0.03)  or img_lat in np.arange(img_coords[4][i]-0.03, img_coords[6][i]+0.03))\
                            and (img_lon in np.arange(img_coords[1][i]-0.003,img_coords[3][i]+0.003) or img_lon in np.arange(img_coords[5][i]-0.003,img_coords[7][i]+0.003)):
                            print('Match Found!')
                            pairs[xml_file] = i

    print(pairs)
    return(pairs)

IMG_DIRECTORIES = [r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.11', r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.12',\
                   r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.19', r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.21',\
                   r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.23', r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.26']
CSV_FILE = r'D:\cryo2ice\7-9_7-24\SIR_SAR_L2_E_ATL07_495fbf58-4237-11ee-81ab-a966ea06ad80.csv'

pairs = geolocate_xml_csv(CSV_FILE, IMG_DIRECTORIES)

with open('data.json', 'w') as fp:
    json.dump(pairs, fp)
