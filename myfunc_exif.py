import csv
import os
import time
from datetime import datetime
from hashlib import md5
from PIL import Image
from PIL.ExifTags import TAGS
import shutil
from zipfile import ZipFile
import pandas as pd

# MY FUNC'S
#import myfunc_mysql as sql  # sql
import myfunc_debug as debug  # debug
import myfunc_checks as checks  # checks
import myfunc_config as config

from PIL.ExifTags import TAGS


###
##      GPS
###
def get_decimal_from_dms(dms, ref):
    try:
        degrees = dms[0]
        minutes = dms[1] / 60.0
        seconds = dms[2] / 3600.0
    except:
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(gps):
    lat = get_decimal_from_dms(gps[2], gps[1])

    lon = get_decimal_from_dms(gps[4], gps[3])

    return (lat, lon)


def getGPS(fn):
    try:
        exif = Image.open(fn)._getexif()
        gps_exif = exif.get(34853)
        return get_coordinates(gps_exif)
    except:
        return ''


###
##      DATETIME
###

def get_img_date(fn):
    try:
        std_fmt = '%Y:%m:%d %H:%M:%S'
        tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
                (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
                (306, 37520), ]  # (DateTime, SubsecTime)
        exif = Image.open(fn)._getexif()

        for t in tags:
            dat_stmp = exif.get(t[0])
            sub_stmp = exif.get(t[1], 0)

            dat_stmp = dat_stmp[0] if type(dat_stmp) == tuple else dat_stmp
            sub_stmp = sub_stmp[0] if type(sub_stmp) == tuple else sub_stmp
            if dat_stmp != None: break

        full = '{}'.format(dat_stmp)
        T = datetime.strptime(full, std_fmt)
    except:
        T = time.ctime(os.path.getmtime(fn))
        T = datetime.strptime(T, "%a %b %d %H:%M:%S %Y")
    return str(T)
