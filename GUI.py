# SQLconnection = sql.checkConnection()

def addFolder():
    global input_folder

    # labelFolder = tk.Label(frame, text=input_folder)
    # labelFolder.pack()
    print(input_folder)


def display_title(string):
    label = tk.Label(subDisplay, text=string, font=("Helvetica", 20), bg='white', justify=LEFT)
    label.grid(row=0, column=0)


def confirmSettings(labels, params, values):
    # todo mudar para verde se ok
    global SQLimported, sql
    global forceSettings
    for param, value in zip(params, values):
        value = value.get()
        if param in ['output_folder', 'duplicate_folder']:
            if not config.get_USERconfig(param) == value:
                if checks.check_folder(param):
                    fh.move_folder(config.get_USERconfig(param), value)
                    # falta mover no check_folder se existir items. se for output, atualizar DB !!!!

                    config.changeConfig('user', param, value)

            # proceder com as definicoes
        if param in ['user', 'passwd', 'host', 'port', 'db_name']:
            if not config.get_SQLconfig(param) == value:
                config.changeConfig('sql', param, value)
            # testar ligacao e se ok mudar settings

        if param == 'db_name':  # ultimo elemento a ser verificado, testar conexao

            # ver isto ! importar so se ainda nao se tiver importado
            if SQLimported:
                forceSettings = not (sql.checkConnection())
            else:
                try:
                    import myfunc_mysql as sql
                    SQLimported = True
                    forceSettings = False
                except:
                    forceSettings = True
            if forceSettings:
                labels[2].config(text='mySQL:  ERROR', fg="red")
            else:
                labels[2].config(text='mySQL:  OK', fg='green')
                face.close_thread = False

def fillpathButton(entry):
    # create button with ...
    path = filedialog.askdirectory(title='Selecionar Pasta')
    print('path')
    entry.delete(0, END)
    entry.insert(0, path)
    # file to open default
    # where to put info
    # return buttontype


def ba_addFiles(entry, label1, label2):
    label1.config(text='Estado : A adicionar ficheiros')
    resp = fh.add_newfiles(entry)
    label1.config(text='Estado : Ficheiros Adicionados')
    label2.config(text=resp)

def showDisplay(type):
    global subDisplay
    subDisplay.destroy()
    subDisplay = tk.Frame(frameDisplay, bg='white')
    subDisplay.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    if type == 'photo':
        display_title('Adicionar Fotografias')
        label = tk.Label(subDisplay, text='Selecionar Pasta com as fotografias :', font=("Helvetica", 12), bg='white',
                         justify=LEFT)
        label.grid(row=1, column=0)
        entryFolder = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black', width=100)
        entryFolder.grid(row=2, column=0)
        button3dot = tk.Button(subDisplay, text="...", padx=5, pady=1, command=lambda: fillpathButton(entryFolder))
        button3dot.grid(row=2, column=1)
        label_status = tk.Label(subDisplay, text='Estado :', font=("Helvetica", 12), bg='white', justify=LEFT)
        label_status.grid(row=4, column=0)
        label_results = tk.Label(subDisplay, text='', font=("Helvetica", 12), bg='white', justify=LEFT)
        label_results.grid(row=5, column=0)
        button_add = tk.Button(subDisplay, text="Adicionar Fotos", padx=20, pady=6,
                               command=lambda: ba_addFiles(entryFolder.get(), label_status, label_results))
        button_add.grid(row=3, column=0)

    if type == 'person':
        display_title('Adicionar Pessoa')


        try:
            hash_id, face_xy, encode = sql.getUnknownFace()
            if fh.hashes == 'notloaded':
                fh.hashes = sql.loadHashes()
                face.close_thread = False
            img = PIL.ImageTk.PhotoImage(Image.open(fh.hashes.loc[fh.hashes['hash_id'] == hash_id]['file_location'].item()))
            panel = tk.Label(subDisplay, image=img)
            panel.grid(row=1, column=0)
        except:
            label = tk.Label(subDisplay, text='Não ha pessoas desconhecidas para apresentar', font=("Helvetica", 12),
                             bg='white', justify=LEFT)
            label.grid(row=1, column=0)
    if type == 'event':
        display_title('Adicionar Evento')

    if type == 'search':
        display_title('Pesquisa')

    if type == 'settings':
        param = ['output_folder', 'duplicate_folder', 'user', 'passwd', 'host', 'port', 'db_name']
        values = []
        labels = []
        display_title('Definições')
        # Def Utilizador
        label = tk.Label(subDisplay, text='Utilizador', font=("Helvetica", 12), bg='white', justify=LEFT)
        label.grid(row=1, column=0)

        dvalue = config.get_USERconfig('output_folder')
        label = tk.Label(subDisplay, text='Localizacao :', font=("Helvetica", 8), bg='white')
        label.grid(row=2, column=0)
        eu1 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black', width=100)
        eu1.grid(row=2, column=1)
        eu1.insert(0, dvalue)
        labels.append(label)

        dvalue = config.get_USERconfig('duplicate_folder')
        label = tk.Label(subDisplay, text='Duplicados :', font=("Helvetica", 8), bg='white')
        label.grid(row=3, column=0)
        eu2 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black', width=100)
        eu2.grid(row=3, column=1)
        eu2.insert(0, dvalue)
        labels.append(label)

        # Def SQL
        label = tk.Label(subDisplay, text='mySQL', font=("Helvetica", 12), bg='white', justify=LEFT)
        label.grid(row=4, column=0)
        labels.append(label)
        dvalue = config.get_SQLconfig('user')
        label = tk.Label(subDisplay, text='user :', font=("Helvetica", 8), bg='white')
        label.grid(row=5, column=0)
        es1 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black')
        es1.grid(row=5, column=1, sticky=W)
        es1.insert(0, dvalue)

        dvalue = config.get_SQLconfig('passwd')
        label = tk.Label(subDisplay, text='passwd :', font=("Helvetica", 8), bg='white')
        label.grid(row=6, column=0)
        es2 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black', show="*")
        es2.grid(row=6, column=1, sticky=W)
        es2.insert(0, dvalue)

        dvalue = config.get_SQLconfig('host')
        label = tk.Label(subDisplay, text='host :', font=("Helvetica", 8), bg='white')
        label.grid(row=7, column=0)
        es3 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black')
        es3.grid(row=7, column=1, sticky=W)
        es3.insert(0, dvalue)

        dvalue = config.get_SQLconfig('port')
        label = tk.Label(subDisplay, text='port :', font=("Helvetica", 8), bg='white')
        label.grid(row=8, column=0)
        es4 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black')
        es4.grid(row=8, column=1, sticky=W)
        es4.insert(0, dvalue)

        dvalue = config.get_SQLconfig('db_name')
        label = tk.Label(subDisplay, text='db_name :', font=("Helvetica", 8), bg='white')
        label.grid(row=9, column=0)
        es5 = tk.Entry(subDisplay, font=("Helvetica", 8), bg='white', fg='black')
        es5.grid(row=9, column=1, sticky=W)
        es5.insert(0, dvalue)

        values.extend([eu1, eu2, es1, es2, es3, es4, es5])
        confirmButton = tk.Button(
            subDisplay, padx=60, pady=20, bg='grey', fg='white', text="Confirmar Definições",
            command=lambda: confirmSettings(labels, param, values)
        )
        confirmButton.grid(row=10, column=1)
    '''
    config['user'] = {
        'output_folder': r'.\Output Folder',
        'duplicate_folder': r'.\Duplicate Folder'
    }
    config['sql'] = {
        'user': 'root',
        'passwd': 'themrxpro',
        'host': 'localhost',
        'port': '3306',
        'db_name': 'sql_photos'
    }
    '''
