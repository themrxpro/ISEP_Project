import face_recognition
import myfunc_mysql as sql
import numpy as np
import myfunc_filehandler as fh
import myfunc_mysql as sql



def get_faces(file):
    faces = []
    lf = face_recognition.load_image_file(file)
    face_locations = face_recognition.face_locations(lf)
    encodes = face_recognition.face_encodings(lf, face_locations)
    #print(type(encodes[0]))
    #print(face_recognition.face_distance([encodes[0]], encodes[0]))
    #print(encodes[1])
    for face_xy, encode in zip(face_locations, encodes):
        #face_recognition.compare_faces(df_Conhecidos["encodes"])
        faces.append([face_xy, encode])
    return faces

def compare_faces(face,df):
    known_faces = df['encode'].tolist()
    list = face_recognition.face_distance(known_faces, face)
    if np.amin(list) <= tolerance:
        resp = np.where(list == np.amin(list))
        return df['person_id'][resp[0][0]]
    else:
        return 1

#faces = get_faceEncodes(file)
loc=(215,844,854,256)
#sql.addFace('000067a4d951bb4e0385d7eeb0b67d34', 2, '{0}'.format(loc), '{0}'.format(face_1))

def getPersonID(face,df):
    if df.empty:
        return 1
    else:
        return compare_faces(face,df)
def loadEncodes():
    df=sql.getKnownFaces()
    for x in range(len(df)):
        string = df['encode'][x]
        string = string.replace(r'\n', '')
        df.at[x,'encode'] = np.fromstring(string, dtype=float,count=-1, sep=' ')
    return df

#def RequestUnkown():

'''
returnar hash_id, face_xy , encode
para depois adicionar o nome ao encode
'''



def processPhoto(hash_id, df, file):
    #file = fh.hashes.loc[fh.hashes['hash_id'] == hash_id]['file_location'].iloc[0]
    faces = get_faces(file)
    for face in faces:
        face_id = getPersonID(face[1],df)

        sql.addFace(hash_id, face_id, face[0], f'{face[1]}')
        df = df.append({'person_id':face_id,'encode':face[1]}, ignore_index=True)

tolerance = 0.6

