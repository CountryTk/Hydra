import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTextEdit, QInputDialog, QFileDialog, QDialog
from PyQt5.QtGui import QFont
from PyQt5 import QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import Qt
from subprocess import PIPE, Popen
from pyautogui import hotkey


file_o = None
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
        self.is_opened = False
        self.open()
        self.undo()
        self.printPreview()
        self.printButton()
        self.saveButton()
        self.saveAs()
        self.initUI()


    def exit(self):
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

    def execute(self):
        out, err = Popen(["python fuck.py"], shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return (out + err).decode()

    def new(self):
        self.newAct = QAction('New', self)
        self.newAct.setShortcut('Ctrl+N')
        self.newAct.setStatusTip('Create a file')
        self.newAct.triggered.connect(self.execute)  

    def open(self):
        self.openAct = QAction('Open...', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open a file')
        self.is_opened = False
        def _open():
            global files
            self.is_opened = True
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(
                self, "Open a file", "",
                "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
                options=options
            )
            if files:
                with open(files[0], "r+") as file_o:
                    self.textArea.setText(file_o.read())
        self.openAct.triggered.connect(_open)

    def saveFileAs(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            name = QFileDialog.getSaveFileName(self, 'Save File' , '', "All Files (*);;Python Files (*.py);;Text Files (*.txt)", options=options)
            file_s = open(name[0], 'w+')
            text = self.textArea.toPlainText()
            file_s.write(text)
            file_s.close()
        except:
            pass

    def saveButton(self):
        self.saveAct = QAction('Save', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.save)

    def save(self):
        if self.is_opened is True:
            with open(files[0], "w") as saving:
                saving.write(self.textArea.toPlainText())
        elif self.is_opened is False:
            print("woops")

    def saveAs(self):
        self.saveAsAct = QAction('Save as...', self)
        self.saveAsAct.setShortcut('Shift+Ctrl+S')
        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(self.saveFileAs)

    def printButton(self):
        self.printAct = QAction('Print...', self)
        self.printAct.setShortcut('Ctrl+P')
        self.printAct.setStatusTip('Print a file')

        def test():
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.textArea.document().print_(dialog.printer())
        self.printAct.triggered.connect(test)

    def printPreview(self):
        self.printPrAct = QAction('Print preview', self)
        self.printPrAct.setShortcut('Shift+Ctrl+P')
        self.printPrAct.setStatusTip('See a print preview')
        def test():
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.paintRequested.connect(self.textArea.print_)
            dialog.exec_()
        self.printPrAct.triggered.connect(test)
    def undo(self):
        self.undoAct = QAction('Undo', self)
        self.undoAct.setShortcut('Ctrl+Z')
        self.undoAct.setStatusTip('Undo')
        self.undoAct.triggered.connect(lambda: hotkey('ctrl', 'z'))
    def initUI(self):

        self.statusBar()
        font = QFont()
        font.setPointSize(14)

        menubar = self.menuBar() #Creating a menu bar

        fileMenu = menubar.addMenu('File') #Creating the first menu which will have options listed below
        fileMenu.addAction(self.newAct) #Adding a newact button
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.printPrAct)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        editMenu = menubar.addMenu('Edit') # tired of writing comments
        editMenu.addAction(self.undoAct)
        self.textArea = QTextEdit(self)
        self.textArea.setFont(font)
        self.textArea.move(0, 20)
        self.textArea.resize(400,360)
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
