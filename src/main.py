import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTextEdit, QInputDialog, QFileDialog, QDialog, QLineEdit, QPlainTextEdit, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QFontMetrics, QPainter, QTextFormat, QColor
from PyQt5 import QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import Qt, QRegExp, QRect, QSize
from subprocess import PIPE, Popen
from pyautogui import hotkey



file_o = None
lineBarColor = QColor("#5E5E5E")
lineHighlightColor = QColor("#5E5E5E")

class NumberBar(QWidget):
    def __init__(self, parent = None):
        super(NumberBar, self).__init__(parent)
        self.editor = parent
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 10
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), lineBarColor)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()

            painter.end()

class Main(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 400, 400)
        self.editor = QPlainTextEdit()
        self.numbers = NumberBar(self.editor)
        self.move(0, 0)
        self.font = QFont()
        self.font.setFamily('Consolas')
        self.font.setPointSize(14)
        self.exit()
        self.new()
        self.is_opened = False
        self.open()
        self.undo()
        self.cut()
        self.copy()
        self.paste()
        self.all()
        self.printPreview()
        self.redo()
        self.find()
        self.printButton()
        self.saveButton()
        self.saveAs()
        self.initUI()
        self.setWindowTitle('pypad')


    def exit(self):
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

    def execute(self):
        out, err = Popen(["python main.py"], shell=True, stdout=PIPE, stderr=PIPE).communicate()
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
        self.openAct.triggered.connect(self.open1)
    def open1(self):
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
                self.editor.setPlainText(file_o.read())
                if files[0].endswith('.py'):
                    self.highlighter = Highlighter(self.editor.document())
                else:
                    print("no")

    def saveFileAs(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            name = QFileDialog.getSaveFileName(self, 'Save File' , '', "All Files (*);;Python Files (*.py);;Text Files (*.txt)", options=options)
            file_s = open(name[0], 'w+')
            text = self.editor.toPlainText()
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
            with open("Untitled.txt", 'w+') as newfile:
                newfile.write(self.editor.toPlainText())

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
                self.editor.document().print_(dialog.printer())
        self.printAct.triggered.connect(test)

    def printPreview(self):
        self.printPrAct = QAction('Print preview', self)
        self.printPrAct.setShortcut('Shift+Ctrl+P')
        self.printPrAct.setStatusTip('See a print preview')
        def test():
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.paintRequested.connect(self.editor.print_)
            dialog.exec_()
        self.printPrAct.triggered.connect(test)

    def undo(self):
        self.undoAct = QAction('Undo', self)
        self.undoAct.setShortcut('Ctrl+Z')
        self.undoAct.setStatusTip('Undo')
        self.undoAct.triggered.connect(lambda: hotkey('ctrl', 'z'))

    def redo(self):
        self.redoAct = QAction('Redo', self)
        self.redoAct.setShortcut('Shift+Ctrl+Z')
        self.redoAct.setStatusTip('Redo')
        self.redoAct.triggered.connect(lambda: hotkey('shift', 'ctrl', 'z'))

    def cut(self):
        self.cutAct = QAction('Cut', self)
        self.cutAct.setShortcut('Ctrl+X')
        self.cutAct.setStatusTip('Cut')
        self.cutAct.triggered.connect(lambda: hotkey('ctrl', 'x'))

    def copy(self):
        self.copyAct = QAction('Copy', self)
        self.copyAct.setShortcut('Ctrl+C')
        self.copyAct.setStatusTip('Copy')
        self.copyAct.triggered.connect(lambda: hotkey('ctrl', 'c'))

    def paste(self):
        self.pasteAct = QAction('Paste', self)
        self.pasteAct.setShortcut('Ctrl+V')
        self.pasteAct.setStatusTip('Paste')
        self.pasteAct.triggered.connect(lambda: hotkey('ctrl', 'v'))

    def all(self):
        self.allAct = QAction('Select all', self)
        self.allAct.setShortcut('Ctrl+A')
        self.allAct.setStatusTip('Select all')
        self.allAct.triggered.connect(lambda: hotkey('ctrl', 'a'))

    def findWindow(self):
        global files
        text, ok = QInputDialog.getText(self, 'Find', "Find what: ")
        if ok:
            try:
                with open(files[0], 'r') as read:
                    index = read.read().find(text)
                    if index != -1:
                        self.cursors.setPosition(index)
                        self.cursors.movePosition(self.cursors.Right, self.cursors.KeepAnchor, len(text))
                        self.editor.setTextCursor(self.cursors)
                    else:
                        qApp.beep()

            except NameError:
                with open("Untitled.txt", 'a+') as newfile:
                    index = newfile.read().find(text)
                    if index != -1:
                        self.cursors.setPosition(index)
                        self.cursors.movePosition(self.cursors.Right, self.cursors.KeepAnchor, len(text))
                        self.editor.setTextCursor(self.cursors)
                    else:
                        qApp.beep()

    def find(self):
        self.findAct = QAction('Find', self)
        self.findAct.setShortcut('Ctrl+F')
        self.findAct.setStatusTip('Find')
        self.findAct.triggered.connect(self.findWindow)

    def initUI(self):
        self.statusBar()
        font = QFont()
        font.setFamily('Consolas') # TODO: Add your own font in a config file
        font.setFixedPitch(True)
        font.setPointSize(14) # TODO: Add your own font size in a config file
        menubar = self.menuBar() # Creating a menu bar
        fileMenu = menubar.addMenu('File') # Creating the first menu which will have options listed below

        fileMenu.addAction(self.newAct) # Adding a newact button
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.printPrAct)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        editMenu = menubar.addMenu('Edit')
        editMenu.addAction(self.undoAct)
        editMenu.addAction(self.redoAct)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAct)
        editMenu.addAction(self.copyAct)
        editMenu.addAction(self.pasteAct)
        editMenu.addSeparator()
        editMenu.addAction(self.allAct)

        searchMenu = menubar.addMenu('Search')
        searchMenu.addAction(self.findAct)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.numbers)
        layoutH.addWidget(self.editor)
        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH)
        mainWindow = QWidget(self)
        mainWindow.setLayout(layoutV)
        self.editor.setFont(self.font)
        self.setCentralWidget(mainWindow)
        self.cursors = self.editor.textCursor()

        self.show()

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0, 153, 255)) # TODO: Add your own customization to keyword color
        keywordFormat.setFontWeight(QFont.Bold)

        pyKeywordPatterns = ["\\bfor\\b", "\\bclass\\b", "\\brange\\b",
                "\\bFalse\\b", "\\bfinally\\b", "\\bis\\b", "\\breturn\\b",
                "\\bNone\\b", "\\bcontinue\\b", "\\bfor\\b", "\\blambda\\b",
                "\\btry\\b", "\\bTrue\\b", "\\bdef\\b",
                "\\bfrom\\b", "\\bnonlocal\\b", "\\bwhile\\b", "\\band\\b",
                "\\bnot\\b", "\\bglobal\\b", "\\bdel\\b",
                "\\bwith\\b", "\\bas\\b", "\\belif\\b",
                "\\bif\\b", "\\bor\\b", "\\byield\\b", "\\bassert\\b",
                "\\belse\\b", "\\bimport\\b", "\\bpass\\b", "\\bbreak\\b",
                "\\bexcept\\b", "\\bin\\b", "\\braise\\b"]

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in pyKeywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(QColor(255, 135, 48)) # TODO: Add your own customization to keyword color
        self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QtGui.QColor(107, 110, 108))
        self.highlightingRules.append((QRegExp("#[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtGui.QColor(3, 145, 53))

        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QColor(255, 221, 0)) # TODO: Add your own customization to keyword color
        self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"), functionFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(3, 145, 53))
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), quotationFormat))
        self.highlightingRules.append((QRegExp("'[^']*'"), quotationFormat))

        self.commentStartExpression = QRegExp("^'''")
        self.commentEndExpression = QRegExp("'''$")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                           self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                                                             startIndex + commentLength);



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QColor(48, 48, 48))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QColor(48, 48, 48))
    palette.setColor(QtGui.QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QColor(77, 210, 255).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    ex = Main()
    sys.exit(app.exec_())
