# Test file for new UI

# Copyright (C) 2018 AnonymousDapper & Fuchsiaff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from subprocess import PIPE, Popen

from resources.main_window import Ui_MainWindow

class PyPad(Ui_MainWindow):
    def __init__(self, window, parent=None):
        Ui_MainWindow.__init__(self)

        self.open_files = [] # holds all important information about files
        self.window = window

        self.setupUi(window)

        #self.setAttribute(Qt.WA_DeleteOnClose)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #self.setGeometry(0, 0, 400, 400)

        window.setWindowTitle("pypad (UNREGISTERED)")

        # Action connections
        self.actionOpen.triggered.connect(self.open_file)
        self.actionQuit.triggered.connect(self.exit)
        self.actionNew.triggered.connect(self.new_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrintPreview.triggered.connect(self.preview_print)

        # Edit bindings once we get a working hotkey system

        self.actionFind.triggered.connect(self.find_in_file)
        self.actionReplace.triggered.connect(self.replace_in_file)

        window.show()


    def exit(self):
        self.window.close()
        sys.exit()

    def open_file(self):
        print("Open")

    def new_file(self):
        print("New")

    def save_file(self):
        print("Save")

    def save_file_as(self):
        print("Save As")

    def print_file(self):
        print("Print")

    def preview_print(self):
        print("Print Preview")

    def find_in_file(self):
        print("Find")

    def replace_in_file(self):
        print("Replace")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    pypad = PyPad(window)

    sys.exit(app.exec_())