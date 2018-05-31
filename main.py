import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.Window |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.MSWindowsFixedSizeDialogHint

        )
        self.setFixedSize(400, 400)
        self.height = 600
        self.move(0, 0)
        self.width = 600
        self.exit()
        self.new()
        self.open()
        self.saveAs()
        self.save_button()
        self.blank()
        self.initUI()
    def onstart(self):
        with open('untitled.txt', 'a+') as file:
            pass
    def blank(self):
        self.blankAct = QAction('', self)

    def exit(self):
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

    def new(self):
        self.newAct = QAction('New', self)
        self.newAct.setShortcut('Ctrl+N')
        self.newAct.setStatusTip('Create a file')
        self.newAct.triggered.connect(qApp.beep)  # TODO: add a new file creation function

    def open(self):
        self.openAct = QAction('Open...', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open a file')
        self.openAct.triggered.connect(qApp.beep)  # TODO: add a open file function

    def save_button(self):
        self.saveAct = QAction('Save', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save a file')

        def save():
            data = self.textArea.toPlainText()
            with open('untitled.txt', 'w+') as file:
                file.write(data)
                file.close()
                
        self.saveAct.triggered.connect(save)

    def saveAs(self):
        self.saveAsAct = QAction('Save as...', self)
        self.saveAsAct.setShortcut('Shift+Ctrl+S')
        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(qApp.beep)

    def initUI(self):

        self.statusBar()
        menubar = self.menuBar() #Creating a menu bar
        fileMenu = menubar.addMenu('File') #Creating the first menu which will have options listed below
        fileMenu.addAction(self.newAct) #Adding a newact button
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)
        self.textArea = QTextEdit(self)

        self.textArea.move(0, 20)
        self.textArea.resize(400,380)
        self.setWindowTitle('fpad')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(53, 53, 53).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    ex = Example()
    sys.exit(app.exec_())
