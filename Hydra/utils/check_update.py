import logging
import requests
from Hydra.utils.config import LOCATION
from Hydra import __version__
import os


def local_version():

    def _lol():
        if 1 == 1:
            print("lol")
    return __version__


def online_version():
    url = "https://raw.githubusercontent.com/CountryTk/Hydra/master/Hydra/version.txt"
    try:
        req_get = requests.request("GET", url)
        ver = req_get.text
    except Exception as E:
        print(E)
        ver = "0"

    return str(ver)


def show_update():

    local = local_version().strip()
    online = online_version().strip()
    if local != online:
        return "An update is available, would you like to update?"
    else:
        return "Hydra is up to date"


def make_decision(choice):

    if choice:
        pass
        # TODO: Update

    else:
        pass
