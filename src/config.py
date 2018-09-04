import json


def read(theme):
    if theme == 0:
        try:
            jsonFile = open("../config.json", "r")

        except FileNotFoundError:
            jsonFile = open("../config.json", "r")

    elif theme == 1:
        jsonFile = open("../config1.json", "r")

    elif theme == 2:
        jsonFile = open("../config.json", "r")

    else:
        print("Error occured")

    text = jsonFile.read()

    return json.loads(text)
