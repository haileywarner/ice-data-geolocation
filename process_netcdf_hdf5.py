import h5py
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset

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


#hdf5_icesat_lon_lat(r'D:\7-9_7-24\ATL07_4bb5055b-4237-11ee-9200-a966ea06ad80\ATL07-01_20220711003556_02921601_005_01.h5')
#netcdf_cryosat_lon_lat(r'D:\7-9_7-24\SIR_SAR_L2_E_4b094afc-4237-11ee-8f72-a966ea06ad80\CS_OFFL_SIR_SAR_2__20220711T010718_20220711T011508_E001.nc')
