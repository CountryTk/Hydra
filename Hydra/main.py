# Setting up imports
import sys
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QProcess
from PyQt5.QtGui import QColor, QPalette, QFont, QIcon, QTextCursor
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QFileDialog,
    qApp,
    QLabel,
    QStatusBar,
    QPushButton,
    QProgressBar,
)
from PyQt5.QtTest import QTest
import platform
import random
from Hydra.widgets.Messagebox import MessageBox, NewProject
from Hydra.utils.config import config_reader, config_choice, LOCATION
from Hydra.widgets.Tabs import Tabs
from Hydra.utils.last_open_file import update_previous_file, get_last_file
from Hydra.widgets.Content import Content
from Hydra.widgets.Image import Image
from Hydra.widgets.Events import DeadCodeCheker
from Hydra.utils.find_utility import DocumentSearch
from Hydra.widgets.SaveFile import SaveFile
from Hydra.widgets.Label import StatusLabel
from Hydra.widgets.Browser import Browser
from Hydra.resources.materialblack import material_blue
from Hydra.utils.check_update import show_update, make_decision
import shutil

configs = [config_reader(0), config_reader(1), config_reader(2)]

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

# os.environ["PYTHONUNBUFFERED"] = "1"  # This is just an environment variable that PyCharm uses


class Main(QMainWindow):
    def __init__(self, app, palette, editor, parent=None):
        super().__init__(parent)

        self.editor = editor  # Current config chosen (can be one of 3 config<N>.json)
        self.onStart(choiceIndex)   # Initializing config options 
        self.status = QStatusBar(self)  # Status bar for displaying useful info like update found etc

        # Initializing the main widget where text is displayed
        self.tab = Tabs(self.cleanOpen, app, palette, self)
        # self.tabsOpen = []

        self.pic_opened = False  # This is used to open pictures but right now that feature is disabled
        self.dialog = MessageBox(self)  # Handles dialogs, for now it only creates the create new project dialog

        self.setWindowIcon(
            QIcon("resources/Python-logo-notext.svg_.png")
        )  # Setting the window icon

        self.setWindowTitle("Hydra")  # Setting the window title

        self.status_font = QFont(editor["statusBarFont"], editor["statusBarFontSize"])  # Status bar font

        self.os = platform.system()

        self.tab.tabs.currentChanged.connect(self.fileNameChange)  # To change the title of the window when tab changes
        self.search = DocumentSearch()  # To find documents in the whole system, also not quite working today

        # Initializing QActions that can be triggered from a QMenu or via keyboard shortcuts
        self.openterm()
        self.openterminal()
        # self.split2Tabs()
        self.new()
        self.newProject()
        self.findDocument()

        self.openProjectF()
        self.open()
        self.save()
        self.saveAs()
        self.exit()

        self.thread = UpdateThread()  # Update checking runs on its own thread to prevent main GUI from blocking
        self.thread.start()

        # Data retrieved from the update thread gets processed check_updates
        self.thread.textSignal.connect(self.check_updates)

        # Attributes to manage opening directories and such
        self.dir_opened = False
        self._dir = None

        self.update_progress = QProgressBar()
        self.update_progress.setMaximumWidth(225)

        self.update_progress.setStyleSheet(self.update_progress.styleSheet())

        self.setCentralWidget(self.tab)  # QMainWindow's central widget

        self.files = None  # Tracking the current file that is open

        self.dead_code_thread = DeadCodeCheker()  # This checks for dead code

        self.dead_code_thread.infoSignal.connect(self.write_dead_code_info)

        self.stack = []  # Used for tracking when to check for dead code

        self.tab_to_write_to = None

        self.tagInfo = StatusLabel(text="", font=self.status_font)

        self.initUI()  # Main UI

    def write_dead_code_info(self, text):

        self.tab.events.info_bar.setText(text)

    def check_updates(self, text):
        """
        A function to check for updates and ask the user if they want to update or not
        """
        self.update_label = QLabel()
        self.update_label.setFont(
            QFont(self.editor["generalFont"], self.editor["generalFontSize"])
        )
        self.update_label.setFont(self.status_font)
        self.update_label.setText(text)
        self.status.addWidget(self.update_label)

        if text != "An update is available, would you like to update?":
            pass
        else:
            self.button = QPushButton("Update")
            self.button.setFont(
                QFont(self.editor["generalFont"], self.editor["generalFontSize"])
            )
            self.status.addWidget(self.button)
            self.button.clicked.connect(self.update_Hydra)

    def update_Hydra(self):
        """
        This function gets used when the user wants to update Hydra
        This function is not finished so it doesn't do any updating
        """

        self.update_label.setText("Updating...")
        self.status.removeWidget(self.button)
        self.status.addWidget(self.update_progress)

        for i in range(101):
            self.update_progress.setValue(i)
            QTest.qWait(random.randint(50, 75))
        # make_decision(True)

    def fileNameChange(self):

        try:
            currentFileName = self.tab.tabs.currentWidget().baseName
            self.setWindowTitle("Hydra ~ " + str(currentFileName))

        except AttributeError:
            self.setWindowTitle("Hydra ~ ")

    def onStart(self, index):

        try:
            editor = configs[index]["editor"]
            if editor["windowStaysOnTop"] is True:
                self.setWindowFlags(Qt.WindowStaysOnTopHint)

            else:
                pass

        except Exception as err:
            pass  # log exception

        self.font = QFont()
        self.font.setFamily(self.editor["editorFont"])

        self.font.setPointSize(self.editor["editorFontSize"])
        self.tabSize = self.editor["TabWidth"]

    def initUI(self):

        self.setStatusBar(self.status)  # Initializing the status bar

        self.font.setFixedPitch(True)
        menuFont = QFont()
        menuFont.setFamily(self.editor["menuFont"])
        menuFont.setPointSize(self.editor["menuFontSize"])
        menu = self.menuBar()
        menu.setFont(menuFont)
        # Creating the file menu

        fileMenu = menu.addMenu("File")

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

        toolMenu = menu.addMenu("Tools")
        toolMenu.addAction(self.openTermAct)
        toolMenu.addAction(self.openTerminalAct)
        # toolMenu.addAction(self.split2TabsAct)

        searchDoc = menu.addMenu("Find document")

        searchDoc.addAction(self.findDocumentAct)

        self.showMaximized()

    def open(self):
        self.openAct = QAction("Open...", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.setStatusTip("Open a file")
        self.openAct.triggered.connect(self.openFileFromMenu)

    def closeEvent(self, QCloseEvent):

        os._exit(42)  # This makes sure every thread gets killed

    def new(self):
        self.newAct = QAction("New")
        self.newAct.setShortcut("Ctrl+N")

        self.newAct.setStatusTip("Create a new file")
        self.newAct.triggered.connect(self.newFile)

    def newProject(self):
        self.newProjectAct = QAction("New project")
        self.newProjectAct.setShortcut("Ctrl+Shift+N")

        self.newProjectAct.setStatusTip("Create a new project")
        self.newProjectAct.triggered.connect(self.newProjectFolder)

    def openProjectF(self):
        self.openProjectAct = QAction("Open project")
        self.openProjectAct.setShortcut("Ctrl+Shift+O")

        self.openProjectAct.setStatusTip("Open a project")
        self.openProjectAct.triggered.connect(self.openProject)

    def split2Tabs(self):
        self.split2TabsAct = QAction("Split the first 2 tabs")
        self.split2TabsAct.setShortcut("Ctrl+Alt+S")

        self.split2TabsAct.setStatusTip("Splits the first 2 tabs into one tab")
        self.split2TabsAct.triggered.connect(self.tab.split)

    def switchTabs(self):
        if self.tab.tabs.count() - 1 == self.tab.tabs.currentIndex():
            self.tab.tabs.setCurrentIndex(0)
        else:
            self.tab.tabs.setCurrentIndex(self.tab.tabs.currentIndex() + 1)

    def save(self):
        self.saveAct = QAction("Save")
        self.saveAct.setShortcut("Ctrl+S")

        self.saveAct.setStatusTip("Save a file")
        self.saveAct.triggered.connect(self.saveFile)

    def openterm(self):
        self.openTermAct = QAction("Run", self)
        self.openTermAct.setShortcut("Shift+F10")

        self.openTermAct.setStatusTip("Run your code")
        self.openTermAct.triggered.connect(self.execute_file)

    def openterminal(self):
        self.openTerminalAct = QAction("Terminal", self)
        self.openTerminalAct.setShortcut("Ctrl+T")

        self.openTerminalAct.setStatusTip("Open a terminal")
        self.openTerminalAct.triggered.connect(self.realterminal)

    def saveAs(self):
        self.saveAsAct = QAction("Save As...")
        self.saveAsAct.setShortcut("Ctrl+Shift+S")

        self.saveAsAct.setStatusTip("Save a file as")
        self.saveAsAct.triggered.connect(self.saveFileAs)

    def findDocument(self):
        self.findDocumentAct = QAction("Find document")
        self.findDocumentAct.setShortcut("Ctrl+Shift+F")

        self.findDocumentAct.setStatusTip("Find a document")
        self.findDocumentAct.triggered.connect(self.temp)

    def temp(self):
        pass

    def findDocumentFunc(self):

        self.search.run()

    def exit(self):
        self.exitAct = QAction("Quit", self)
        self.exitAct.setShortcut("Ctrl+Q")

        self.exitAct.setStatusTip("Exit application")
        self.exitAct.triggered.connect(self.lets_exit)

    def lets_exit(self):
        # self.saveFile()
        qApp.quit()

    def openFileFromMenu(self):
        options = QFileDialog.Options()

        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Open a file",
            "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
            options=options,
        )

        if filenames:  # If file is selected, we can open it
            filename = filenames[0]
            if filename[-3:] in ["gif", "png", "jpg", "bmp"] or filename[-4:] in [
                "jpeg"
            ]:
                self.pic_opened = True
            self.cleanOpen(filename, self.pic_opened)

    def openBrowser(self):
        widget = Browser("https://duckduckgo.com")
        word = ""
        index = self.tab.tabs.addTab(widget, "Info about: " + str(word))
        self.tab.tabs.setCurrentIndex(index)

    def cleanOpen(self, filename, pic_opened=False, searchCommand=None):

        basename = os.path.basename(filename)
        if os.path.isdir(filename):
            return
        if pic_opened:
            tab = Image(filename, basename)
        else:
            tab = Content("", filename, basename, self, False, searchCommand)

        for index, tab_name in enumerate(self.tab.tabCounter):

            if (
                tab_name == basename
            ):  # If we already have a file open and we're trying to open the same file, then do nothing

                if searchCommand:
                    print(searchCommand, " search ocmmand")
                    tab.searchFor(searchCommand)

                return

        tab.start_opening()  # TODO: Only works for NON image files right now

        label = QLabel("Loading...")
        label.setAlignment(Qt.AlignCenter)
        index_to_remove = self.tab.tabs.addTab(label, "")  # lmao it works

        tab.readyToShow.connect(
            lambda state: self.addTab(state, tab, basename, index_to_remove)
        )

        update_previous_file(filename)

    def addTab(self, state, tab, basename, index_to_remove):
        """
        Removes given tab and adds a new tab and makes it active
        """
        self.tab.tabs.removeTab(index_to_remove)
        index = self.tab.tabs.addTab(tab, basename)
        self.tab.tabs.setCurrentIndex(index)
        self.tab.tabCounter.append(basename)

    # Not in use
    def openFile(self, filename):

        try:
            for index, tabName in enumerate(self.tab.tabCounter):
                with open(filename, "r+") as file_o:
                    print("first open")
                    if filename[-3:] in ["gif", "png", "jpg", "bmp"] or filename[
                        -4:
                    ] in ["jpeg"]:
                        self.pic_opened = True
                    else:
                        self.pic_opened = False
                    try:
                        text = file_o.read()

                    except UnicodeDecodeError as E:
                        text = str(E)

                    basename = os.path.basename(filename)
                    if not self.pic_opened:
                        tab = Content(text, filename, basename, self)
                        tab.saved = True
                        tab.modified = False
                    else:
                        tab = Image(filename, basename)

                if tabName == tab.baseName:
                    self.tab.tabs.removeTab(index)

                    self.tab.tabCounter.remove(tab.baseName)
            try:
                with open(filename, "r+") as file_o:
                    try:
                        if self.pic_opened is not True:
                            text = file_o.read()
                        else:
                            text = None
                    except (FileNotFoundError, UnicodeDecodeError, AttributeError) as E:
                        text = str(E)
            except FileNotFoundError:
                with open(filename, "w+") as newFileCreated:
                    print("third open")
                    text = newFileCreated.read()

            basename = os.path.basename(filename)
            if self.pic_opened is True:
                tab = Image(filename, basename)

            else:
                tab = Content(
                    text, filename, basename, self
                )  # Creating a tab object *IMPORTANT*
                tab.saved = True
                tab.modified = False
            self.tab.tabCounter.append(tab.baseName)
            dirPath = os.path.dirname(filename)
            self.files = filename

            # self.tabsOpen.append(self.files)

            index = self.tab.tabs.addTab(
                tab, tab.baseName
            )  # This is the index which we will use to set the current
            self.tab.tabs.setTabToolTip(index, str(tab.fileName))
            if (
                not self.dir_opened
            ):  # If a project isn't opened then we open a directory everytime we open a file
                self.tab.directory.openDirectory(dirPath)

                self.tab.showDirectory()
            else:
                pass

            self.tab.setLayout(self.tab.layout)  # Finally we set the layout
            update_previous_file(filename)
            self.tab.tabs.setCurrentIndex(
                index
            )  # Setting the index so we could find the current widget

            self.currentTab = self.tab.tabs.currentWidget()

            if self.pic_opened is not True:
                self.currentTab.editor.setFont(self.font)  # Setting the font
                self.currentTab.editor.setFocus()  # Setting focus to the tab after we open it

            self.pic_opened = False
        except (
            IsADirectoryError,
            AttributeError,
            UnboundLocalError,
            PermissionError,
        ) as E:
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
        file = Content(text, fileName, base_file_name, self)
        self.tab.splitterH.addWidget(
            self.tab.tabs
        )  # Adding tabs, now the directory tree will be on the left
        self.tab.tabCounter.append(file.fileName)
        self.tab.setLayout(self.tab.layout)  # Finally we set the layout
        index = self.tab.tabs.addTab(
            file, file.baseName
        )  # addTab method returns an index for the tab that was added
        self.tab.tabs.setTabToolTip(index, str(file.fileName))
        self.tab.tabs.setCurrentIndex(
            index
        )  # Setting focus to the new tab that we created
        widget = self.tab.tabs.currentWidget()

    def newProjectFolder(self):
        self.dialog = NewProject(self)
        self.dialog.show()

    def openProject(self):

        self._dir = QFileDialog.getExistingDirectory(
            None, "Select a folder:", "", QFileDialog.ShowDirsOnly
        )

        self.tab.directory.openDirectory(self._dir)
        self.dir_opened = True

        # Generating tags file
        self.generateTagFile(self._dir)

        self.tab.showDirectory()

    def generateTagFile(self, directoryLocation: str) -> bool:

        location = shutil.which("ctags")
        appDir = os.getcwd()

        if location is None:
            print("Please download universal ctags from the website https://github.com/universal-ctags/ctags")
            return False

        else:
            os.chdir(directoryLocation)
            generateProcess = QProcess(self)
            command = [location, "-R"]
            generateProcess.start(" ".join(command))
            self.tagInfo.setText("Generating tags file...")
            self.status.addWidget(self.tagInfo, Qt.AlignRight)
            generateProcess.finished.connect(lambda: self.afterTagGeneration(appDir))

    def afterTagGeneration(self, appDir: str) -> None:

        os.chdir(appDir)
        print(os.getcwd())
        self.status.removeWidget(self.tagInfo)

    def parseTagFile(self):
        pass

    def openProjectWithPath(self, path):

        self.tab.directory.openDirectory(path)
        self.dir_opened = True
        self._dir = path
        self.tab.showDirectory()

    def saveFile(self):
        self.stack.append(1)
        try:
            active_tab = self.tab.tabs.currentWidget()
            if self.tab.tabs.count():  # If a file is already opened
                # self.save_thread.add_args(active_tab)
                # self.save_thread.start()
                active_tab.start_saving()
                active_tab.saved = True
                # active_tab.start_from = os.path.getsize(active_tab.fileName)
                # self.dead_code_thread.add_args(active_tab.editor.toPlainText())
                # self.dead_code_thread.start()  # TODO: THrow this analyzer into a code analyzer
                if len(self.stack) > 5:
                    self.dead_code_thread.add_args(active_tab.editor.toPlainText())
                    self.dead_code_thread.start()  # TODO: THrow this analyzer into a code analyzer
                    self.stack = []
                active_tab.modified = False
                """f
                if active_tab.fileName.endswith(".py"):
                    active_tab.editor.updateAutoComplete(active_tab.fileName)
                """
            else:
                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(
                    self,
                    "Save File",
                    "",
                    "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
                    options=options,
                )
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    active_tab.saved = True
                    active_tab.modified = False
                    # self.tabsOpen.append(fileName)
                    saveFile.write(active_tab.editor.toPlainText())
                    self.tab.events.look_for_dead_code(active_tab.editor.toPlainText())
                    saveFile.close()
                    """
                    if fileName.endswith(".py"):
                        active_tab.editor.updateAutoComplete(active_tab.fileName)
                    """
            self.setWindowTitle("Hydra ~ " + str(active_tab.baseName) + " [SAVED]")
            active_tab.tokenize_file()
        except Exception as E:
            print(E, " on line 403 in the file main.py")

    def choose_python(self):

        return sys.executable

    def saveFileAs(self):

        try:
            active_tab = self.tab.tabs.currentWidget()
            if active_tab is not None:
                active_index = self.tab.tabs.currentIndex()

                options = QFileDialog.Options()
                name = QFileDialog.getSaveFileName(
                    self,
                    "Save File",
                    "",
                    "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
                    options=options,
                )
                fileName = name[0]
                with open(fileName, "w+") as saveFile:
                    active_tab.saved = True
                    active_tab.modified = False
                    # self.tabsOpen.append(fileName)

                    try:
                        baseName = os.path.basename(fileName)
                    except AttributeError:
                        print("All tabs closed")
                    saveFile.write(active_tab.editor.toPlainText())
                    text = active_tab.editor.toPlainText()
                    newTab = Content(str(text), fileName, baseName, self)
                    newTab.ready = True
                    self.tab.tabs.removeTab(
                        active_index
                    )  # When user changes the tab name we make sure we delete the old one
                    index = self.tab.tabs.addTab(
                        newTab, newTab.baseName
                    )  # And add the new one!
                    self.tab.tabs.setTabToolTip(index, str(newTab.fileName))

                    self.tab.tabs.setCurrentIndex(index)
                    newActiveTab = self.tab.tabs.currentWidget()

                    newActiveTab.editor.setFont(self.font)
                    newActiveTab.editor.setFocus()

                    saveFile.close()
                self.setWindowTitle("Hydra ~ " + str(active_tab.baseName) + " [SAVED]")

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
            self.tab.splitterV.replaceWidget(
                self.tab.splitterV.indexOf(self.tab.Console), self.tab.terminal
            )
            self.tab.splitterV.setSizes([400, 10])
        else:
            self.tab.showConsole()

    def open_documentation(self, data, word):

        """
        Opens documentation for a built in function
        """
        data = data.replace("|", "")
        index = self.tab.tabs.addTab(
            Content(
                data,
                os.getcwd() + "/" + str(word) + ".doc",
                str(word) + ".doc",
                self,
                True,
            ),
            str(word),
        )
        self.tab.tabs.setCurrentIndex(index)

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
            self.tab.splitterV.replaceWidget(
                self.tab.splitterV.indexOf(self.tab.terminal), self.tab.Console
            )
            self.tab.Console.run(
                "{} ".format(python_command) + active_tab.fileName, active_tab.fileName
            )
            self.tab.splitterV.setSizes([400, 10])

        elif self.tab.splitterV.indexOf(self.tab.Console) == 1:
            self.tab.Console.run(
                "{} ".format(python_command) + active_tab.fileName, active_tab.fileName
            )
            self.tab.splitterV.setSizes([400, 10])
        else:
            self.tab.showFileExecuter()
            self.tab.Console.run(
                "{} ".format(python_command) + active_tab.fileName, active_tab.fileName
            )
            self.tab.splitterV.setSizes([400, 10])

    def jumpToDef(self, tagList: list):

        print(tagList)

        tagInfo = tagList[0]
        fileName = tagList[1]
        searchCommand = tagList[2]

        self.cleanOpen(fileName, False, searchCommand)


class UpdateThread(QThread):

    textSignal = pyqtSignal(str)

    def __init_(self):
        super().__init__()

    def run(self):

        self.textSignal.emit(show_update())


def launch():
    # from utils.install_punkt import install_punkt

    # install_punkt()

    app = QApplication(sys.argv)

    try:
        file = sys.argv[1]
    except IndexError:  # File not given
        file = get_last_file()
    app.setStyle("Fusion")
    palette = QPalette()
    editor = configs[choiceIndex]["editor"]

    ex = Main(app, palette, editor)
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
        ex.cleanOpen(file)
        ex.openProjectWithPath(os.getcwd())

    sys.exit(app.exec_())


if __name__ == "__main__":
    launch()
