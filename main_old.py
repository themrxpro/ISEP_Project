import csv
import os
import time
from datetime import datetime
from hashlib import md5
from PIL import Image
import shutil
from zipfile import ZipFile
import myfunc_mysql as mysql_func


'''
Constantes em todas as imagens:
    ID
    Nome do ficheiro
    Localizaçao
    Hash
    Data
'''


def get_img_date(fn):
    try:
        "returns the image date from image (if available)\nfrom Orthallelous"
        std_fmt = '%Y:%m:%d %H:%M:%S'
        # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
        tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
                (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
                (306, 37520), ]  # (DateTime, SubsecTime)
        exif = Image.open(fn)._getexif()

        for t in tags:
            dat_stmp = exif.get(t[0])
            sub_stmp = exif.get(t[1], 0)

            # PIL.PILLOW_VERSION >= 3.0 returns a tuple
            dat_stmp = dat_stmp[0] if type(dat_stmp) == tuple else dat_stmp
            sub_stmp = sub_stmp[0] if type(sub_stmp) == tuple else sub_stmp
            if dat_stmp != None: break

        # if dat_stmp == None: return None
        full = '{}'.format(dat_stmp)
        T = datetime.strptime(full, std_fmt)
        T = str(T)
    except:
        T = time.ctime(os.path.getmtime(fn))
        T = datetime.strptime(T, "%a %b %d %H:%M:%S %Y")
        T = str(T).replace(":", ".")
    return T

def file_hash(filepath):
    with open(filepath, 'rb') as f:
        return md5(f.read()).hexdigest()

#### Variaveis

debug_mode = True

# Do dev

thumbnail_size = (300, 300)
thumbnail_path = r'.\Thumbnails'

# Do utilizador
output_folder = r'.\Output Folder'
input_folders = [r'.\TEST FOLDER 1']

# Do sistema



def debug_print(string):
    if debug_mode:
        print('# DEBUG: {}'.format(string))


if __name__ == '__main__':  

    if not os.path.exists(db_files_location):
        # Creates file if does not exist
        debug_print("Db does not exist, creating new")
        with open(db_files_location, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
            csv_writer.writeheader()

    else:
        with open(db_files_location, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='\t')
            check_fieldnames = csv_reader.fieldnames
            # if it exists check if it is correct
            if check_fieldnames == fieldnames:
                debug_print("Db correct, loading")
                for line in csv_reader:
                    hash_list.append(line['hash'])
                debug_print('{} hashes loaded'.format(len(hash_list)))
            # if ok get hashes
            else:
                # not ok, create new db
                debug_print("Db incorrect, creating new")
                csv_file.close()
                with open(db_files_location, 'w', newline='') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
                    csv_writer.writeheader()
    # DEBUG: resets db for test purposes
    if debug_mode:
        #deletes Test Folders & output folders
        all_folders=[r'.\TEST FOLDER 1', r'.\TEST FOLDER 2',r'.\Output Folder',r'.\Thumbnails']
        for folders in all_folders:
            try:
                shutil.rmtree(folders)
            except:
                pass
        # unzips test files
        with ZipFile(r'.\test.zip', 'r') as zip_ref:
            zip_ref.extractall(r'.')

        hash_list = []
        with open(db_files_location, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')
            csv_writer.writeheader()



    # verificar se existe a pasta thumbnail
    if not os.path.isdir(thumbnail_path):
        os.mkdir(thumbnail_path)
    # verificar se existe a pasta output
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for folder in input_folders:
        for root, dirnames, filenames in os.walk(folder):
            for filename in filenames:

                # get hash check and save
                this_hash = file_hash(os.path.join(root, filename))

                if this_hash not in hash_list:
                    hash_list.append(this_hash)

                    this_date = get_img_date(os.path.join(root,filename))
                    this_thumbnail_path = '{}\{}{}'.format(thumbnail_path, this_hash, os.path.splitext(filename)[1])

                    with open(db_files_location, 'a', newline='',encoding='utf-8') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')


                        if not os.path.isfile(this_thumbnail_path):
                            i = Image.open(os.path.join(root, filename))
                            i.thumbnail(thumbnail_size)
                            i.save(this_thumbnail_path)
                            debug_print('Tn created - '+this_thumbnail_path)

                        shutil.move(os.path.join(root,filename),os.path.join(output_folder,filename))

                        info = {
                            "hash": this_hash,
                            "name": filename,
                            "path": os.path.join(root, filename),
                            "date": this_date
                        }
                        csv_writer.writerow(info)

                # file already exists
                # else:

                # get id and save id
                # save name
                # save apth
