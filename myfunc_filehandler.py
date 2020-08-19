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
from multiprocessing import Process, Manager
# MY FUNC'S  # sql
import myfunc_exif as exif  # exif
import myfunc_debug as debug  # debug
import myfunc_checks as checks  # checks
import myfunc_config as config
import myfunc_face as face


def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()


def create_tn(fn, hash):
    tn_folder = config.get_DEVconfig('thumbnail_folder')
    tn_size = config.get_DEVconfig('thumbnail_size')
    i = Image.open(fn)
    i.thumbnail((tn_size, tn_size))
    i.save(r'{}\{}{}'.format(tn_folder, hash, os.path.splitext(fn)[1]))

def move_folder(old,new):
    try:
        list_dir = os.listdir(old)
        for sub_dir in list_dir:
            dir_to_move = os.path.join(old, sub_dir)
            shutil.move(dir_to_move, new)
        os.rmdir(old)
    except: pass
def move_file(path, date):
    year = str(datetime.strptime(date, '%Y-%m-%d %H:%M:%S').year)
    i = 0
    path_folder = r'{0}\{1}'.format(config.get_USERconfig('output_folder'), year)
    path_file = str(date.replace(":", "."))
    path_ext = os.path.splitext(os.path.split(path)[1])[1]
    new_path = r'{0}\{1}{2}'.format(path_folder, path_file, path_ext)
    print(os.path.isdir(path_folder))
    if not os.path.isdir(path_folder):
        os.makedirs(path_folder)
    while os.path.isfile(new_path):
        i += 1
        new_path = r'{0}\{1} ({2}){3}'.format(path_folder, path_file, i, path_ext)
    os.rename(path, new_path)
    return new_path


def move_duplicate(path):  # moves file to trash

    i = 0
    path_folder = config.get_USERconfig('duplicate_folder')
    path_file = os.path.splitext(os.path.split(path)[1])[0]
    path_ext = os.path.splitext(os.path.split(path)[1])[1]
    new_path = r'{0}\{1}{2}'.format(path_folder, path_file, path_ext)

    while os.path.isfile(new_path):
        i += 1
        new_path = r'{0}\{1}({2}){3}'.format(path_folder, path_file, i, path_ext)
    os.rename(path, new_path)


def add_newfiles(folder):
    import myfunc_mysql as sql

    dup = 0
    added = 0
    new_files = []
    global hashes

    sup_img = [".jpg", ".JPG", ".png", ".PNG", ".jpeg"]

    checks.check_allfolders()

    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[1] in sup_img:
                new_files.append(r'{0}\{1}'.format(root, filename))

    for file in new_files:
        this_hash = file_hash(file)

        if not hashes.hash_id.eq(this_hash).any():
            this_time = exif.get_img_date(file)
            this_gps = exif.getGPS(file)
            create_tn(file, this_hash)
            file = move_file(file, this_time)
            sql.addPhoto(this_hash, file.replace(config.get_USERconfig('output_folder'), '@'), this_time, this_gps)

            #new_hashes.append(this_hash)
            hashes = hashes.append({
                'hash_id': this_hash,
                'file_location': file,
                'face_proc': 0
            }, ignore_index=True)
            print('{}{}{}'.format(this_hash,file,0))
            added += 1
            # todo adicionar em dataframe parecido com o inicial para dar apend de forma a evitar um segundo querry para processaamento posterior
        else:

            move_duplicate(file)
            dup += 1
    results = ('''
        Numero de ficheiros: {0}
        Ficheiros Adicionados: {1}
        Ficheiros Duplicados: {2}

        '''.format(len(new_files), added, dup)
               )
    return results

def face_Worker(d):
    while d['close_flag'] == False:
        if not d['fileToProcess'] == None:
            #d['is_processing'] = True
            face.processPhoto(d['hashToProcess'], d['dataframe'], d['fileToProcess'])
            d['is_processing'] = False
            d['hashToProcess'] = None
            d['fileToProcess'] = None
        time.sleep(1)

def face_Manager():
    global Global_labelText
    start_process = False
    while close_thread == None:
        time.sleep(1)
        print('sleeping')

    with Manager() as manager:
        d = manager.dict()
        d['close_flag'] = False
        d['is_processing'] = False
        d['fileToProcess'] = None
        d['dataframe'] = face.loadEncodes()
        print(d)
        p = Process(target=face_Worker, args=(d,))


        while not close_thread:
            if start_process == False:
                p.start()
                start_process = True

            pending = hashes[hashes.face_proc == 0].shape[0]
            Global_labelText = 'Reconhecimento Facial : a processar {} foto(s)'.format(pending)

            if not pending == 0:
                fileToProcess = hashes.loc[hashes['face_proc'] == 0].iloc[0]
                file_index = hashes.loc[hashes['hash_id'] == fileToProcess.hash_id].index[0]

                if d['is_processing'] == False:
                    d['is_processing'] = True
                    print(f'Processing {fileToProcess.hash_id}')
                    d['fileToProcess'] = fileToProcess.file_location
                    d['hashToProcess'] = fileToProcess.hash_id
                    hashes.at[file_index, 'face_proc'] = 1

                    sql.updateFace_proc(fileToProcess.hash_id)
                    print('Done')
            else:
                time.sleep(1)
                print('Waiting for files')
        d['close_flag'] = True
        p.join()


hashes = pd.DataFrame()
df_encodes = pd.DataFrame()
try:
    import myfunc_mysql as sql
    hashes = sql.loadHashes()
    close_thread = False
    Global_labelText = ''
    df_encodes = face.loadEncodes()
except:
    hashes = 'notloaded'