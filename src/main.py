import sys
from subprocess import PIPE, Popen
import json
from pyautogui import hotkey
from PyQt5 import QtCore, QtGui, QtPrintSupport
from PyQt5.QtCore import QRect, QRegExp, QSize, Qt
from PyQt5.QtGui import (QColor, QFont, QFontMetrics, QPainter,
                         QSyntaxHighlighter, QTextCharFormat, QTextCursor, QFontDatabase,
                         QTextFormat)
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QFileDialog,
                             QHBoxLayout, QInputDialog, QLineEdit, QMainWindow,
                             QMessageBox, QPlainTextEdit, QVBoxLayout, QWidget,
                             qApp)

# debug
import time
import traceback

file_o = None
lineBarColor = QColor(53, 53, 53)
lineHighlightColor = QColor('#00FF04')

# QWidget


class NumberBar(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.editor = parent
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        # # gg64du02
        # self.editor.selectionChanged.connect(self.testselectionChanged)
        # # //selectionChanged ()


        self.update_width('1')


    def mousePressEvent(self, QMouseEvent):
        print("class NumberBar(QWidget):mousePressEvent")


    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 10
        print("update_width:width:"+str(width))
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

            while block.isValid():
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
                painter.drawText(rect, Qt.AlignRight, '%i' % number)

                if block_top > event.rect().bottom():
                    break

                block = block.next()

            painter.end()

# # QWidget.mousePressEvent()
class QWidgetLOL(QWidget):
    # def __init__(self, parent=QWidget):
    #     super().__init__()
    #     print("lolilol1")
    def mousePressEvent(self):
        print("lolilol2")
        # http: // pyqt.sourceforge.net / Docs / PyQt4 / qplaintextedit.html

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.onStart()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.data = None
        self.setGeometry(0, 0, 800, 600)
        # self.editor = QPlainTextEdit()
        self.numbers = NumberBar(self.editor)
        self.move(0, 0)
        self.filename = ''
        self.setWindowIcon(QtGui.QIcon('resources/py.png'))
        self.exit()
        self.new()
        self.run_m()
        self.is_opened = False
        self.saved = False
        self.open()
        self.undo()
        self.cut()
        self.copy()
        self.paste()
        self.indent()
        self.all()
        self.printPreview()
        self.redo()
        self.find()
        self.printButton()
        self.saveButton()
        self.saveAs()
        self.initUI()
        self.setWindowTitle('PyPad')
        self.files = None
        # gg64du02
        self.editor.selectionChanged.connect(self.selectionChanged)
        self.startBlock = 0;
        self.endBlock = 0;
        self.startBlock2 = 0;
        self.endBlock2 = 0;
        # //selectionChanged ()
        self.editor.blockCountChanged.connect(self.blockCountChanged)
        self.editor.copyAvailable.connect(self.copyAvailable)
        self.editor.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.editor.modificationChanged.connect(self.modificationChanged)
        self.editor.redoAvailable.connect(self.redoAvailable)
        self.editor.selectionChanged.connect(self.selectionChanged)
        self.editor.textChanged.connect(self.textChanged)
        self.editor.undoAvailable.connect(self.undoAvailable)

        self.anchor_int = 0

        # self.editor.updateRequest.connect(self.updateRequest)
        # updateRequest

        self.startBlock3 = 0;
        self.endBlock3 = 0;

        self.anchorLineStart = 0
        self.anchorLineEnd   = 0
        self.anchor_int2 = 0
        self.anchorLineStart = 0
        self.anchorLineEnd = 0

        self.startBlock5 = 0
        self.endBlock5   = 0


        # gg64du02
        # self.centralWidget = self.centralWidget()

    # class Qwidget():
    #     def mousePressEvent():
    #         print("tupeupatest")
    # # besion de QWidget
    # def mousePressEvent(self, QMouseEvent):
    #     print("def mousePressEvent(self, QMouseEvent):mousePressEvent")

    def blockCountChanged(self):
        print("blockCountChanged")
    def copyAvailable(self):
        print("copyAvailable")
    def cursorPositionChanged(self):
        print("+++++++++++++++++++++++++++++++++++1")
        print("cursorPositionChanged")
        textCursor_1 = self.editor.textCursor()
        if (textCursor_1.hasSelection() == True):
            print("textCursor_1.hasSelection() == True")
            # textCursor_1.select(QTextCursor.BlockUnderCursor)
            print("textCursor_1.selectionStart():"+str(textCursor_1.selectionStart())+
                  "textCursor_1.selectionEnd():" +str(textCursor_1.selectionEnd()))

        possible_cursor = self.editor.textCursor()
        anchor_int = possible_cursor.anchor()
        print("anchor_int:" + str(anchor_int))

        textBlock = self.editor.toPlainText()
        print("textBlock[anchor_int-1]:" + textBlock[anchor_int-1])

        # # ======================

        # strAnchor1 = ""
        # strAnchor2 = ""
        #
        # try:
        #     strAnchor1 = textBlock[anchor_int]
        #     print("strAnchor1:"+str(strAnchor1))
        # except:
        #     print("except:cursorPositionChanged1")
        #     print(sys.exc_info())
        #     try:
        #         strAnchor2 = textBlock[anchor_int-1]
        #         print("strAnchor2:" + str(strAnchor2))
        #     except:
        #         print("except:cursorPositionChanged2")
        #         print(sys.exc_info())
        #         pass
        #     pass
        #
        # strAnchor = ""
        # if(strAnchor1 != ""):
        #     anchor_int =anchor_int
        # if(strAnchor2 != ""):
        #     anchor_int = anchor_int -1
        #
        # # strAnchor is a int
        # print("anchor_int:"+str(anchor_int))
        #
        # if(self.anchor_int2!=anchor_int):
        #     # possible_cursor.select(QTextCursor.BlockUnderCursor)
        #     self.anchorLineStart = possible_cursor.selectionStart()
        #     self.anchorLineEnd   = possible_cursor.selectionEnd()
        #
        # print("self.anchorLineStart:"+str(self.anchorLineStart))
        # print("self.anchorLineEnd:"+str(self.anchorLineEnd))
        #
        # print("textBlock[self.anchorLineStart:self.anchorLineEnd]:"+"\n"
        #       +textBlock[self.anchorLineStart:self.anchorLineEnd])
        #
        #
        # print("possible_cursor.select(QTextCursor.BlockUnderCursor)")
        # possible_cursor.select(QTextCursor.BlockUnderCursor)
        # # test downward
        # print("# test downward")
        # if(self.anchorLineEnd<possible_cursor.selectionEnd()):
        #     print("if(self.anchorLineEnd<possible_cursor.selectionEnd()):")
        #     print("textBlock[self.anchorLineStart:possible_cursor.selectionEnd()]:"+"\n"
        #         +textBlock[self.anchorLineStart:possible_cursor.selectionEnd()])
        #     # print("\n"
        #     #     +textBlock[self.anchorLineStart:possible_cursor.selectionEnd()])
        #     pass
        # # test   upward
        # print("# test   upward")
        # if(self.anchorLineStart>possible_cursor.selectionStart()):
        #     print("if(self.anchorLineStart>possible_cursor.selectionStart()):")
        #     print("textBlock[possible_cursor.selectionStart():self.anchorLineEnd]:"+"\n"
        #         +textBlock[possible_cursor.selectionStart():self.anchorLineEnd])
        #     pass

        # # ==================================

        try:
            print("textBlock[anchor_int]:" + textBlock[anchor_int])

            if(self.anchor_int2!=anchor_int):
                # possible_cursor.select(QTextCursor.BlockUnderCursor)
                self.anchorLineStart = possible_cursor.selectionStart()
                self.anchorLineEnd   = possible_cursor.selectionEnd()

            print("self.anchorLineStart:"+str(self.anchorLineStart))
            print("self.anchorLineEnd:"+str(self.anchorLineEnd))

            print("textBlock[self.anchorLineStart:self.anchorLineEnd]:"+"\n"
                  +textBlock[self.anchorLineStart:self.anchorLineEnd])


            print("possible_cursor.select(QTextCursor.BlockUnderCursor)")
            possible_cursor.select(QTextCursor.BlockUnderCursor)

            # # test downward
            # # print("# test downward")
            # if(self.anchorLineEnd<possible_cursor.selectionEnd()):
            #     print("if(self.anchorLineEnd<possible_cursor.selectionEnd()):")
            #     # print("textBlock[self.anchorLineStart:possible_cursor.selectionEnd()]:"+"\n"
            #     #     +textBlock[self.anchorLineStart:possible_cursor.selectionEnd()])
            #     pass
            #
            # # test   upward
            # # print("# test   upward")
            # if(self.anchorLineStart>possible_cursor.selectionStart()):
            #     print("if(self.anchorLineStart>possible_cursor.selectionStart()):")
            #     # print("textBlock[possible_cursor.selectionStart():self.anchorLineEnd]:"+"\n"
            #     #     +textBlock[possible_cursor.selectionStart():self.anchorLineEnd])
            #     pass



            # test downward
            # print("# test downward")
            if(self.anchorLineEnd<possible_cursor.selectionEnd()):
                print("if(self.anchorLineEnd<possible_cursor.selectionEnd()):")

                i = 0
                anchor_intI = anchor_int - i
                while (textBlock[anchor_intI] != "\n"):
                    # print("while")
                    # print("textBlock[anchor_intI]:" + textBlock[anchor_intI])
                    anchor_intI = anchor_intI - 1
                    # print("anchor_int:" + str(anchor_intI))
                    pass

                # print("textBlock[anchor_intI]:" + textBlock[anchor_intI])

                print("textBlock[self.anchorLineStart:possible_cursor.selectionEnd()]:"
                    +textBlock[anchor_intI:possible_cursor.selectionEnd()])

                self.startBlock5 = anchor_intI
                self.endBlock5 = possible_cursor.selectionEnd()
                pass
            # test   upward
            # print("# test   upward")
            if(self.anchorLineStart>possible_cursor.selectionStart()):
                print("if(self.anchorLineStart>possible_cursor.selectionStart()):")

                i = 0
                anchor_intI = anchor_int + i
                while (textBlock[anchor_intI] != "\n"):
                    # print("while")
                    # print("textBlock[anchor_intI]:" + textBlock[anchor_intI])
                    anchor_intI = anchor_intI + 1
                    # print("anchor_int:" + str(anchor_intI))
                    pass

                # print("textBlock[anchor_intI]:" + textBlock[anchor_intI])

                print("textBlock[possible_cursor.selectionStart():self.anchorLineEnd]:"
                    +textBlock[possible_cursor.selectionStart():anchor_intI])

                self.startBlock5 = possible_cursor.selectionStart()
                self.endBlock5 = anchor_intI
                pass

            print("textBlock[self.startBlock5:self.endBlock5]:"+
                  textBlock[self.startBlock5:self.endBlock5])
        except:
            traceback.print_stack
            pass


        # # ==============================




        print("+++++++++++++++++++++++++++++++++++2")
    def modificationChanged(self):
        print("modificationChanged")

    def redoAvailable(self):
        print("redoAvailable")

    def selectionChanged(self):
        # print("======================================")
        # print('selectionChanged ')
        # print("======================================")
        pass
    def textChanged(self):
        print('textChanged ')
    def undoAvailable(self):
        print("undoAvailable")
    # def updateRequest(self):
    #     print("updateRequest")





    def onStart(self):
        with open("../config.json", "r") as jsonFile:
            read = jsonFile.read()
            self.data = json.loads(read)
            if self.data["editor"][0]["windowStaysOnTop"] is True:
                self.setWindowFlags(Qt.WindowStaysOnTopHint)
            else:
                pass
            self.font = QFont()
            self.font.setFamily(self.data["editor"][0]["editorFont"])
            self.font.setPointSize(self.data["editor"][0]["editorFontSize"])
            jsonFile.close()

            self.editor = QPlainTextEdit()
            self.editor.setTabStopWidth(self.data["editor"][0]["TabWidth"])
            self.editor.setPlainText('''
#############################
|                           |
|      No files open        |
|Press Ctrl+O to open a file|
|      Ctrl+Q to quit       |
|                           |
#############################
            ''')

    def exit(self):
        # I want to know when this is defined
        # print("def exit(self):")
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

    @staticmethod
    def execute(self):
        out, err = Popen(['python main.py'], shell=True, stdout=PIPE, stderr=PIPE).communicate()
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
        self.is_opened = True
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.files, _ = QFileDialog.getOpenFileNames(
            self, 'Open a file', '',
            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
            options=options
        )

        if self.files:
            with open(self.files[0], 'r+') as file_o:

                self.filename = file_o, self.editor.setPlainText(file_o.read())

                if self.files[0].endswith('.py'):
                    self.highlighter = Highlighter(self.editor.document())
                    self.setWindowTitle("PyPad [" + self.files[0] + "]")
                else:
                    print('Non-Python file opened. Highlighting will not be used.')
                    self.setWindowTitle("PyPad [" + self.files[0] + "]")

    def saveFileAs(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                               'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                               options=options)
            file_s = open(name[0], 'w+')
            self.filename = file_s
            text = self.editor.toPlainText()
            # what is the content of text
            # print("saveFileAs:text:"+text)
            file_s.write(text)
            file_s.close()
        except:
            pass



    def indenting(self):
        print("indenting:start")
        textBlock = self.editor.toPlainText()

        try:
            # self.startBlock5
            # self.endBlock5

            tmpStr =  self.editor.toPlainText()
            tmpStr2 = textBlock[self.startBlock5:self.endBlock5]
            print("tmpStr2:"+tmpStr2)
            tmpStr3 = tmpStr2.replace("\n", "\n    ")
            print("tmpStr3:"+tmpStr3)

            tmpStrStart = tmpStr[0:self.startBlock5]
            tmpStrEnd = tmpStr[self.endBlock5:len(tmpStr)]

            print("tmpStrStart:"+tmpStrStart)
            print("tmpStrEnd:"+tmpStrEnd)

            textCursor_1 = self.editor.textCursor()
            if (textCursor_1.hasSelection() == True):
                # textCursor_1.select(QTextCursor.BlockUnderCursor)
                self.editor.setPlainText(tmpStrStart+tmpStr3+tmpStrEnd)
                # textCursor_1.beginEditBlock()
                # textCursor_1.insertText(tmpStr3+"")
                # textCursor_1.endEditBlock()
        except:
            print("except:indenting")
            print(sys.exc_info())
            pass

        print("indenting:end")


    def saveButton(self):
        self.saveAct = QAction('Save', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.save)

    def save(self):
        if self.is_opened:
            with open(self.files[0], 'w+') as saving:
                self.filename = saving
                self.saved = True
                saving.write(self.editor.toPlainText())
        else:
            print("No file open!")

    def saveAs(self):
        self.saveAsAct = QAction('Save as...', self)
        self.saveAsAct.setShortcut('Shift+Ctrl+S')
        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(self.saveFileAs)

    def printButton(self):
        self.printAct = QAction('Print...', self)
        self.printAct.setShortcut('Ctrl+P')
        self.printAct.setStatusTip('Print a file')
        def _action():
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QDialog.Accepted:
                self.textArea.document().print_(dialog.printer())
        self.printAct.triggered.connect(_action)

    def printPreview(self):
        self.printPrAct = QAction('Print preview', self)
        self.printPrAct.setShortcut('Shift+Ctrl+P')
        self.printPrAct.setStatusTip('See a print preview')
        def _action():
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.paintRequested.connect(self.textArea.print_)
            dialog.exec_()

        self.printPrAct.triggered.connect(_action)

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

    def run(self):
        if self.files is None or self.files[0].endswith(".py") is False:
            print("Can't run a non python file or a file that doesn't exist...")
        else:
            Popen(['python ' + self.files[0]], shell=True, stdout=PIPE, stderr=PIPE).communicate()

    def run_m(self):
        self.runAct = QAction('Run', self)
        self.runAct.setShortcut('Ctrl+R')
        self.runAct.setStatusTip('Run your program')
        self.runAct.triggered.connect(self.run)

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

    def indent(self):
        self.indentAct = QAction('Indent selected line', self)
        self.indentAct.setShortcut('Ctrl+I')
        self.indentAct.setStatusTip('Indent selected line')
        # ok
        self.indentAct.triggered.connect(self.indenting)

    def findWindow(self):
        text, ok = QInputDialog.getText(self, 'Find', 'Find what: ')
        if not ok:
            return False

        try:
            with open(self.files[0], 'r') as read:
                index = read.read().find(text)
                if index != -1:
                    self.cursors.setPosition(index)
                    self.cursors.movePosition(self.cursors.Right, self.cursors.KeepAnchor, len(text))
                    self.editor.setTextCursor(self.cursors)
                else:
                    qApp.beep()

        except:
            print("No file opened")

    def find(self):
        self.findAct = QAction('Find', self)
        self.findAct.setShortcut('Ctrl+F')
        self.findAct.setStatusTip('Find')
        self.findAct.triggered.connect(self.findWindow)

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

    def isModified(self):
        return self.editor.document().isModified()

    def maybeSave(self):
        if not self.isModified():
            return True
        if self.saved is False:
            ret = QMessageBox.question(self, 'Message',
                                       '<h4><p>The document was modified.</p>\n' \
                                       '<p>Do you want to save changes?</p></h4>',
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                if self.filename == '':
                    self.saveFileAs()
                    return False
                else:
                    self.save()
                    return True

            if ret == QMessageBox.Cancel:
                return False

            return True
        else:
            return True
    def initUI(self):
        self.statusBar()
        self.font.setFixedPitch(True)

        menubar = self.menuBar()  # Creating a menu bar
        fileMenu = menubar.addMenu('File')  # Creating the first menu which will have options listed below

        fileMenu.addAction(self.newAct)  # Adding a newact button
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
        editMenu.addAction(self.indentAct)
        editMenu.addSeparator()
        editMenu.addAction(self.allAct)

        searchMenu = menubar.addMenu('Search')
        searchMenu.addAction(self.findAct)
        runMenu = menubar.addMenu('Run')
        runMenu.addAction(self.runAct)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.numbers)
        layoutH.addWidget(self.editor)
        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH)

        # class QWidget

        mainWindow = QWidget(self)

        # gg64du02
        # mainWindow = QWidgetLOL(self)

        mainWindow.setLayout(layoutV)
        self.editor.setFont(self.font)
        self.setCentralWidget(mainWindow)
        self.installEventFilter(self)
        self.editor.setFocus()
        self.cursor = QTextCursor()
        self.editor.moveCursor(self.cursor.End)
        self.cursors = self.editor.textCursor()

        self.show()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        with open("../config.json", "r") as jsonFile:
            read = jsonFile.read()
            data = json.loads(read)
            jsonFile.close()
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["keywordFormatColor"]))  # TODO: Add your own customization to keyword color
        keywordFormat.setFontWeight(QFont.Bold)

        pyKeywordPatterns = ['for', 'class', 'range',
                             'False', 'finally', 'is',
                             'return', 'None', 'continue',
                             'for', 'lambda', 'try',
                             'True', 'def', 'from',
                             'nonlocal', 'while', 'and',
                             'not', 'global', 'del',
                             'with', 'as', 'elif',
                             'if', 'or', 'yield',
                             'assert', 'else', 'import',
                             'pass', 'break', 'except',
                             'in', 'raise', 'self',
                             'async']

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in pyKeywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["classFormatColor"]))  # TODO: Add your own customization to keyword color
        self.highlightingRules.append((QRegExp('class [A-Za-z]+'), classFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QtGui.QColor(107, 110, 108))
        self.highlightingRules.append((QRegExp('#[^\n]*'), singleLineCommentFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtGui.QColor(3, 145, 53))
        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["functionFormatColor"]))  # TODO: Add your own customization to keyword color
        self.highlightingRules.append((QRegExp('[A-Za-z0-9_]+(?=\\()'), functionFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["quotationFormatColor"])) # TODO: Add your own customization color
        self.highlightingRules.append((QRegExp("\'[^\']*\'"), quotationFormat))
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
                                                             startIndex + commentLength)

