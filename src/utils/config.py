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
            open(json_file_path.format(json_file[0]), "r")
        except FileNotFoundError as err:
            logger.exception(err)
            logger.log(logger.INFO, "Attempting to correct directory and find config.json")
            logger.log(logger.INFO, os.getcwd())
            os.chdir(default_path)
            open(json_file_path.format(json_file[0]), 'r')

    elif theme == 1:
        try:
            open(json_file_path.format(json_file[1]), "r")
        except FileNotFoundError as err:
            logger.exception(err)
            logger.log(logger.INFO, "Unable to find theme with int 1")
    elif theme == 2:
        try:
            open(json_file_path.format(json_file[2]), "r")
        except FileNotFoundError as err:
            logger.exception(err)
            logger.log(logger.INFO, "Unable to find theme with int 2")
    else:
        print("Error occurred")
    text = open(json_file_path.format(json_file[theme]), "r").read()
    return json.loads(text)


def config_choice(file):
    with open(file, 'r') as index_file:
        config_chosen = int(index_file.read())

        if config_chosen == 0:
            config = config_reader(0)
        elif config_chosen == 1:
            config = config_reader(1)
        elif config_chosen == 2:
            config = config_reader(2)
        else:
            config = config_reader(1)
        return config
