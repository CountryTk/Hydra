import json
import os, logging

def config_reader(theme):
    logger = logging
    logger.basicConfig(filename="pypad.log", filemode='a', level=logger.INFO)
    json_file = ['config', 'config1', 'config2']
    json_file_path = r"../{}.json"
    default_path = "../"

    if theme == 0:
        try:
            open(json_file_path.format(json_file[0]), 'r')
        except FileNotFoundError as err:
            logger.exception(err)
            logger.info(os.getcwd() + ' Attempting to correct directory and find config.json')
            os.chdir(default_path)
            open(json_file_path.format(json_file[0]), 'r')

    elif theme == 1:
        try:
            open(json_file_path.format(json_file[1]), 'r')
        except FileNotFoundError as err:
            logger.exception(err)
            logger.info('Unable to find theme with int 1')
    elif theme == 2:
        try:
            open(json_file_path.format(json_file[2]), 'r')
        except FileNotFoundError as err:
            logger.exception(err)
            logger.info('Unable to find theme with int 2')
    else:
        print('Error occurred')
    text = open(json_file_path.format(json_file[theme]), 'r').read()
    return json.loads(text)


def config_choice(file):
    with open(file, 'r') as index_file:
        config_chosen = int(index_file.read())
    while config_chosen:
        config = config_reader(config_chosen)
        return config
