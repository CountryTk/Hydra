import json


def read():
    try:
        jsonFile = open("../config.json", "r")
    except FileNotFoundError:
        jsonFile = open("../config.json", "r")

    text = jsonFile.read()
    jsonFile.close()

    return json.loads(text)
