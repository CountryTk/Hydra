from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCompleter
from utils.predictionList import wordList


class Completer(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, myKeywords=None, parent=None):
        self.wordList = wordList
        QCompleter.__init__(self, myKeywords, parent)

        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):

        self.insertText.emit(completion)
