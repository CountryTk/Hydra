import logging
import requests
from pypad.utils.config import LOCATION


def local_version():

    logger = logging
    logger.basicConfig(filename="pypad.log", filemode='a', level=logger.INFO)

    file = LOCATION + "version.txt"

    try:
        with open(file, "r") as local:
            ver = local.read()
            return str(ver)

    except FileNotFoundError as err:
        logger.exception(err)
        logger.log(logger.INFO, "Unable to find file {}".format(file))
        logger.log(logger.INFO, "Starting the updater...")

        return "0"


def online_version():
    url = 'https://raw.githubusercontent.com/Fuchsiaff/PyPad/master/src/version.txt'
    req_get = requests.request('GET', url)
    ver = req_get.text

    return str(ver)


def show_update():

    local = local_version().strip()
    online = online_version().strip()
    if local != online:
        return "An update is available, would you like to update?"
    else:
        return "PyPad is up to date"


def make_decision(choice):
    
    if choice:
        pass
        # TODO: Update

    else:
        pass