if __name__ == '__main__':
    with open("../config.json", "r") as jsonFile:
        read = jsonFile.read()
        data = json.loads(read)
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QColor(data["editor"][0]["windowColor"]))
        palette.setColor(QtGui.QPalette.WindowText, QColor(data["editor"][0]["windowText"]))
        palette.setColor(QtGui.QPalette.Base, QColor(data["editor"][0]["editorColor"]))
        palette.setColor(QtGui.QPalette.AlternateBase, QColor(data["editor"][0]["alternateBase"]))
        palette.setColor(QtGui.QPalette.ToolTipBase, QColor(data["editor"][0]["ToolTipBase"]))
        palette.setColor(QtGui.QPalette.ToolTipText, QColor(data["editor"][0]["ToolTipText"]))
        palette.setColor(QtGui.QPalette.Text, QColor(data["editor"][0]["editorText"]))
        palette.setColor(QtGui.QPalette.Button, QColor(data["editor"][0]["buttonColor"]))
        palette.setColor(QtGui.QPalette.ButtonText, QColor(data["editor"][0]["buttonTextColor"]))
        palette.setColor(QtGui.QPalette.Highlight, QColor(data["editor"][0]["HighlightColor"]).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, QColor(data["editor"][0]["HighlightedTextColor"]))
        app.setPalette(palette)
        ex = Main()
        sys.exit(app.exec_())
        jsonFile.close()
