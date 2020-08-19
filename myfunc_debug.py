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
import myfunc_checks as checks  # checks


def resetALL(debug_mode, engine):
    if debug_mode:

        resetFolders()
        resetConfig()

def resetConfig():
    if os.path.isfile(r'\config.ini'):
        os.remove(r'\config.ini')


def resetFolders():
    # deletes Test Folders & output folders
    all_folders = [r'.\Input Folder', r'.\Output Folder', r'.\Thumbnails']
    for folders in all_folders:
        try:
            shutil.rmtree(folders)
        except:
            pass
    # unzips test files
    with ZipFile(r'.\test.zip', 'r') as zip_ref:
        zip_ref.extractall(r'.')


def debug_print(string):
    if debug_mode:
        print('# DEBUG: {}'.format(string))
