import logging
import requests
from pypad.utils.config import LOCATION
from pypad import __version__
import os


def local_version():
    return __version__


def online_version():
    url = "https://raw.githubusercontent.com/CountryTk/PyPad/master/pypad/version.txt"
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