def updateLabel(label):
    label.config(text=fh.Global_labelText)
    label.after(1000,lambda: updateLabel(label))

def createWindow():
    global frameMenu, frameDisplay, subDisplay

    # CREATES FRAME - MENU
    frameMenu = tk.Frame(root, bg='black')
    frameMenu.place(relwidth=0.3, relheight=1)
    subMenu = tk.Frame(frameMenu, bg='black')
    subMenu.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
    # CREATES FRAMES - DISPLAY
    frameDisplay = tk.Frame(root, bg='white')
    frameDisplay.place(relwidth=0.7, relx=0.3, relheight=1)
    subDisplay = tk.Frame(frameDisplay, bg='white')
    subDisplay.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    face_status = tk.Label(frameDisplay, text='Starting', font=("Helvetica", 12), bg='white', justify=LEFT)
    face_status.place(relx = 1.0,rely = 1.0, anchor='se')
    updateLabel(face_status)

    # MENU OPTIONS
    size_x = 120
    size_y = 40

    menu_addfoto = tk.Button(
        subMenu, padx=size_x, pady=size_y, bg='black', fg='white', text="Adicionar Fotografias",
        command=lambda: showDisplay('photo'))
    menu_addperson = tk.Button(
        subMenu, padx=size_x, pady=size_y, bg='black', fg='white', text="Adicionar Pessoa",
        command=lambda: showDisplay('person'))
    menu_addevent = tk.Button(
        subMenu, padx=size_x, pady=size_y, bg='black', fg='white', text="Adicionar Evento",
        command=lambda: showDisplay('event'))
    menu_search = tk.Button(
        subMenu, padx=size_x, pady=size_y, bg='black', fg='white', text="Pesquisa",
        command=lambda: showDisplay('search'))
    menu_settings = tk.Button(
        subMenu, padx=size_x, pady=size_y, bg='black', fg='white', text="Definições",
        command=lambda: showDisplay('settings'))

    menu_addfoto.pack()
    menu_addperson.pack()
    menu_addevent.pack()
    menu_search.pack()
    menu_settings.pack()


if __name__ == '__main__':
    # init
    import myfunc_config as config
    import os

    if not os.path.isfile(r'\config.ini'): config.create_config()
    try:
        import myfunc_mysql as sql

        forceSettings = False
        SQLimported = True
    except ImportError:
        forceSettings = True
        SQLimported = False
    import tkinter as tk
    from tkinter import filedialog, Text
    from tkinter import BOTH, END, LEFT, W
    # import myfunc_mysql as sql
    import myfunc_checks as checks
    import myfunc_filehandler as fh
    import myfunc_face as face
    import threading
    import PIL
    #start thread here


    root = tk.Tk()
    input_folder = ''
    canvas = tk.Canvas(root, height=700, width=1200)
    canvas.pack()
    # todo block window size
    ### LEFT FRAME
    createWindow()
    showDisplay('settings')

    worker = threading.Thread(target=fh.face_Manager)
    worker.start()

    root.mainloop()
    #todo end_tread
    if fh.close_thread == None:
        worker.exit()
    else:
        fh.close_thread = True
        worker.join()

