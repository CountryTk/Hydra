import json
import os

def config_reader(theme):
    json_file = None
    if theme == 0:
        try:
            json_file = open("../config.json", "r")

        except FileNotFoundError:
            print("aaaa")
            json_file = open("../config.json", "r")
            print(os.getcwd())
            os.chdir("../")
            print(os.getcwd())

    elif theme == 1:
        json_file = open("../config1.json", "r")

    elif theme == 2:
        json_file = open("../config.json", "r")

    else:
        print("Error occurred")

    text = json_file.read()

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
