import os
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def plot_altimetry_track(txtxmlfile):
    '''
    plot_altimetry_track : 

    :txtxmlfile: path to .TXT.xml file.
    :return:
    '''

    polygon_points = []
    tree = et.parse(txtxmlfile)
    root = tree.getroot()
    p = root.iter('Point')
    #print(sum(1 for _ in p))
    for i in range(0,sum(1 for _ in p)-1):
        lon = float(root[2][8][0][0][0][i][0].text)
        lat = float(root[2][8][0][0][0][i][1].text)
        polygon_points.append((lon,lat))
    print(polygon_points)
        #matplotlib fill()

    return


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
    t0 = float(start_military[0:2])*3600 + float(start_military[2:4])*60 + float(start_military[4:6])
    tn = float(end_military[0:2])*3600 + float(end_military[2:4])*60 + float(end_military[4:6])
    return t0, tn


def get_txt_time_range(txtfile):

    '''
    get_txt_time_range : Parses LVISF2 TXT files for start and end time of segment in UTC decimal seconds per day.

                         (IceBridge Dataset: LVISF2 (https://nsidc.org/data/lvisf2/versions/1))

    :xml_file: path to .TXT file.
    :return:   t0 (s), tn (s)
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
