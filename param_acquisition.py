import xml.etree.ElementTree as et
import h5py
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import os




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
    print(tree)
    root = tree.getroot()
    print(root.tag)
    
    img_lon = float(root[2][8][0][0][0].text)
    img_lat  = float(root[2][8][0][0][1].text)
    img_date_time = int(str(root[2][7][1].text).replace('-','') + str(root[2][7][0].text).replace(':',''))
    print(img_lon)
    print(img_lat)
    print(img_date_time)

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
    print(cryo_start_time[2])
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

    return cryo_start_time, cryo_end_time, ice_start_time, ice_end_time, img_coords



def hdf5_icesat_lon_lat(h5_file):
    '''
    This function parses the trajectory of the IceSat-2 ground track
    and returns the total range of latitude and longitude covered.


    '''

    h5_file = h5py.File(h5_file, 'r')
    print(list(h5_file.keys()))
    gt2r_lat_max = max(h5_file.get('gt2r/sea_ice_segments/latitude'))
    gt2r_lat_min = min(h5_file.get('gt2r/sea_ice_segments/latitude'))
    gt2r_lon_max = max(h5_file.get('gt2r/sea_ice_segments/longitude'))
    gt2r_lon_min = min(h5_file.get('gt2r/sea_ice_segments/longitude'))
    print(gt2r_lat_max)
    print(gt2r_lat_min)
    print(gt2r_lon_max)
    print(gt2r_lon_min)


    return gt2r_lat_max, gt2r_lat_min, gt2r_lon_max, gt2r_lon_min



def netcdf_cryosat_lon_lat(nc_file):

    '''

    '''

    root_group = Dataset(nc_file, 'r+', format='NETCDF4')
    print(root_group.data_model)
    #print(root_group.variables)
    #print(root_group.dimensions)
    #echo_lat = root_group
    root_group.close()
    
    return 


#xml_lon_lat_date_time(r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.11\IS2OLVIS1BCV_CAM038MP_GL2022_0711_R2212_12-26-15.138.tif.xml')
#netcdf_cryosat_lon_lat(r'D:\7-9_7-24\SIR_SAR_L2_E_4b094afc-4237-11ee-8f72-a966ea06ad80\CS_OFFL_SIR_SAR_2__20220711T010718_20220711T011508_E001.nc')
#csv_overlap(r'D:\7-9_7-24\SIR_SAR_L2_E_ATL07_495fbf58-4237-11ee-81ab-a966ea06ad80.csv')
#hdf5_icesat_lon_lat(r'D:\7-9_7-24\ATL07_4bb5055b-4237-11ee-9200-a966ea06ad80\ATL07-01_20220711003556_02921601_005_01.h5')





IMG_DIRECTORY = r'D:\n5eil01u.ecs.nsidc.org\ICESAT2_PO\IS2OLVIS1BCV.001\2022.07.11/'
CSV_FILE = r'D:\7-9_7-24\SIR_SAR_L2_E_ATL07_495fbf58-4237-11ee-81ab-a966ea06ad80.csv'
pairs = {}


def geolocate_xml_csv(csv_file, IMG_DIRECTORY):

    #chdir()

    cryo_start_time, cryo_end_time, ice_start_time, ice_end_time, img_coords = csv_overlap(csv_file)

    for xml_file in IMG_DIRECTORY:
        #print(xml_file)
        for i in range(0,11999):                # i = csv row index
            if xml_file.endswith('.xml'):
                img_lon, img_lat, img_date_time = xml_lon_lat_date_time(xml_file)

                # to extend range, cant just +/- 12hrs of military time (00:00:01 - 12 hours = ?)
                if img_date_time in range(cryo_start_time[i], cryo_end_time[i]) | img_date_time in range(ice_start_time[i], ice_end_time[i]):
                    #bl_lat,bl_lon, br_lat,br_lon, tl_lat,tl_lon, tr_lat,tr_lon
                    if (img_lat in range(img_coords[0][i] - 0.03, img_coords[2][i] + 0.03) & img_lat in range(img_coords[4][i] - 0.03, img_coords[6][i] + 0.003)\
                     | img_lon in range(img_coords[1][i] - 0.03, img_coords[3][i] + 0.03) & img_lat in range(img_coords[5][i] - 0.03, img_coords[7][i] + 0.003)):
                        
                        pairs[xml_file] = i

    print(pairs)

geolocate_xml_csv(CSV_FILE, IMG_DIRECTORY)

