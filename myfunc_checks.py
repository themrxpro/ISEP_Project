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
import myfunc_exif as exif  # exif
import myfunc_filehandler as fh  # file_handling
import myfunc_debug as debug  # debug
import myfunc_checks as checks  # checks
import myfunc_config as config

#todo eliminar checkALL
'''def checkALL():
    check_config()
    sql.create_engine()
    sql.db_check()
    check_folders()
'''

def check_config():
    if not os.path.isfile(r'\config.ini'):
        config.create_config()

def check_allfolders():
    thumbnail_path = config.get_DEVconfig('thumbnail_folder')
    if not os.path.isdir(thumbnail_path):
        os.mkdir(thumbnail_path)

    output_folder = config.get_USERconfig('output_folder')
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    duplicate_folder = config.get_USERconfig('duplicate_folder')
    if not os.path.isdir(duplicate_folder):
        os.mkdir(duplicate_folder)
def check_folder(folder):
    #todo MOVE HERE
    try:
        folder = config.get_USERconfig('output_folder')
        if not os.path.isdir(folder):
            os.mkdir(folder)
        return True
    except:
        return False
