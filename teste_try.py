from multiprocessing import Process, Manager
import pandas as pd
import time
def f(d, l):
    while d['close_flag'] == False:

        d[1] = '1'
        d['2'] = 2
        d[0.25] = None
        l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        df = pd.DataFrame()
        d = manager.dict()

        d['close_flag'] = False
        d['process_status'] = False
        d['df'] = df
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        time.sleep(4)

        d['close_flag'] = True
        p.join()

'''
def faceWorker():
    global Global_labelText

    while close_thread == None:
        time.sleep(1)
        print('sleeping')

    while not close_thread:
        pending = hashes[hashes.face_proc == 0].shape[0]
        Global_labelText = 'Reconhecimento Facial : a processar {} foto(s)'.format(pending)
        if not pending == 0:
            fileToProcess = hashes.loc[hashes['face_proc'] == 0].iloc[0]
            file_index = hashes.loc[hashes['hash_id'] == fileToProcess.hash_id].index[0]

            print(f'Processing {fileToProcess.hash_id}')
            #face.processPhoto(fileToProcess.hash_id)

            new_worker = multiprocessing.Process(
                target=face.processPhoto,
                args=(fileToProcess.hash_id, df_encodes)
            )

            #hashes.set_value(file_index, 'face_proc', 1)
            hashes.at[file_index,'face_proc'] = 1

            sql.updateFace_proc(fileToProcess.hash_id)
            print('Done')
        else:
            time.sleep(1)
            print('Waiting for files')
'''
'''
import multiprocessing as mp
import time
def func_worker(d):
    i=0
    while not d['stop_flag'] == True:
        d[] = i
        time.sleep(1)
        i+=1
        print(i)

if __name__ == '__main__':
    with mp.Manager() as manager:
        d = manager.dict()

        #d['hashes']= df
        #d['stop_flag'] = False

        p = mp.Process(target=func_worker, args=(d))
        p.start()

        d['stop_flag'] = True
        time.sleep(5)
        p.join()

'''
