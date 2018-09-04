from bs4 import *
import urllib.request


def checkVerOnlineFunc():
    url = urllib.request.urlopen('https://github.com/Fuchsiaff/PyPad/blob/master/src/version.txt').read()

    object = BeautifulSoup(url, 'lxml')
    lol = object.find("td", class_="blob-code blob-code-inner js-file-line")

    return str(lol.text)
