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
import myfunc_mysql as sql      # sql
import myfunc_exif as exif      # exif
import myfunc_filehandler as fh          # file_handling
import myfunc_debug as debug    # debug
import myfunc_checks as checks  # checks
import myfunc_config as config



if __name__ == '__main__':

    #TODO AMANHA !!!
    # criar uma boa forma de testar tudo .zip
    # dar o porte dos funcoes para uma interface !
    # arrumar com os "tudo" urgentes que já sao possiveis de resolver com interface
    # Comecar os querrys basicos

    #todo dois tipos diferentes de flags debug test(recebe prints), debug reset

    #todo verificar em que momentos sao verificados as configs\pastas\engine
    #ordem:
    # config primeiro: uma vez que todas as outras necessitam destas configuracoes
    # base de dados, e depois as pastas e assim.
    # como configuraçao inicial, apresentar janela ao utilizador, ja com valores default
    checks.check_config()

    engine = sql.checkConnection()
    debug.resetALL(True, engine)


    checks.check_allfolders()


    #todo manual para já
    input_folder = r'.\TEST FOLDER 1'

    results = fh.add_newfiles(input_folder) #todo df, results
    print(results)
    #todo clear folders insisde input folder (or input folder itself)
    #todo teste de duas fases com a segunda com duplicados para testar as duas condicoes
    # todo englobar esta main como funcao para ser chamada pelo GUI de adicionar fotos
    # todo criar um ambiente de teste bom com todos os casos possiveis !!!
    # todo check if there is need to close connection
    # todo funcoes de QUERRYs para encontrar fotografias
    # todo GUI para adicionar eventos, com o processamento posterior à criacao do mesmo
    # todo processamento do reconhecimento facial GUI para adicionar caras conhecidas
    #   arrancar um subprocesso para ir adicionanado as fotografias de forma passiva
    #   ou dar a escolher ao utilizador um botao para ativar os cores todos (mais a frente X% cores)
    # todo testes
    #   funcoes para debug
    #       verificar o numero correto de fotografias em dado caso: c/ GPS
    #todo setting change output directory must move all previous files
    #todo file location output + \ + [2020\2020-1.23] guardar apenas o essencial !
    ## TODO LATER ##
    # todo perguntar a configuraçao do mysql
    # todo alterar configuracoes a meio do programa
    # todo interromper de forma segura o programa
    # todo thumbnails folder hidden
    # todo progress bar das fotos adicionadas
    # todo GUI para:
    #   o user selecionar a pasta para adicionar novas fotografias
    #   selecionar para onde vao as fotografias
    # todo instalar dlib com os cuda cores ativos


