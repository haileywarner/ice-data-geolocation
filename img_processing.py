import xml.etree.ElementTree as et
import matplotlib.pyplot as plt

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
    utc = float(military[0:2])*3600 + float(military[2:4])*60 + float(military[4:6])
    return utc


def get_img_lon_lat(xmlfile):
    '''
    get_img_lon_lat : Parses longitude and latitude of aerial image.

                         Coordinate is roughly the geometric center of the image.
                         (IceBridge Dataset: IS2OLVIS1BCV (https://nsidc.org/data/is2olvis1bcv/versions/1))

    :xml_file: path to .xml file.
    :return: lat (float), lon (float).
    '''
    tree = et.parse(xmlfile)
    root = tree.getroot()
    lat = float(root[2][8][0][0][0][0][1].text)
    lon = float(root[2][8][0][0][0][0][0].text)
    return lat, lon
