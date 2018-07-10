from PyQt5.QtCore import Qt, QRect, QDir
from PyQt5.QtGui import QColor, QPainter, QPalette, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, \
    QVBoxLayout, QTabWidget, QFileDialog, QPlainTextEdit, QHBoxLayout, QDialog, qApp, QTreeView, QFileSystemModel, QLabel


from pypad import window, editor


class Tabs(QTabWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.change_tab)

    def close_tab(self, index):
        tab = self.widget(index)
        tab.save()
        tab.deleteLater()
        self.removeTab(index)

    def get_current(self):
        return self.widget(self.currentIndex())

    def change_tab(self, index):
        name = self.widget(index).get_name()
        window.main_window.set_filename(name)

    def new_tab(self, path: str=''):
        tab = editor.Editor(path)
        self.addTab(tab, tab.get_name())


tabs = Tabs()
