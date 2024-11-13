#!/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :rtype: float
    """

    return value[0] + (value[1] / 60.0) + (value[2] / 3600.0)


def get_gps(filepath):
    img = Image.open(filepath)
    exif_data = img._getexif()

    exif_table = {}
    for tag, value in exif_data.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value

    gps_info = {}
    for key in exif_table['GPSInfo'].keys():
        decode = GPSTAGS.get(key,key)
        gps_info[decode] = exif_table['GPSInfo'][key]

    print(gps_info)

    latitude = gps_info['GPSLatitude']
    latitude_ref = gps_info['GPSLatitudeRef']
    longitude = gps_info['GPSLongitude']
    longitude_ref = gps_info['GPSLongitudeRef']
    print(latitude, latitude_ref, longitude, longitude_ref)

    if latitude:
        lat_value = _convert_to_degress(latitude)
        if latitude_ref != 'N':
            lat_value = -lat_value
    else:
        return {}
    if longitude:
        lon_value = _convert_to_degress(longitude)
        if longitude_ref != 'E':
            lon_value = -lon_value
    else:
        return {}
    return {'latitude': lat_value, 'longitude': lon_value}


file_path = 'PXL_20241110_235925674.jpg'
gps = get_gps(file_path)
print (gps)