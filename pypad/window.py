import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout


from pypad import config, dialog, directory, menu, tabs, settings


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)

        self.layout.addWidget(directory.directory_tree, 0, 0, 2, 1)
        self.layout.addWidget(tabs.tabs, 0, 1, 2, 1)

        tabs.tabs.new_tab()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.statusBar()

        self.setWindowTitle('PyPad')
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resources/Python-logo-notext.png')))

        self.resize(*config.config.get('window.size'))

    def set_filename(self, name):
        self.setWindowTitle('Pypad - ' + name)

    def closeEvent(self, event):
        event.ignore()
        dialog.Quit()

    def show(self):
        menu.Menu()
        main_window.setCentralWidget(main_widget)
        super().show()


main_window = MainWindow()
main_widget = MainWidget()
