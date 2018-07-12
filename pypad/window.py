import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QGridLayout, QSplitter


from pypad import config, dialog, directory, menu, tabs


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout(self)
        self.hsplit = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.hsplit)

        self.hsplit.addWidget(directory.directory_tree)
        self.hsplit.addWidget(tabs.tabs)

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
