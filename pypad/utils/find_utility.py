import os
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


class DocumentSearch(QWidget):
    def __init__(self):
        super().__init__()

        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)

        self.setWindowTitle("Find a document")
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.vbox = QHBoxLayout()
        self.label = QLabel("Enter a file name to search:")

        self.searchButton = QPushButton("Search")
        self.cancelButton = QPushButton("Cancel")
        self.searchResults = QPlainTextEdit()
        self.infoLabel = QLabel("Results will be displayed below")
        self.searchResults.setReadOnly(True)

        self.searchDocumentField = QLineEdit()
        self.searchButton.clicked.connect(self.trigger)
        self.cancelButton.clicked.connect(lambda: self.hide())

        self.searchButton.setAutoDefault(True)

        self.label.setFont(self.font)
        self.infoLabel.setFont(self.font)
        self.searchResults.setFont(self.font)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.searchDocumentField)
        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.searchResults)

        self.vbox.addWidget(self.searchButton)
        self.vbox.addWidget(self.cancelButton)

        self.layout.addLayout(self.vbox)
        self.setLayout(self.layout)

    def trigger(self):
        file = self.searchDocumentField.text()
        self.thread = grabFiles(file)
        self.thread.start()
        self.thread.fileSignal.connect(self.showPath)

    def showPath(self, path):
        self.searchResults.appendPlainText("\n")
        self.searchResults.appendPlainText(path)

    def run(self):
        self.show()


class grabFiles(QThread):
    fileSignal = pyqtSignal(str)

    def __init__(self, file):
        super().__init__()

        self.file = file

    def run(self):
        file = self.file
        operating_sys = sys.platform
        if operating_sys == "win32":
            thing = "\\"
        elif operating_sys == "linux":
            thing = '/'

        for i in os.walk('/'):

            for j in i:
                if file in j or j == file:
                    path = str(i[0] + thing + str(file))
                    self.fileSignal.emit(path)
                # return "Path to file: " + str(i[0]) + thing + str(file)

                else:
                    pass

