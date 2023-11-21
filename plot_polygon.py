import glob as glob
import matplotlib.pyplot as plt
from lvisf2_processing import get_polygon
from img_processing import get_img_lon_lat

folder = r'56133_to_56249'

def plot_polygon(folder):
    '''
    :plot_polygon: Displays figure showing altimetry boundary
                   polygon and coincident imagery locations.

    :return: None.
    '''
    txtxmlfile = glob.glob("E:\spatially_sorted_lvisf2_is2olvis1bcv\\"+folder+"\\*.TXT.xml")[0]
    txtlon, txtlat = get_polygon(txtxmlfile)

    imgfiles = "E:\spatially_sorted_lvisf2_is2olvis1bcv\\"+folder+"\\*.TIF.xml"
    imglon = []
    imglat = []
    for imgxmlfile in glob.glob(imgfiles):
        new_lon, new_lat = get_img_lon_lat(imgxmlfile)
        imglon.append(new_lon)
        imglat.append(new_lat)

    plt.figure(figsize=(8,8))
    plt.axis('equal')
    plt.fill(txtlon,txtlat)
    plt.scatter(imglon,imglat, c= 'red')
    plt.show()
    return

plot_polygon(folder)