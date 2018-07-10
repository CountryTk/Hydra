import os
import sys
import uuid

from PyQt5.QtCore import Qt, QRect, QDir
from PyQt5.QtGui import QColor, QPainter, QPalette, QFont, QIcon, QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, \
    QVBoxLayout, QTabWidget, QFileDialog, QPlainTextEdit, QHBoxLayout, QDialog, qApp, QTreeView, QFileSystemModel, QLabel, QGridLayout


from pypad import dialog, numbers


class Editor(QWidget):

    def __init__(self, path: str=''):
        super().__init__()

        self.layout = QGridLayout(self)

        self.editor = QPlainTextEdit()

        self.path = path

        if path:
            self.open_file()
        else:
            self.new_file()

        self.line_numbers = numbers.NumberBar(self.editor)

        self.layout.addWidget(self.line_numbers, 0, 0)
        self.layout.addWidget(self.editor, 0, 1)

    def get_name(self):
        return os.path.basename(self.path)

    def new_file(self):
        temp = '/tmp'
        if sys.platform == 'win32':
            temp = os.getenv('temp') or ''

        if not os.path.exists(temp):
            dialog.FatalError("Couldn't find your config directory")

        path = os.path.join(temp, 'pypad-' + str(uuid.uuid4()).split('-')[0] + '.txt')

        try:
            open(path, 'a').close()
        except PermissionError:
            dialog.FatalError("Couldn't write to", path)

        self.path = path
        self.editor.setPlainText('')

    def open_file(self):
        with open(self.path, 'r') as file:
            text = file.read()
        self.editor.setPlainText(text)

    def save(self):
        pass

    def save_as(self):
        pass
