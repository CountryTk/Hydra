from utils.config import config_reader
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QDesktopWidget, QLabel, \
    QVBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QIcon
import shutil
import os
config0 = config_reader(0)
config1 = config_reader(1)
config2 = config_reader(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())

if choiceIndex == 0:
    editor = config0['editor']
elif choiceIndex == 1:
    editor = config1['editor']
elif choiceIndex == 2:
    editor = config2['editor']
else:
    editor = config0['editor']


class MessageBox(QWidget):
    def __init__(self, parent, error=None, helpword=None, index=choiceIndex):
        super().__init__()
        self.helpword = helpword
        self.layout = QHBoxLayout(self)
        self.parent = parent
        self.index = str(index)
        self.screen_geomtery = QDesktopWidget().screenGeometry(-1)
        self.width = self.screen_geomtery.width()
        self.height = self.screen_geomtery.height()
        self.path = None
        self.add_browser = None
        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.deleteButton = QPushButton("Yes")
        self.button = QPushButton("No")
        self.cancel = QPushButton("Cancel")
        self.getHelpButton = QPushButton("Yes")
        self.closeAnywayButton = QPushButton()
        self.getHelpButton.setAutoDefault(True)
        self.saveButton = QPushButton("Save")

        self.deleteButton.clicked.connect(self.delete)
        self.cancel.clicked.connect(self.dont)
        self.button.clicked.connect(self.dont)
        self.getHelpButton.clicked.connect(self.gettingHelp)

        self.saved = None
        self.center()
        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)

        self.setFont(self.font)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def run(self, str, fileName):
        self.fileName = fileName
        baseName = os.path.basename(self.fileName)
        self.label.setText(str + baseName + " ?")
        self.deleteButton.setAutoDefault(True)
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.button)
        self.show()

    def delete(self):
        if os.path.isdir(self.fileName):  # If it is a directory
            shutil.rmtree(self.fileName)
        else:
            os.remove(self.fileName)
        self.hide()

    def dont(self):

        self.hide()

    def confirmation(self, index):

        self.label.setText \
            ("Theme " + str(index) + " selected\nNOTE: For some changes to work you need to restart PyPad")
        self.button.setText("Ok")
        self.button.setAutoDefault(True)

        self.button.setFocus()
        self.layout.addWidget(self.button)
        self.show()

    def success(self, directory):

        def _exit():
            self.hide()

        self.successButton = QPushButton("Ok")
        self.successButton.resize(10, 30)
        self.successLabel = QLabel()

        self.successLabel.setText("Successfully created a new project to: " + str(directory))
        self.successButton.clicked.connect(_exit)
        self.layout.addWidget(self.successLabel)
        self.layout.addWidget(self.successButton)

        self.show()

    def saveMaybe(self, file, tabCounter, tab, index):

        def _closeAnyway():
            try:
                file.deleteLater()
                tabCounter.pop(index)
                tab.removeTab(index)
                self.hide()
            except (IndexError, RuntimeError) as E:
                print(E, " on line 125 in the file Messagebox.py")

        def _hide():
            self.hide()

        self.label.setText("<b>Warning</b>, you have unsaved changes!")
        self.saveButton.setText("Ok")
        self.saveButton.setAutoDefault(True)

        self.closeAnywayButton.setText("Close anyway")
        self.saveButton.clicked.connect(_hide)
        self.closeAnywayButton.clicked.connect(_closeAnyway)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.closeAnywayButton)
        self.show()

    def gettingHelp(self):

        self.url = "https://duckduckgo.com/?q=" + str(self.helpword)
        self.add_browser.showBrowser(self.url, self.helpword)  # self.add_browser should have the value <__main__.Main
        self.hide()

    def noMatch(self, word):

        self.label.setText("No matches found for word: " + str(word))
        self.button.setText("Ok")
        self.button.setAutoDefault(True)

        self.layout.addWidget(self.button)
        self.show()

    def newProject(self):

        cwd = os.getcwd()
        self.vertical = QVBoxLayout()

        def createFolder():
            try:
                folderName = self.textField.text()
                directory = self.ProjectDirectory.text()

                if not os.path.exists(folderName):
                    self.path = str(directory) + str(folderName)
                    os.makedirs(self.path)
                    self.hide()
                    self.success(self.path)

                else:
                    print("File already exists")

            except Exception as E:
                print(E, " on line 176 in the file Messagebox.py")

        self.setWindowTitle("New project")
        self.projectLabel = QLabel()
        self.directoryLabel = QLabel()

        self.directoryLabel.setText("Where do you want to create it?")
        self.projectLabel.setText("Enter a new project name: ")
        self.ProjectDirectory = QLineEdit()
        self.ProjectDirectory.setText(cwd)
        self.textField = QLineEdit()

        self.textFieldButton = QPushButton("Create")
        self.textFieldButton.clicked.connect(createFolder)
        self.vertical.addWidget(self.projectLabel)
        self.vertical.addWidget(self.textField)
        self.vertical.addWidget(self.directoryLabel)
        self.vertical.addWidget(self.ProjectDirectory)
        self.vertical.addWidget(self.textFieldButton)
        self.vertical.addWidget(self.cancel)
        self.layout.removeWidget(self.label)
        self.layout.addLayout(self.vertical)
        self.setLayout(self.layout)
        self.show()

    def getHelp(self, paren):
        self.add_browser = paren
        try:
            self.layout.removeWidget(self.deleteButton)
            self.layout.removeWidget(self.button)

        except AttributeError as E:
            print(E, " on line 208 in the file Messagebox.py")
        self.label.setText("It seems like you made an error, would you like to get help?")
        self.layout.addWidget(self.getHelpButton)
        self.layout.addWidget(self.button)
        if self.index == "0":

            config = config0

        elif self.index == "1":

            config = config1

        elif self.index == "2":
            config = config2

        else:

            config = config0

        if config["editor"]["errorMessages"] is True:
            self.show()

        else:
            self.hide()

