import sys
import json
import os
from PyQt5.QtCore import Qt, QRect, QRegExp, QDir
from PyQt5.QtGui import QColor, QPainter, QPalette, QSyntaxHighlighter, QFont, QTextCharFormat, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, \
    QVBoxLayout, QTabWidget, QFileDialog, QPlainTextEdit, QHBoxLayout, QDialog, qApp, QTreeView, QFileSystemModel, QLabel

from pyautogui import hotkey


lineBarColor = QColor(53, 53, 53)
lineHighlightColor = QColor('#00FF04')


class NumberBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = parent
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
        width = self.fontMetrics().width(str(string)) + 40
        print("update_width:width:" + str(width))
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


class Search(QWidget):
    pass


class Directory(QTreeView):
    def __init__(self, path):
        super().__init__()

        self.layout = QHBoxLayout()
        model = QFileSystemModel()
        self.setModel(model)

        model.setRootPath(QDir.rootPath())
        self.setRootIndex(model.index(path))

        self.setIndentation(10)
        self.setAnimated(True)

        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")

        self.hideColumn(1)
        self.resize(200, 600)

        self.hideColumn(2)
        self.hideColumn(3)
        self.layout.addWidget(self)
        self.doubleClicked.connect(self.test)
        self.show()
    def test(self, signal):
        file_path = self.model().filePath(signal)
        return file_path


class Content(QWidget):
    def __init__(self, text, fileName):
        super().__init__()
        self.editor = QPlainTextEdit()
        self.text = text
        self.fileName = fileName
        self.editor.setPlainText(text)
        # Create a layout for the line numbers

        self.hbox = QHBoxLayout(self)
        self.numbers = NumberBar(self.editor)
        self.hbox.addWidget(self.numbers)
        self.hbox.addWidget(self.editor)



