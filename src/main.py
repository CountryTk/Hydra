import sys
import os
import keyword
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QPalette, QSyntaxHighlighter, QFont, QTextCharFormat, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, qApp, QStatusBar
import platform
import random
from widgets.Customize import Customize
from widgets.Messagebox import MessageBox
from utils.config import config_reader
from widgets.Tabs import Tabs
from widgets.Content import Content
from widgets.Image import Image
from utils.find_all_files import DocumentSearch

config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())

lineBarColor = QColor(53, 53, 53)

os.environ["PYTHONUNBUFFERED"] = "1"


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.onStart(choiceIndex)
        self.status = QStatusBar(self)
        self.custom = Customize()
        # Initializing the main widget where text is displayed
        self.tab = Tabs(self.openFile, app, palette)
        self.tabsOpen = []
        self.pic_opened = False

        if file is not None:
            self.openFile(file)
            self.fileNameChange()

        self.dialog = MessageBox()

        self.pyConsoleOpened = None
        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))  # Setting the window icon

        self.setWindowTitle('PyPad')  # Setting the window title
        self.tab.tabs.currentChanged.connect(self.fileNameChange)
        self.search = DocumentSearch()
        self.os = sys.platform
        self.openpy()
        self.openterm()
        self.openterminal()
        self.new()
        self.newProject()
        self.findDocument()
        self.openProjectF()
        self.open()
        self.save()
        self.saveAs()
        self.customize()
        self.exit()
        
        self.dir_opened = False
        self._dir = None

        # Without this, the whole layout is broken
        self.setCentralWidget(self.tab)
        self.newFileCount = 0  # Tracking how many new files are opened

        self.files = None  # Tracking the current file that is open
        self.pyFileOpened = False  # Tracking if python file is opened, this is useful to delete highlighting

        self.cFileOpened = False
        self.initUI()  # Main UI

    def fileNameChange(self):
        try:
            currentFileName = self.tab.tabs.currentWidget().baseName
            self.setWindowTitle("PyPad ~ " + str(currentFileName))

        except AttributeError:
            self.setWindowTitle("PyPad ~ ")

    def onStart(self, index):

        if index == 0:
            editor = config0['editor']

        elif index == 1:
            editor = config1['editor']

        elif index == 2:
            editor = config2['editor']

        else:
            editor = config0['editor']

        if editor["windowStaysOnTop"] is True:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)

        else:
            pass

        self.font = QFont()
        self.font.setFamily(editor["editorFont"])

        self.font.setPointSize(editor["editorFontSize"])
        self.tabSize = editor["TabWidth"]

    def initUI(self):

        self.setStatusBar(self.status)  # Initializing the status bar

        self.font.setFixedPitch(True)
        menuFont = QFont()
        menuFont.setFamily(editor["menuFont"])
        menuFont.setPointSize(editor['menuFontSize'])
        menu = self.menuBar()
        menu.setFont(menuFont)
        # Creating the file menu

        fileMenu = menu.addMenu('File')

        # Adding options to the file menu
        # self.setStatusBar(self.status)
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.newProjectAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.openProjectAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.saveAsAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        toolMenu = menu.addMenu('Tools')
        toolMenu.addAction(self.openPyAct)
        toolMenu.addAction(self.openTermAct)
        toolMenu.addAction(self.openTerminalAct)

        appearance = menu.addMenu('Appearance')

        appearance.addAction(self.colorSchemeAct)
        
        searchDoc = menu.addMenu('Find document')
        
        searchDoc.addAction(self.findDocumentAct)

        self.showMaximized()

    def open(self):
        self.openAct = QAction('Open...', self)
        self.openAct.setShortcut('Ctrl+O')

        self.openAct.setStatusTip('Open a file')
        self.openAct.triggered.connect(self.openFileFromMenu)

    def new(self):
        self.newAct = QAction('New')
        self.newAct.setShortcut('Ctrl+N')

        self.newAct.setStatusTip('Create a new file')
        self.newAct.triggered.connect(self.newFile)
        
    def newProject(self):
        self.newProjectAct = QAction('New project')
        self.newProjectAct.setShortcut('Ctrl+Shift+N')
        
        self.newProjectAct.setStatusTip('Create a new project')
        self.newProjectAct.triggered.connect(self.newProjectFolder)
            
    def openProjectF(self):
        self.openProjectAct = QAction('Open project')
        self.openProjectAct.setShortcut('Ctrl+Shift+O')
        
        self.openProjectAct.setStatusTip('Open a project')
        self.openProjectAct.triggered.connect(self.openProject)    

    def customize(self):
        self.colorSchemeAct = QAction('Customize', self)
        self.colorSchemeAct.setShortcut('Alt+C')

        self.colorSchemeAct.setStatusTip('Select a color scheme')
        self.colorSchemeAct.triggered.connect(self.theme)

    def theme(self):
        self.custom.run()
        self.custom.selector.clicked.connect(self.custom.test)

    def save(self):
        self.saveAct = QAction('Save')
        self.saveAct.setShortcut('Ctrl+S')

        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.saveFile)
        
    def openpy(self):
        self.openPyAct = QAction('IPython console', self)
        self.openPyAct.setShortcut('Ctrl+Y')

        self.openPyAct.setStatusTip('Open IPython console')
        self.openPyAct.triggered.connect(self.console)

    def openterm(self):
        self.openTermAct = QAction('Run', self)
        self.openTermAct.setShortcut('Shift+F10')

        self.openTermAct.setStatusTip('Run your code')
        self.openTermAct.triggered.connect(self.terminal)

    def openterminal(self):
        self.openTerminalAct = QAction("Terminal", self)
        self.openTerminalAct.setShortcut("Ctrl+T")

        self.openTerminalAct.setStatusTip("Open a terminal")
        self.openTerminalAct.triggered.connect(self.realterminal)

    def saveAs(self):
        self.saveAsAct = QAction('Save As...')
        self.saveAsAct.setShortcut('Ctrl+Shift+S')

        self.saveAsAct.setStatusTip('Save a file as')
        self.saveAsAct.triggered.connect(self.saveFileAs)
        
    def findDocument(self):
        self.findDocumentAct = QAction('Find document')
        self.findDocumentAct.setShortcut('Ctrl+Shift+F')
        
        self.findDocumentAct.setStatusTip('Find a document')
        self.findDocumentAct.triggered.connect(self.findDocumentFunc)
    
    def findDocumentFunc(self):
        
        self.search.run()    
        
    def exit(self):
        self.exitAct = QAction('Quit', self)
        self.exitAct.setShortcut('Ctrl+Q')

        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(qApp.quit)

    def openFileFromMenu(self):
        options = QFileDialog.Options()

        filenames, _ = QFileDialog.getOpenFileNames(
            self, 'Open a file', '',
            'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
            options=options
        )

        if filenames:  # If file is selected, we can open it
            filename = filenames[0]
            if filename[-3:] in ['gif', 'png', 'jpg', 'bmp'] or filename[-4:] in ['jpeg']:
                self.pic_opened = True
            self.openFile(filename)

    def openFile(self, filename):
       
        try:
            for index, tabName in enumerate(self.tab.tabCounter):
                with open(filename, 'r+') as file_o:
                    if filename[-3:] in ['gif', 'png', 'jpg', 'bmp'] or filename[-4:] in ['jpeg']:
                        self.pic_opened = True
                    else:
                        self.pic_opened = False
                    try:
                        text = file_o.read()
                        
                    except UnicodeDecodeError as E:
                        text = str(E)

                    basename = os.path.basename(filename)
                    if not self.pic_opened:
                        tab = Content(text, filename, basename, self.custom.index, self, ex)
                        tab.saved = True
                        tab.modified = False
                    else:
                        tab = Image(filename, basename)
                if tabName == tab.baseName:
                    self.tab.tabs.removeTab(index)

                    self.tab.tabCounter.remove(tab.baseName)
            try:
                with open(filename, 'r+') as file_o:
                    try:
                        if self.pic_opened is not True:
                            text = file_o.read()
                        else:
                            text = None
                    except (FileNotFoundError, UnicodeDecodeError, AttributeError) as E:
                        text = str(E)

            except FileNotFoundError:
                with open(filename, 'w+') as newFileCreated:
                    text = newFileCreated.read()
            basename = os.path.basename(filename)
            if self.pic_opened is True:
                tab = Image(filename, basename)
                
            else:
                tab = Content(text, filename, basename, self.custom.index, self, ex)  # Creating a tab object *IMPORTANT*
                tab.saved = True
                tab.modified = False
            self.tab.tabCounter.append(tab.baseName)
            dirPath = os.path.dirname(filename)
            self.files = filename
            
            self.tabsOpen.append(self.files)

            index = self.tab.tabs.addTab(tab,
                                         tab.fileName)  # This is the index which we will use to set the current
            if not self.dir_opened:  # If a project isnt opened then we open a directory everytime we open a file
                self.tab.directory.openDirectory(dirPath)

                self.tab.showDirectory()
            else:
                pass

            self.tab.setLayout(self.tab.layout)  # Finally we set the layout

            self.tab.tabs.setCurrentIndex(index)  # Setting the index so we could find the current widget

            self.currentTab = self.tab.tabs.currentWidget()
            
            if self.pic_opened is not True:
                self.currentTab.editor.setFont(self.font)  # Setting the font
                self.currentTab.editor.setTabStopWidth(self.tabSize)  # Setting tab size
                self.currentTab.editor.setFocus()  # Setting focus to the tab after we open it

            self.pic_opened = False
        except (IsADirectoryError, AttributeError, UnboundLocalError, PermissionError) as E:
            print(E)

    def newFile(self):
        text = ""
        
        if self._dir:
            fileName = str(self._dir) + "/" + "Untitled_file_" + str(random.randint(1, 100)) + ".py"
        else:
            current = os.getcwd()
            fileName = current + "/" + "Untitled_file_" + str(random.randint(1,100)) + ".py"
            
        self.pyFileOpened = True
        # Creates a new blank file
        file = Content(text, fileName, fileName, self.custom.index, self, ex)

        self.tab.splitterH.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left
        self.tab.tabCounter.append(file.fileName)
        self.tab.setLayout(self.tab.layout)  # Finally we set the layout
        index = self.tab.tabs.addTab(file, file.fileName)  # addTab method returns an index for the tab that was added
        self.tab.tabs.setCurrentIndex(index)  # Setting focus to the new tab that we created
        widget = self.tab.tabs.currentWidget()

        widget.editor.setFocus()
        widget.editor.setFont(self.font)
        widget.editor.setTabStopWidth(self.tabSize)
        
    def newProjectFolder(self):
        self.dialog = MessageBox()
        self.dialog.newProject()
        
    def openProject(self):
        
        self._dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', '', QFileDialog.ShowDirsOnly)
        
        self.tab.directory.openDirectory(self._dir)
        self.dir_opened = True
        self.tab.showDirectory()
        
    def saveFile(self):
        try:
            active_tab = self.tab.tabs.currentWidget()
            if self.tab.tabs.count():  # If a file is already opened
                with open(active_tab.fileName, 'w+') as saveFile:
                    saveFile.write(active_tab.editor.toPlainText())
                    active_tab.saved = True
                    
                    active_tab.modified = False
                    saveFile.close()
                active_tab.tokenize_file()
            else:
                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(self, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    active_tab.saved = True
                    active_tab.modified = False
                    self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.toPlainText())
                    saveFile.close()
            ex.setWindowTitle("PyPad ~ " + str(active_tab.baseName) + " [SAVED]")
            active_tab.tokenize_file()
        except Exception as E:
            print(E)
        
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
                    active_tab.saved = True
                    active_tab.modified = False
                    self.tabsOpen.append(fileName)

                    try:
                        baseName = os.path.basename(fileName)
                    except AttributeError:
                        print("All tabs closed")
                    saveFile.write(active_tab.editor.toPlainText())
                    text = active_tab.editor.toPlainText()
                    newTab = Content(str(text), fileName, baseName, self.custom.index, self, ex)

                    self.tab.tabs.removeTab(active_index)  # When user changes the tab name we make sure we delete the old one
                    index = self.tab.tabs.addTab(newTab, newTab.fileName)  # And add the new one!

                    self.tab.tabs.setCurrentIndex(index)
                    newActiveTab = self.tab.tabs.currentWidget()

                    newActiveTab.editor.setFont(self.font)
                    newActiveTab.editor.setFocus()

                    if fileName.endswith(".py"):  # If we are dealing with a python file we use highlighting on it
                        self.pyhighlighter = PyHighlighter(newActiveTab.editor.document(), index=self.custom.index)

                        newActiveTab.editor.setTabStopWidth(self.tabSize)

                    saveFile.close()
                ex.setWindowTitle("PyPad ~ " + str(active_tab.baseName) + " [SAVED]")

            else:
                print("No file opened")

        except FileNotFoundError:
            print("File dialog closed")

    def console(self):

        self.pyConsoleOpened = True
        self.ind = self.tab.splitterV.indexOf(self.tab.term)

        self.o = self.tab.splitterV.indexOf(self.tab.Console)

        if self.tab.splitterV.indexOf(self.tab.Console) == -1:  # If the Console widget DOESNT EXIST YET!

            self.tab.splitterV.addWidget(self.tab.term)

            self.ind = self.tab.splitterV.indexOf(self.tab.term)

        if self.tab.splitterV.indexOf(self.tab.term) == -1:  # If the terminal widget doesnt exist yet
            self.tab.splitterV.replaceWidget(self.o, self.tab.term)
            self.o = self.tab.splitterV.indexOf(self.tab.Console)

            self.ind = self.tab.splitterV.indexOf(self.tab.term)

    def realterminal(self):
        self.tab.splitterV.addWidget(self.tab.status)
        self.tab.status.addWidget(self.tab.hide_button)
        self.tab.splitterV.addWidget(self.tab.terminal)

    def terminal(self):
        active_tab = self.tab.tabs.currentWidget()

        if self.pyConsoleOpened:
            self.o = self.tab.splitterV.indexOf(self.tab.Console)
            self.ind = self.tab.splitterV.indexOf(self.tab.term)

            if self.ind == -1:
                if platform.system() == "Linux":
                    self.tab.Console.run("python3 " + active_tab.fileName)

                elif platform.system() == "Windows":
                    self.tab.Console.run("python " + active_tab.fileName)

                else:
                    self.tab.Console.run("python3 " + active_tab.fileName)

            else:
                self.tab.splitterV.replaceWidget(self.ind, self.tab.Console)

            try:

                if platform.system() == "Linux":
                    self.tab.Console.run("python3 " + active_tab.fileName)

                elif platform.system() == "Windows":
                    self.tab.Console.run("python " + active_tab.fileName)

                else:
                    self.tab.Console.run("python3 " + active_tab.fileName)

            except AttributeError as E:
                print(E)

        else:
            self.tab.splitterV.addWidget(self.tab.Console)

            try:
                active_tab = self.tab.tabs.currentWidget()

                if platform.system() == "Linux":
                    self.tab.Console.run("python3 " + active_tab.fileName)

                elif platform.system() == "Windows":
                    self.tab.Console.run("python " + active_tab.fileName)

                else:
                    self.tab.Console.run("python3 " + active_tab.fileName)

            except AttributeError as E:
                print(E)
                           

class PyHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, index=choiceIndex, *args):
        super(PyHighlighter, self).__init__(parent, *args)

        if index == "0":
            python = config0['files']['python']

        elif index == "1":
            python = config1['files']['python']

        elif index == "2":
            python = config2['files']['python']
        else:
            python = config0['files']['python']  # This is the default config

        self.highlightingRules = []
        self.formats = {}
        self.regex = {
            "class": "\\bclass\\b",
            "function": "[A-Za-z0-9_]+(?=\\()",
            "magic": "\\__[^']*\\__",
            "decorator": "@[^\n]*",
            "singleLineComment": "#[^\n]*",
            "quotation": "\"[^\"]*\"",
            "quotation2": "'[^\']*\'",
            "multiLineComment": "[-+]",
            "int": "\\b[-+]?[0-9]+\\b",
        }

        pyKeywordPatterns = keyword.kwlist

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(python['highlighting']['keyword']['color']))
        keywordFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in pyKeywordPatterns]

        for name, values in self.regex.items():
            self.formats[name] = QTextCharFormat()

            if name == "class":
                self.formats[name].setFontWeight(QFont.Bold)

            elif name == "function":
                self.formats[name].setFontItalic(True)

            elif name == "magic":
                self.formats[name].setFontItalic(True)

            self.formats[name].setForeground(QColor(python['highlighting'][name]['color']))

            self.highlightingRules.append((QRegExp(values), self.formats[name]))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        self.multiLineHighlight(text)

    def multiLineHighlight(self, text):

        comment = QRegExp('"""')
        if self.previousBlockState() == 1:
            start_index = 0
            index_step = 0
        else:
            start_index = comment.indexIn(text)
            while start_index >= 0 and self.format(start_index+2) in self.formats.values():
                start_index = comment.indexIn(text, start_index + 3)
            index_step = comment.matchedLength()

        while start_index >= 0:
            end = comment.indexIn(text, start_index + index_step)
            if end != -1:
                self.setCurrentBlockState(0)
                length = end - start_index + comment.matchedLength()
            else:
                self.setCurrentBlockState(1)
                length = len(text) - start_index

            self.setFormat(start_index, length, self.formats['multiLineComment'])
            start_index = comment.indexIn(text, start_index + length)


