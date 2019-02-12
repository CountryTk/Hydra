import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont,  QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, qApp, QStatusBar
import platform
import random
from widgets.Messagebox import MessageBox
from utils.config import config_reader, config_choice
from utils.lastFileOpen import lastFileOpen, updateLastFileOpen
from widgets.Tabs import Tabs
from widgets.Content import Content
from widgets.Image import Image
from utils.find_all_files import DocumentSearch
from widgets.Browser import Browser
from resources.materialblack import material_blue

configs = [config_reader(0), config_reader(1), config_reader(2)]

with open("default.json") as choice:
    choiceIndex = int(choice.read())

os.environ["PYTHONUNBUFFERED"] = "1"


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.onStart(choiceIndex)
        self.status = QStatusBar(self)
        # Initializing the main widget where text is displayed
        self.tab = Tabs(self.openFile, app, palette, self)
        self.tabsOpen = []
        self.pic_opened = False

        self.dialog = MessageBox(self)

        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))  # Setting the window icon

        self.setWindowTitle('PyPad')  # Setting the window title
        
        self.os = platform.system()
        
        self.tab.tabs.currentChanged.connect(self.fileNameChange)
        self.search = DocumentSearch()
        self.openterm()
        self.openterminal()
        self.new()
        self.newProject()
        self.findDocument()
        self.openProjectF()
        self.open()
        self.save()
        self.saveAs()
        self.exit()
        
        self.dir_opened = False
        self._dir = None

        # Without this, the whole layout is broken
        self.setCentralWidget(self.tab)

        self.files = None  # Tracking the current file that is open
       # self.pyFileOpened = False  # Tracking if python file is opened, this is useful to delete highlighting

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
            editor = configs[0]['editor']

        elif index == 1:
            editor = configs[1]['editor']

        elif index == 2:
            editor = configs[2]['editor']

        else:
            editor = configs[0]['editor']

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
        toolMenu.addAction(self.openTermAct)
        toolMenu.addAction(self.openTerminalAct)
        
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

    def switchTabs(self):
        if self.tab.tabs.count() - 1 == self.tab.tabs.currentIndex():
            self.tab.tabs.setCurrentIndex(0)
        else:
            self.tab.tabs.setCurrentIndex(self.tab.tabs.currentIndex() + 1)

    def save(self):
        self.saveAct = QAction('Save')
        self.saveAct.setShortcut('Ctrl+S')

        self.saveAct.setStatusTip('Save a file')
        self.saveAct.triggered.connect(self.saveFile)

    def openterm(self):
        self.openTermAct = QAction('Run', self)
        self.openTermAct.setShortcut('Shift+F10')

        self.openTermAct.setStatusTip('Run your code')
        self.openTermAct.triggered.connect(self.execute_file)

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
        self.findDocumentAct.triggered.connect(self.temp)

    def temp(self):
        pass

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

    def openBrowser(self, url, word):
        widget = Browser(url)
        index = self.tab.tabs.addTab(widget, "Info about: " + str(word))
        self.tab.tabs.setCurrentIndex(index)

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
                        tab = Content(text, filename, basename, self, ex)
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
                tab = Content(text, filename, basename, self, ex)  # Creating a tab object *IMPORTANT*
                tab.saved = True
                tab.modified = False
            self.tab.tabCounter.append(tab.baseName)
            dirPath = os.path.dirname(filename)
            self.files = filename
            
            self.tabsOpen.append(self.files)

            index = self.tab.tabs.addTab(tab,
                                         tab.baseName)  # This is the index which we will use to set the current
            self.tab.tabs.setTabToolTip(index, str(tab.fileName))
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
                self.currentTab.editor.setFocus()  # Setting focus to the tab after we open it

            self.pic_opened = False

            updateLastFileOpen(filename)
        except (IsADirectoryError, AttributeError, UnboundLocalError, PermissionError) as E:
            print(E, " on line 346 in the file main.py")

    def newFile(self):
        text = ""
        if self._dir:
            base_file_name = "Untitled_file_" + str(random.randint(1, 100)) + ".py"
            fileName = str(self._dir) + "/" + base_file_name
        else:
            base_file_name = "Untitled_file_" + str(random.randint(1, 100)) + ".py"
            current = os.getcwd()
            fileName = current + "/" + base_file_name
            
        self.pyFileOpened = True
        # Creates a new blank file
        file = Content(text, fileName, base_file_name, self, ex)
        self.tab.splitterH.addWidget(self.tab.tabs)  # Adding tabs, now the directory tree will be on the left
        self.tab.tabCounter.append(file.fileName)
        self.tab.setLayout(self.tab.layout)  # Finally we set the layout
        index = self.tab.tabs.addTab(file, file.baseName)  # addTab method returns an index for the tab that was added
        self.tab.tabs.setTabToolTip(index, str(file.fileName))
        self.tab.tabs.setCurrentIndex(index)  # Setting focus to the new tab that we created
        widget = self.tab.tabs.currentWidget()

    def newProjectFolder(self):
        self.dialog = MessageBox(self.parent)
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
                    saveFile.write(active_tab.editor.text())
                    active_tab.saved = True
                    self.tab.events.look_for_dead_code(active_tab.editor.text())
                    active_tab.modified = False
                    saveFile.close()
                if active_tab.fileName.endswith(".py"):
                    active_tab.editor.updateAutoComplete(active_tab.fileName)
            else:
                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(options, 'Save File', '',
                                                   'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                   options=options)
                fileName = name[0]

                with open(fileName, "w+") as saveFile:
                    active_tab.saved = True
                    active_tab.modified = False
                    self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.text())
                    self.tab.events.look_for_dead_code(active_tab.editor.text())
                    saveFile.close()
                    if fileName.endswith(".py"):
                        active_tab.editor.updateAutoComplete(active_tab.fileName)
            ex.setWindowTitle("PyPad ~ " + str(active_tab.baseName) + " [SAVED]")
            active_tab.tokenize_file()
        except Exception as E:
            print(E, " on line 403 in the file main.py")
    
    def choose_python(self):
        if self.os == "Windows":
            return "python"
            
        elif self.os == "Linux":
            return "python3"
        
        elif self.os == "Darwin":
            return "python3"
         
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
                    saveFile.write(active_tab.editor.text())
                    text = active_tab.editor.text()
                    newTab = Content(str(text), fileName, baseName, self, ex)

                    self.tab.tabs.removeTab(active_index)  # When user changes the tab name we make sure we delete the old one
                    index = self.tab.tabs.addTab(newTab, newTab.baseName)  # And add the new one!
                    self.tab.tabs.setTabToolTip(index, str(newTab.fileName))

                    self.tab.tabs.setCurrentIndex(index)
                    newActiveTab = self.tab.tabs.currentWidget()

                    newActiveTab.editor.setFont(self.font)
                    newActiveTab.editor.setFocus()

                    saveFile.close()
                ex.setWindowTitle("PyPad ~ " + str(active_tab.baseName) + " [SAVED]")

            else:
                print("No file opened")

        except FileNotFoundError:
            print("File dialog closed")

    def realterminal(self):

        """
        Checking if the file executing widget already exists in the splitter layout:
         
        If it does exist, then we're going to replace the widget with the terminal widget, if it doesn't exist then
        just add the terminal widget to the layout and expand the splitter.

        """

        if self.tab.splitterV.indexOf(self.tab.Console) == 1:
            self.tab.splitterV.replaceWidget(self.tab.splitterV.indexOf(self.tab.Console), self.tab.terminal)
            self.tab.splitterV.setSizes([400, 10])
        else:
            self.tab.showConsole()

    def execute_file(self):
        """
        Checking if the terminal widget already exists in the splitter layout:

        If it does exist, then we're going to replace it, if it doesn't then we're just gonna add our file executer to
        the layout, expand the splitter and run the file.

        Then check if the file executer already exists, but is called again to run the file again

        """
        active_tab = self.tab.tabs.currentWidget()
        python_command = self.choose_python()
        if self.tab.splitterV.indexOf(self.tab.terminal) == 1:
            self.tab.splitterV.replaceWidget(self.tab.splitterV.indexOf(self.tab.terminal), self.tab.Console)
            self.tab.Console.run("{} ".format(python_command) + active_tab.fileName, active_tab.fileName)
            self.tab.splitterV.setSizes([400, 10])

        elif self.tab.splitterV.indexOf(self.tab.Console) == 1:
            self.tab.Console.run("{} ".format(python_command) + active_tab.fileName, active_tab.fileName)
        else:
            self.tab.showFileExecuter()
            self.tab.Console.run("{} ".format(python_command) + active_tab.fileName, active_tab.fileName)


if __name__ == '__main__':
    if True:  # checkVersion("version.txt") != checkVerOnlineFunc():
        pass  # TODO: implement an updater
    # from utils.install_punkt import install_punkt

    # install_punkt()

    app = QApplication(sys.argv)
    try:
        file = sys.argv[1]
    except IndexError:  # File not given
        file = lastFileOpen()
    app.setStyle('Fusion')
    palette = QPalette()
    editor = configs[choiceIndex]['editor']
    print(choiceIndex)

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
    app.setStyleSheet(material_blue)  # uncomment this to have a material blue theme
    ex.show()
    if file is not None:
        ex.openFile(file)
    sys.exit(app.exec_())
