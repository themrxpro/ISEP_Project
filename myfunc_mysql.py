from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import myfunc_config as config
import re
import os
'''
user = 'root'
passwd = 'themrxpro'
host = 'localhost'
port = '3306'
db_name = 'sql_photos'

url = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(user, passwd, host, port, db_name)
'''

### Test
def reset_db():
    engine.execute('drop database `{0}`'.format(config.get_SQLconfig('db_name')))

def checkConnection():
    # this only runs after import is made to update engine
    global url
    global engine
    try:
        url = config.get_SQLconfig('url')
        engine = create_engine(url, echo=False)
        createDB()
        engine.connect()
        return True
    except:
        return False

###
def createDB():
    if not database_exists(url):
        create_database(url)
        engine.execute("USE {0}".format(config.get_SQLconfig('db_name')))

    if not engine.dialect.has_table(engine, 'Photo'):
        engine.execute("""CREATE TABLE `Photo` (
                        `hash_id` varchar(128) PRIMARY KEY,
                        `file_location` varchar(256) NOT NULL,
                        `date` timestamp,
                        `gps` text,
                        `face_proc` BOOLEAN NOT NULL DEFAULT false);""")
    if not engine.dialect.has_table(engine, 'Person'):
        engine.execute("""CREATE TABLE `Person` (
                        `person_id` int PRIMARY KEY AUTO_INCREMENT,
                        `name` varchar(64));""")
    if not engine.dialect.has_table(engine, 'Event'):
        engine.execute("""CREATE TABLE `Event` (
                        `event_id` int PRIMARY KEY AUTO_INCREMENT,
                        `event_name` varchar(64),
                        `start_date` date,
                        `end_date` date);""")
    if not engine.dialect.has_table(engine, 'Photo_Person'):
        engine.execute("""CREATE TABLE `Photo_Person` (
                        `hash_id` varchar(128),
                        `person_id` int,
                        `face_xy` varchar(32),
                        `encode` text,
                        FOREIGN KEY (`hash_id`)
                            REFERENCES `Photo`(`hash_id`)
                            ON DELETE CASCADE,
                        FOREIGN KEY (`person_id`)
                            REFERENCES `Person`(`person_id`)
                            ON DELETE CASCADE);""")
    if not engine.dialect.has_table(engine, 'Photo_Event'):
        engine.execute("""CREATE TABLE `Photo_Event` (
                        `hash_id` varchar(128),
                        `event_id` int,
                        FOREIGN KEY (`hash_id`)
                            REFERENCES `Photo`(`hash_id`)
                            ON DELETE CASCADE,
                        FOREIGN KEY (`event_id`)
                            REFERENCES `Event`(`event_id`)
                            ON DELETE CASCADE);""")
    try:
        engine.execute("INSERT INTO `Person` VALUES ( 1 , 'Unkown')")
        engine.execute("INSERT INTO `Person` VALUES ( 2 , 'Ignore')")
    except:
        pass
def loadHashes():
    SQL_Query = pd.read_sql_query('''
        SELECT hash_id, file_location, face_proc  
        FROM photo''', engine)
    df = pd.DataFrame(SQL_Query, columns=['hash_id', 'file_location', 'face_proc'])
    df['file_location'] = df['file_location'].str.replace('@', r'{}'.format(config.get_USERconfig("output_folder")), regex=True)
    return df


def addPhoto(hash_id, file_location, date, gps):
    SQL_INSERT = "INSERT INTO `Photo` VALUES ('{0}', '{1}' , '{2}', '{3}', default)".format(
        hash_id,
        file_location.replace('\\', '\\\\'),
        date,
        gps
    )
    sql_response = engine.execute(SQL_INSERT)
    return sql_response

def addFace(hash_id, person_id, face_xy, encode):
    encode = encode.replace('[', '')
    encode = encode.replace(']', '')

    SQL_INSERT = "INSERT INTO `Photo_Person` VALUES ('{0}', '{1}' , '{2}', '{3}')".format(
        hash_id,
        person_id,
        face_xy,
        encode
    )
    sql_response = engine.execute(SQL_INSERT)
    return sql_response

def getKnownFaces():
    SQL_Query = pd.read_sql_query("Select person_id, encode from photo_person where person_id > 2", engine)
    df = pd.DataFrame(SQL_Query, columns=['person_id', 'encode'])
    return df

def getUnknownFaces():
    SQL_Query = pd.read_sql_query("Select hash_id, face_xy, encode from photo_person where person_id = 1 Limit 1", engine)
    df = pd.DataFrame(SQL_Query, columns=['hash_id', 'face_xy', 'encode'])
    return df['hash_id'][0], df['face_xy'][0], df['encode'][0]

def updateFace_proc(hash_id):
    SQL_INSERT = "update Photo set face_proc = 1 where hash_id = '{}' ".format(hash_id)
    sql_response = engine.execute(SQL_INSERT)
    return sql_response
try:
    url = config.get_SQLconfig('url')
    engine = create_engine(url, echo=False)
    createDB()
    engine.connect()
except:
    raise ImportError