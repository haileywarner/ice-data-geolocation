from PIL import Image
from img_processing import get_img_lon_lat
from scipy import spatial
import numpy as np
import glob

def partition_img(txtfile, folder, n, thresh):
    '''
    partition_img: Partitions each aerial image into an n-by-n grid. Discards boundary image samples which contain >thresh black border pixels.

    :tiffile: path to .tif file.
    :n: side length of partition samples (in pixels)
    :thresh: threshold at which image samples get discarded. If sample contains more than m black pixels, discard it. Otherwise store and return the sample.
    :return: list of (n,n) ndarrays containing image sample pixel intensities.
    '''
    # Read altimetry txt file into ndarray (columns = TIME, LON_MAXAMP, LAT_MAXAMP, Z_MAXAMP).
    altimetry = np.genfromtxt(txtfile, dtype=float, usecols=(2,6,7,8))
    print(altimetry.shape[0])

    # Generate list of image center coordinates of all imagery within coincident folder.
    imagery_coords = []
    imagery_names = []
    for imgxmlfile in glob.glob(folder+'\*CAM150MP*.xml'):
        center = get_img_lon_lat(imgxmlfile) # center is a (lon,lat) tuple
        imagery_coords.append(center)
        imagery_names.append(imgxmlfile)
    print(imagery_coords)

    # Use a k-d tree to locate nearest neighbor image center to each altimetry entry.
    pairs = []
    sum_d = 0.0
    for row in range(altimetry.shape[0]):
        alt_center = (altimetry[row][1],altimetry[row][2])
        kdtree = spatial.KDTree(imagery_coords)
        d,i = kdtree.query([alt_center], k=1)
        # k-th nearest neighbors to return.
        # distance_upper_bound returns only neighbors within this lon,lat distance.
        # d = nearest neighbor distance ndarray.
        # i = nearest neighbor index ndarray.
        pairs.append((d[0],i[0]))
        sum_d += d
    print(sum_d / float(len(pairs)))
    #print(pairs)

    # Subsample image to 61-by-61 pixel square around altimetry center.
    # for pair in pairs:
    #     tiffile = imagery_names[pair[1]][:-7]+'tif'
    #     whole_image = np.asarray(Image.open(tiffile))u4
    #     image_patch = 
        # (This will produce 1:1 correspondence between altimetry measurements and image squares)

    
    # Eliminate pairs with >thresh black pixels in imagery square (image is out of bounds).
        

f = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\56133_to_56249\LVISF2_IS_GL2022_0712_R2212_056133.txt"
folder = r"E:\spatially_sorted_lvisf2_is2olvis1bcv\56133_to_56249"
partition_img(f, folder, 61, 10)
    
