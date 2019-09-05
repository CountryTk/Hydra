from Hydra.utils.config import config_reader, LOCATION
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QDesktopWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QFileDialog,
    QAction,
    QApplication,
    QGridLayout,
    QSpacerItem,
)
from PyQt5.QtGui import QFont, QIcon, QCursor, QFont, QFontMetrics
from PyQt5.QtCore import Qt
import shutil
import os
import random

configs = [config_reader(0), config_reader(1), config_reader(2)]

with open(LOCATION + "default.json") as choice:
    choiceIndex = int(choice.read())

editor = configs[choiceIndex]["editor"]


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
        self.setWindowIcon(QIcon("resources/Python-logo-notext.svg_.png"))
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

        self.label.setText(
            "Theme "
            + str(index)
            + " selected\nNOTE: For some changes to work you need to restart Hydra"
        )
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

        self.successLabel.setText(
            "Successfully created a new project to: " + str(directory)
        )
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
        self.add_browser.showBrowser(
            self.url, self.helpword
        )  # self.add_browser should have the value <__main__.Main
        self.hide()

    # DONE
    def noMatch(self, word):

        self.label.setText("No matches found for word: " + str(word))
        self.button.setText("Ok")
        self.button.setAutoDefault(True)

        self.layout.addWidget(self.button)
        self.show()

    # DONE
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
        self.show()  #

    def getHelp(self, paren):
        self.add_browser = paren
        try:
            self.layout.removeWidget(self.deleteButton)
            self.layout.removeWidget(self.button)

        except AttributeError as E:
            print(E, " on line 208 in the file Messagebox.py")
        self.label.setText(
            "It seems like you made an error, would you like to get help?"
        )
        self.layout.addWidget(self.getHelpButton)
        self.layout.addWidget(self.button)
        config = editor
        if config["errorMessages"] is True:
            self.show()

        else:
            self.hide()


class NoMatch(QWidget):
    def __init__(self, word):

        super(NoMatch, self).__init__()

        self.setWindowFlags(
            Qt.Widget
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
        )

        self.layout = QHBoxLayout()

        self.word = word
        self.no_match = QLabel("No match found for word: {}".format(self.word))

        self.ok_button = QPushButton("OK")
        self.ok_button.setAutoDefault(True)
        self.ok_button.clicked.connect(self.ok_pressed)

        self.layout.addWidget(self.no_match)
        self.layout.addWidget(self.ok_button)
        self.setLayout(self.layout)

        self.show()

    def ok_pressed(self):

        self.hide()


class NewProject(QWidget):
    def __init__(self, parent=None):
        super(NewProject, self).__init__()

        self.layout = QVBoxLayout()
        self.parent = parent

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedWidth(100)
        self.create_button = QPushButton("Create")
        self.create_button.setFixedWidth(100)

        self.container = QVBoxLayout()

        self.button_layout = QGridLayout()
        self.button_layout.addWidget(self.create_button, 0, 5)
        self.button_layout.addWidget(QLabel(), 0, 2)
        self.button_layout.addWidget(self.cancel_button, 0, 0)

        self.error_layout = QHBoxLayout()
        self.error_label = QLabel()
        self.error_layout.addWidget(self.error_label)

        self.location_layout = QHBoxLayout()

        self.location_label = QLabel("Location: ")
        self.location_line = LineEdit()
        project_name = "Untitled" + str(random.randint(1, 420))
        path = os.path.expanduser("~/Documents/" + project_name)
        print(path)
        self.location_line.setPureText(path)

        self.dir_action = QAction(self)
        self._dir = None
        self.dir_action.setIcon(QIcon("resources/directory_icon.png"))

        self.location_line.addAction(self.dir_action, QLineEdit.TrailingPosition)

        self.dir_action.triggered.connect(self.get_dir)
        self.dir_action.hovered.connect(self.change_cursor)
        self.location_line.textChanged.connect(self.check_if_valid)
        self.cancel_button.clicked.connect(lambda: self.hide())
        self.create_button.clicked.connect(self.create_project)

        self.location_layout.addWidget(self.location_label)
        self.location_layout.addWidget(self.location_line)

        self.container.addLayout(self.location_layout)
        self.container.addLayout(self.error_layout)

        self.layout.addLayout(self.container)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def get_dir(self):
        # Get's the directory

        self._dir = QFileDialog.getExistingDirectory(
            None, "Select a folder:", "", QFileDialog.ShowDirsOnly
        )
        self.location_line.setPureText(self._dir)

    def change_cursor(self):
        # Changes the cursor to indicate that our QAction is clickable
        cursor = QCursor(Qt.PointingHandCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)

    def normal_cursor(self):
        # Returns the cursor to normal cursor
        cursor = QCursor(Qt.ArrowCursor)

        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)

    def check_if_valid(self):

        path = self.location_line.text()

        exists = os.path.exists(path)

        if exists:
            self.error_label.setText("Path already exists")
        else:
            self.error_label.setText("")

    def create_project(self):

        path = self.location_line.text()
        exists = os.path.exists(path)
        access = os.access(
            os.path.dirname(path), os.W_OK
        )  # Can we actually write to that path?

        if access and exists is False:
            os.makedirs(path)
            self.parent.openProjectWithPath(path)
            self.hide()

        elif exists:
            self.error_label.setText("Directory already exists")

        else:
            self.error_label.setText("Permission error")


class GetHelp(QWidget):
    def __init__(self, parent, helpword):

        super(GetHelp, self).__init__()

        self.layout = QHBoxLayout()
        self.parent = parent
        self.helpword = helpword

        self.help_label = QLabel(
            "It seems like you made an error, would you to get help?"
        )

        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")

        self.yes_button.clicked.connect(self.ok_pressed)
        self.no_button.clicked.connect(lambda: self.hide())

        self.layout.addWidget(self.help_label)
        self.setLayout(self.layout)

    def show_or_not(self):

        if editor["errorMessages"]:
            self.show()
        else:
            self.hide()

    def ok_pressed(self):

        self.url = "https://duckduckgo.com/?q=" + str(self.helpword)
        self.parent.showBrowser(
            self.url, self.helpword
        )  # self.add_browser should have the value <__main__.Main
        self.hide()


class LineEdit(QLineEdit):
    def __init__(self):

        super(LineEdit, self).__init__()

    def mouseMoveEvent(self, event):
        cursor = QCursor(Qt.ArrowCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)
        super().mouseMoveEvent(event)

    def setPureText(self, a0: str) -> None:
        # This will set text and resize to fit contents
        self.setText(a0)
        self.resize_contents()

    def resize_contents(self):
        text = self.text()

        font = QFont("", 0)
        metrics = QFontMetrics(font)

        width = metrics.width(text)
        height = metrics.height()

        self.setMinimumWidth(width + 40)
        self.setMinimumHeight(height + 15)


class GenericMessage(QWidget):
    def __init__(self, text):

        super(GenericMessage, self).__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(text)

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
