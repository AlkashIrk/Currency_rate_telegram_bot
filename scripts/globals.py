import scripts.config_data
import os

token = ''
telegram_token = ''
base_name = ''
base_folder_path = ''
settings = {}


def init():
    global base_folder_path
    global base_name
    global settings
    global token
    global telegram_token

    config = scripts.config_data.config_read()

    try:
        telegram_token = config['telegram_token']
    except:
        telegram_token = None

    base_folder_path = config['base_folder']
    base_name = base_folder_path + config['base_main']

    if telegram_token == 'your_telegram_token' or telegram_token is None:
        config_path = os.getcwd() + '\\cfg\\config.ini'
        print('Enter your TELEGRAM token to config:\n\t%s' % config_path)
        exit()
