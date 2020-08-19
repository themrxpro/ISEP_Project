import configparser

def get_options(param):
    parser = configparser.ConfigParser()
    parser.read(r'.\config.ini')
    return parser.options(param)

def create_config():
    config = configparser.ConfigParser()
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
    config['dev - DONT CHANGE'] = {
        'thumbnail_folder': r'.\Thumbnails',
        'thumbnail_size': '300'
    }

    with open(r'.\config.ini', 'w') as f:
        config.write(f)

def changeConfig(categ, param, value):
    parser = configparser.ConfigParser()
    parser.read(r'.\config.ini')
    parser[categ][param] = value
    with open(r'.\config.ini', 'w') as f:
        parser.write(f)

def get_USERconfig(param):
    parser = configparser.ConfigParser()
    parser.read(r'.\config.ini')
    return parser.get('user', param)

def get_DEVconfig(param):
    parser = configparser.ConfigParser()
    parser.read(r'.\config.ini')
    if param == 'thumbnail_size':
        return parser.getint('dev - DONT CHANGE', param)
    else:
        return parser.get('dev - DONT CHANGE', param)

def get_SQLconfig(param):
    parser = configparser.ConfigParser()
    parser.read(r'.\config.ini')
    if param == 'url':
        resp = parser.options('sql')
        return 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
            parser.get('sql', resp[0]),
            parser.get('sql', resp[1]),
            parser.get('sql', resp[2]),
            parser.get('sql', resp[3]),
            parser.get('sql', resp[4])
        )
    else:
        return parser.get('sql', param)