class Tabs(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()

        # Add tabs
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)   # TODO: make this customizable
        self.tabs.setTabShape(1)  # TODO: make this customizable
        self.tabs.tabCloseRequested.connect(self.closeTab)

        # Add tabs to widget
        #self.layout.addWidget(self.tabs)


    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.onStart()
        # Initializing the main widget where text is displayed
        self.tab = Tabs()

        self.tabsOpen = []

        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))  # Setting the window icon
        self.setWindowTitle('PyPad')  # Setting the window title

        # Initializing the functions to handle certain tasks

        self.new()
        self.open()
        self.save()
        self.saveAs()
        self.exit()
        self.undo()
        self.redo()
        self.cut()
        self.copy()
        self.paste()
        self.all()

        # Without this, the whole layout is broken
        self.setCentralWidget(self.tab)
        self.newFileCount = 0  # Tracking how many new files are opened
        self.files = None  # Tracking the current file that is open
        self.pyFileOpened = False  # Tracking if python file is opened, this is useful to delete highlighting
        self.cFileOpened = False

        self.initUI()  # Main UI
        self.show()

    def onStart(self):
        with open("../config.json", "r") as jsonFile:
            read = jsonFile.read()
            self.data = json.loads(read)

            if self.data["editor"][0]["windowStaysOnTop"] is True:
                self.setWindowFlags(Qt.WindowStaysOnTopHint)

            else:
                pass
            if self.data["editor"][0]["DontUseNativeDialog"] is True:
                self.DontUseNativeDialogs = True

            else:
                self.DontUseNativeDialogs = False
            self.font = QFont()
            self.font.setFamily(self.data["editor"][0]["editorFont"])

            self.font.setPointSize(self.data["editor"][0]["editorFontSize"])
            self.tabSize = self.data["editor"][0]["TabWidth"]
            jsonFile.close()

    def initUI(self):
        self.statusBar()  # Initializing the status bar

        self.font.setFixedPitch(True)

        # Creating the menu bar

        menu = self.menuBar()

        # Creating the file menu

        fileMenu = menu.addMenu('File')

        # Adding options to the file menu

        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        # Creating the edit menu

        editMenu = menu.addMenu('Edit')

        # Adding options to it

        editMenu.addAction(self.undoAct)
        editMenu.addAction(self.redoAct)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAct)
        editMenu.addAction(self.copyAct)
        editMenu.addAction(self.pasteAct)
        editMenu.addSeparator()
        editMenu.addAction(self.allAct)

        self.resize(800, 600)

    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tab.removeTab(index)

    def open(self):
        self.openAct = QAction('Open...', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open a file')
        self.is_opened = False
        self.openAct.triggered.connect(self.openFile)

    def openFile(self):
        if hasattr(self, 'dir'):
            self.tab.layout.removeWidget(self.dir)
        options = QFileDialog.Options()

        filenames, _ = QFileDialog.getOpenFileNames(
            self, 'Open a file', '',
            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
            options=options
        )
        tab_idx = len(self.tabsOpen)

        if filenames:  # If file is selected, we can open it
            filename = filenames[0]
            with open(filename, 'r+') as file_o:
                text = file_o.read()
                tab = Content(text, filename)  # Creating a tab object *IMPORTANT*
                self.is_opened = True
                if filename.endswith(".py"):
                    dirPath = os.path.dirname(filename)
                    self.files = filename

                    self.tabsOpen.append(self.files)
                    self.pyFileOpened = True

                    index = self.tab.tabs.addTab(tab,
                                                 tab.fileName)  # This is the index which we will use to set the current index
                    self.dir = Directory(dirPath)  # # this will spawn the directory

                    self.tab.layout.addWidget(self.dir)  # Adding that directory widget in the Tab class BEFORE the tabs
                    self.tab.layout.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left

                    self.tab.setLayout(self.tab.layout)  # Finally we set the layout

                    self.tab.tabs.setCurrentIndex(index)  # Setting the index so we could find the currentwidget
                    currentTab = self.tab.tabs.currentWidget()

                    currentTab.editor.setFont(self.font)  # Setting the font
                    currentTab.editor.setTabStopWidth(self.tabSize)  # Setting tab size
                    currentTab.editor.setFocus()  # Setting focus to the tab after we open it

                    self.pyhighlighter = pyHighlighter(
                        currentTab.editor.document())  # Creating the highlighter for python
                elif filename.endswith(".c"):

                    self.files = filename
                    dirPath = os.path.dirname(filename) # getting the dir path
                    self.tabsOpen.append(self.files)

                    self.cFileOpened = True
                    self.dir = Directory(dirPath)  # this will spawn the directory

                    self.tab.layout.addWidget(self.dir)  # Adding that directory widget in the Tab class BEFORE the tabs
                    self.tab.layout.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left

                    self.tab.setLayout(self.tab.layout)  # Finally we set the layout
                    index = self.tab.tabs.addTab(tab, tab.fileName)

                    self.tab.tabs.setCurrentIndex(index)
                    currentTab = self.tab.tabs.currentWidget()

                    currentTab.editor.setFont(self.font)
                    currentTab.editor.setTabStopWidth(self.tabSize)

                    currentTab.editor.setFocus()  # Setting focus to the tab after we open it
                    self.chighlighter = cHighlighter(currentTab.editor.document())

                else:
                    if self.pyFileOpened or self.cFileOpened:
                        try:
                            del self.pyhighlighter
                            del self.chighlighter
                        except AttributeError:
                            print("Highlighter already deleted")
                        dirPath = os.path.dirname(filename)  # getting the dir path
                        self.dir = Directory(dirPath)  # this will spawn the directory

                        self.tab.layout.addWidget(self.dir)  # Adding that directory widget in the Tab class BEFORE the tabs
                        self.tab.layout.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left

                        self.tab.setLayout(self.tab.layout)

                        index1 = self.tab.tabs.addTab(tab, tab.fileName)
                        self.tab.tabs.setCurrentIndex(index1)

                        tab = self.tab.tabs.currentWidget()
                        tab.editor.setFont(self.font)

                    else:
                        dirPath = os.path.dirname(filename) # getting the dir path
                        self.dir = Directory(dirPath)  # # this will spawn the directory

                        self.tab.layout.addWidget(self.dir)  # Adding that directory widget in the Tab class BEFORE the tabs
                        self.tab.layout.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left

                        self.tab.setLayout(self.tab.layout)  # Finally we set the layout
                        index2 = self.tab.tabs.addTab(tab, tab.fileName)

                        self.tab.tabs.setCurrentIndex(index2)
                        tab1 = self.tab.tabs.currentWidget()
                        tab1.editor.setFont(self.font)

    def new(self):
        self.newAct = QAction('New')
        self.newAct.setShortcut('Ctrl+N')
        self.newAct.setStatusTip('Create a new file')
        self.newAct.triggered.connect(self.newFile)

    def newFile(self):
        text = ""
        fileName = "Untitled.txt"
        self.is_opened = False

        # Creates a new blank file
        file = Content(text, fileName)

        self.tab.layout.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left

        self.tab.setLayout(self.tab.layout)  # Finally we set the layout
        index = self.tab.tabs.addTab(file, file.fileName)  # addTab method returns an index for the tab that was added
        self.tab.tabs.setCurrentIndex(index)  # Setting "focus" to the new tab that we created

        widget = self.tab.tabs.currentWidget()
        widget.editor.setFocus()
        widget.editor.setFont(self.font)
        widget.editor.setTabStopWidth(self.tabSize)

    def save(self):
        self.saveAct = QAction('Save')
        self.saveAct.setShortcut('Ctrl+S')

        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.saveFile)

    def saveFile(self):
        try:
            active_tab = self.tab.tabs.currentWidget()

            if self.is_opened:  # If a file is already opened
                with open(active_tab.fileName, 'w+') as saveFile:
                    self.saved = True
                    saveFile.write(active_tab.editor.toPlainText())


                    saveFile.close()
            else:
                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    self.saved = True
                    self.is_opened = True

                    self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.toPlainText())

                    saveFile.close()
        except:
            print("File dialog closed or no file opened")

    def saveAs(self):
        self.saveAsAct = QAction('Save As...')
        self.saveAsAct.setShortcut('Ctrl+Shift+S')

        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(self.saveFileAs)

    def saveFileAs(self):
        try:
            active_tab = self.tab.tabs.currentWidget()
            if active_tab is not None:
                active_index = self.tab.tabs.currentIndex()

                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    self.saved = True
                    self.tabsOpen.append(fileName)

                    saveFile.write(active_tab.editor.toPlainText())
                    text = active_tab.editor.toPlainText()
                    newTab = Content(str(text), fileName)

                    self.tab.tabs.removeTab(active_index)  # When user changes the tab name we make sure we delete the old one
                    index = self.tab.tabs.addTab(newTab, newTab.fileName)  # And add the new one!

                    self.tab.tabs.setCurrentIndex(index)
                    newActiveTab = self.tab.tabs.currentWidget()

                    newActiveTab.editor.setFont(self.font)
                    newActiveTab.editor.setFocus()

                    if fileName.endswith(".py"):  # If we are dealing with a python file we use highlighting on it
                        self.pyhighlighter = pyHighlighter(newActiveTab.editor.document())
                        newActiveTab.editor.setTabStopWidth(self.tabSize)
                    elif fileName.endswith(".c"):
                        self.chighlighter = cHighlighter(newActiveTab.editor.document())
                        newActiveTab.editor.setTabStopWidth(self.tabSize)
                    saveFile.close()

            else:
                print("No file opened")
        except FileNotFoundError:
            print("File dialog closed")

    def exit(self):
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')

        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

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


class pyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, *args):
        super(pyHighlighter, self).__init__(parent, *args)
        with open("../config.json", "r") as jsonFile:
            read = jsonFile.read()
            data = json.loads(read)
            jsonFile.close()
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["keywordFormatColor"]))
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

        cKeywordPatterns = ['auto', 'break', 'case', 'char', 'const',
                            'const', 'continue', 'default', 'do',
                            'double', 'else', 'enum', 'extern',
                            'float', 'for', 'goto', 'if',
                            'int', 'long', 'register', 'return',
                            'short', 'signed', 'sizeof', 'static',
                            'struct', 'switch', 'typedef', 'union',
                            'unsigned', 'void', 'volatile', 'while']

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in pyKeywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["classFormatColor"]))
        self.highlightingRules.append((QRegExp('\\bclass\\b'), classFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor(3, 145, 53))
        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["functionFormatColor"]))
        self.highlightingRules.append((QRegExp('[A-Za-z0-9_]+(?=\\()'), functionFormat))

        magicFormat = QTextCharFormat()
        magicFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["magicFormatColor"]))
        self.highlightingRules.append((QRegExp("\__[^\']*\__"), magicFormat))

        decoratorFormat = QTextCharFormat()
        decoratorFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["decoratorFormatColor"]))
        self.highlightingRules.append((QRegExp('@[^\n]*'), decoratorFormat))

        intFormat = QTextCharFormat()
        intFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["intFormatColor"]))
        self.highlightingRules.append((QRegExp("[-+]?[0-9]+"), intFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(107, 110, 108))
        self.highlightingRules.append((QRegExp('#[^\n]*'), singleLineCommentFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["quotationFormatColor"]))
        self.highlightingRules.append((QRegExp("'[^\']*\'"), quotationFormat))
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), quotationFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        comment = QRegExp("'''")

        if self.previousBlockState() == 1:
            start_index = 0
            index_step = 0
        else:
            start_index = comment.indexIn(text)
            index_step = comment.matchedLength()

        while start_index >= 0:
            end = comment.indexIn(text, start_index + index_step)
            if end != -1:
                self.setCurrentBlockState(0)
                length = end - start_index + comment.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index

            self.setFormat(start_index, length, self.multiLineCommentFormat)
            start_index = comment.indexIn(text, start_index + length)


class cHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, *args):
        super(cHighlighter, self).__init__(parent, *args)
        with open("../config.json", "r") as jsonFile:
            read = jsonFile.read()
            data = json.loads(read)
            jsonFile.close()
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["keywordFormatColor"]))
        keywordFormat.setFontWeight(QFont.Bold)

        cKeywordPatterns = ['auto', 'break', 'case', 'char', 'const',
                            'const', 'continue', 'default', 'do',
                            'double', 'else', 'enum', 'extern',
                            'float', 'for', 'goto', 'if',
                            'int', 'long', 'register', 'return',
                            'short', 'signed', 'sizeof', 'static',
                            'struct', 'switch', 'typedef', 'union',
                            'unsigned', 'void', 'volatile', 'while']

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in cKeywordPatterns]

        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["classFormatColor"]))
        self.highlightingRules.append((QRegExp('\\bclass\\b'), classFormat))

        self.multiLineCommentFormat = QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QColor(3, 145, 53))
        functionFormat = QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["functionFormatColor"]))
        self.highlightingRules.append((QRegExp('[A-Za-z0-9_]+(?=\\()'), functionFormat))

        magicFormat = QTextCharFormat()
        magicFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["magicFormatColor"]))
        self.highlightingRules.append((QRegExp("\__[^\']*\__"), magicFormat))

        decoratorFormat = QTextCharFormat()
        decoratorFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["decoratorFormatColor"]))
        self.highlightingRules.append((QRegExp('@[^\n]*'), decoratorFormat))

        intFormat = QTextCharFormat()
        intFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["intFormatColor"]))
        self.highlightingRules.append((QRegExp("[-+]?[0-9]+"), intFormat))

        singleLineCommentFormat = QTextCharFormat()
        singleLineCommentFormat.setForeground(QColor(107, 110, 108))
        self.highlightingRules.append((QRegExp('#[^\n]*'), singleLineCommentFormat))

        quotationFormat = QTextCharFormat()
        quotationFormat.setForeground(QColor(data["syntaxHighlightColors"][0]["quotationFormatColor"]))
        self.highlightingRules.append((QRegExp("'[^\']*\'"), quotationFormat))
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), quotationFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        comment = QRegExp("'''")

        if self.previousBlockState() == 1:
            start_index = 0
            index_step = 0
        else:
            start_index = comment.indexIn(text)
            index_step = comment.matchedLength()

        while start_index >= 0:
            end = comment.indexIn(text, start_index + index_step)
            if end != -1:
                self.setCurrentBlockState(0)
                length = end - start_index + comment.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index

            self.setFormat(start_index, length, self.multiLineCommentFormat)
            start_index = comment.indexIn(text, start_index + length)

if __name__ == '__main__':
    with open("../config.json", "r") as jsonFile:
        read = jsonFile.read()
        data = json.loads(read)
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(data["editor"][0]["windowColor"]))
        palette.setColor(QPalette.WindowText, QColor(data["editor"][0]["windowText"]))
        palette.setColor(QPalette.Base, QColor(data["editor"][0]["editorColor"]))
        palette.setColor(QPalette.AlternateBase, QColor(data["editor"][0]["alternateBase"]))
        palette.setColor(QPalette.ToolTipBase, QColor(data["editor"][0]["ToolTipBase"]))
        palette.setColor(QPalette.ToolTipText, QColor(data["editor"][0]["ToolTipText"]))
        palette.setColor(QPalette.Text, QColor(data["editor"][0]["editorText"]))
        palette.setColor(QPalette.Button, QColor(data["editor"][0]["buttonColor"]))
        palette.setColor(QPalette.ButtonText, QColor(data["editor"][0]["buttonTextColor"]))
        palette.setColor(QPalette.Highlight, QColor(data["editor"][0]["HighlightColor"]).lighter())
        palette.setColor(QPalette.HighlightedText, QColor(data["editor"][0]["HighlightedTextColor"]))
        app.setPalette(palette)

        ex = Main()
        sys.exit(app.exec_())
