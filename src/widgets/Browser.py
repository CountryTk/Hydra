from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QWebEngineView):

    def __init__(self, url):
        super().__init__()
        self.url = QUrl(url)

        self.load(QUrl(url))
        self.show()
