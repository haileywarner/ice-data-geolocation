from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from img_processing import get_img_lon_lat
from scipy import spatial
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import glob
import pandas as pd


def partition_img(txtfile, folder, n, thresh):
    '''
    partition_img: For each image in folder, finds pixel locations of altimetry measurments and extracts an nxn patch around each. Discards boundary image samples which contain >thresh black border pixels.

    :txtfile: path to .txt file.
    :n: side length of partition samples (in pixels)
    :thresh: threshold at which image samples get discarded. If sample contains more than m black pixels, discard it. Otherwise store and return the sample.
    :return: list of (n,n) ndarrays containing image sample pixel intensities.
    '''

    SPATIAL_RES = 0.0002 # 1 pixel = 20 cm^2 
    R = 6371. # Earth radius (km)

    # Make folder to save image patches to.
    if not os.path.exists(folder+'/patches61'):
        os.makedirs(folder+'/patches61')

    # Read altimetry txt file into ndarray (columns = TIME, LON_MAXAMP, LAT_MAXAMP, Z_MAXAMP).
    altimetry_coords = []
    altimetry = np.genfromtxt(txtfile, dtype=float, usecols=(2,6,7,8))
    for row in range(altimetry.shape[0]):
        altimetry_coords.append((altimetry[row][1],altimetry[row][2]))
    
    # Generate list of image center coordinates of all imagery within coincident folder.
    imagery_coords = []
    imagery_names = []
    for imgxmlfile in glob.glob(folder+'\*CAM150MP*.xml'):
        center = get_img_lon_lat(imgxmlfile) # center is a (lon,lat) tuple
        imagery_coords.append(center)
        imagery_names.append(imgxmlfile)

    # Use a k-d tree to locate nearest neighbor image center to each altimetry entry.
    kdtree = spatial.KDTree(altimetry_coords)

    inliers = []
    for image_center in imagery_coords:
        image_name = imagery_names[imagery_coords.index(image_center)]
        d,i = kdtree.query([image_center], k=1) #distance_upper_bound=0.13592104642) # ~1.8km
        print(i)
        inliers.append((image_name, image_center, i[0], altimetry_coords[i[0]]))

    # Subsample image to 61-by-61 pixel square around altimetry center. (This will produce 1:1 correspondence between altimetry measurements and image squares)
    n=0
    sorted_alt_row   = []
    sorted_alt_coord = []
    sorted_img_name  = []
    sorted_img_coord = []
    sorted_img_file  = []
    for inlier in inliers:
        tiffile = inlier[0][:-7]+'tif'
        whole_image = cv2.imread(tiffile, cv2.IMREAD_GRAYSCALE)
        x, y = whole_image.shape

        # WGS84 --> km
        # delta_lon = inlier[3][0] - inlier[1][0]
        # delta_lat = inlier[3][1] - inlier[1][1]
        # mean_lat = (inlier[3][1] + inlier[1][1])/2
        
        # Haversine Formula: https://www.movable-type.co.uk/scripts/latlong.html
        # dx_km = R*np.pi*delta_lat/180.
        # dy_km = (R*np.pi*delta_lon/180.)*np.cos(mean_lat)

        # dx_km = R*np.arccos(delta_lat/R^2)
        # dy_km = R*np.arccos(delta_lon/R^2)

        # km --> pixels
        # dx = dx_km/SPATIAL_RES
        # dy = dy_km/SPATIAL_RES

        # alt_pixel_x = int(x/2 + dx)
        # alt_pixel_y = int(y/2 + dy)

        # if 30<alt_pixel_x and alt_pixel_x<x-31 and 30<alt_pixel_y and alt_pixel_y<y-31:
        #     image_patch = whole_image[alt_pixel_x-30:alt_pixel_x+31, alt_pixel_y-30:alt_pixel_y+31]
        # else:
        #     image_patch = np.zeros((61,61), dtype=int)

        # Extract patch around image center.
        image_patch = whole_image[x//2-30:x//2+31, y//2-30:y//2+31]

        # Eliminate pairs with >thresh black pixels in imagery square (image is out of bounds).
        # if np.count_nonzero(image_patch) < 61**2 - thresh:
        #     continue

        print(n)
        n+=1

        # Save each patch as PNG.
        im = Image.fromarray(image_patch)
        im.save(folder+'/patches61/patch'+str(n-1)+'.png')
        print(folder+'/patches61/patch'+str(n-1)+'.png')
        
        # Save patch metadata to TXT file.
        sorted_alt_row.append(str(inlier[2]))
        sorted_alt_coord.append(str(inlier[3]))
        sorted_img_name.append('patch'+str(n-1)+'.png')
        sorted_img_coord.append(inlier[1])
        sorted_img_file.append(inlier[0])
    meta_dict = {'row_in_altimetry_file':sorted_alt_row, 'altimetry_coordinate':sorted_alt_coord,\
                 'image_coordinate':sorted_img_coord, 'patch_name':sorted_img_name, 'img_file_name':sorted_img_file}
    df = pd.DataFrame(data=meta_dict)
    df.to_csv(folder+'/metadata61.csv')

dir = "E:\spatially_sorted_lvisf2_is2olvis1bcv"
unprocessed_folders = ['57085_to_57180', '58037_to_58132', '59554_to_59653', '59484_to_59617']

# for folder in os.listdir(dir):
for folder in unprocessed_folders:
    folder = os.path.join(dir,folder)
    print(folder)
    for f in glob.glob(folder+'\*.txt'):
        print('next file')
        partition_img(f, folder, 61, 10)