if __name__ == '__main__':
    if True:  # checkVersion("version.txt") != checkVerOnlineFunc():
        pass  # TODO: implement an updater

    app = QApplication(sys.argv)
    try:
        file = sys.argv[1]
    except IndexError:  # File not given
        file = None
    app.setStyle('Fusion')
    palette = QPalette()
    if choiceIndex == 0:
        editor = config0['editor']
    elif choiceIndex == 1:
        editor = config1['editor']
    elif choiceIndex == 2:
        editor = config2['editor']
    else:
        editor = config0['editor']
    ex = Main()
    palette.setColor(QPalette.Window, QColor(editor["windowColor"]))
    palette.setColor(QPalette.WindowText, QColor(editor["windowText"]))
    palette.setColor(QPalette.Base, QColor(editor["editorColor"]))
    palette.setColor(QPalette.AlternateBase, QColor(editor["alternateBase"]))
    palette.setColor(QPalette.ToolTipBase, QColor(editor["ToolTipBase"]))
    palette.setColor(QPalette.ToolTipText, QColor(editor["ToolTipText"]))
    palette.setColor(QPalette.Text, QColor(editor["editorText"]))
    palette.setColor(QPalette.Button, QColor(editor["buttonColor"]))
    palette.setColor(QPalette.ButtonText, QColor(editor["buttonTextColor"]))
    palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())
    palette.setColor(QPalette.HighlightedText, QColor(editor["HighlightedTextColor"]))
    app.setPalette(palette)
    ex.show()
    sys.exit(app.exec_())
