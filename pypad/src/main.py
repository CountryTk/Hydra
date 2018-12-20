import sys
import os
from find_all import find_all
import keyword
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRect, QRegExp, QDir, QThread, pyqtSignal, QObject, QProcess, pyqtSlot, QPoint
from PyQt5.QtGui import QColor, QPainter, QPalette, QSyntaxHighlighter, QFont, QTextCharFormat, QIcon, QTextOption,\
    QPixmap, QKeySequence, QTextCursor, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, \
    QVBoxLayout, QTabWidget, QFileDialog, QPlainTextEdit, QHBoxLayout, qApp, QTreeView, QFileSystemModel,\
    QSplitter, QLabel, QComboBox, QPushButton, QShortcut, QCompleter, QLineEdit, QInputDialog, QMenu
import platform
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
import random
import getpass
from predictionList import wordList
from search_algorithm import tokenize
from find_all_files import documentSearch
from checkVer import checkVersion
from checkVerOnline import checkVerOnlineFunc
#from updatePyPad import updatePyPadFunc
import socket
import config
import webbrowser
from TerminalBarWidget import TerminalBar
import shutil

config0 = config.read(0)
config1 = config.read(1)
config2 = config.read(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())

lineBarColor = QColor(53, 53, 53)

os.environ["PYTHONUNBUFFERED"] = "1"


class NumberBar(QWidget):
    def __init__(self, parent=None, index=choiceIndex):
        super().__init__(parent)
        self.editor = parent
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')
        self.index = index

    def update_on_scroll(this, rect, scroll):
        if this.isVisible():
            if scroll:
                this.scroll(0, scroll)
            else:
                this.update()

    def update_width(this, string):
        width = this.fontMetrics().width(str(string)) + 28
        if this.width() != width:
            this.setFixedWidth(width)

    def paintEvent(this, event):
        if this.index == "0":
            config = config0
        elif this.index == "1":
            config = config1
        elif this.index == "2":
            config = config2
        else:

            config = config0
        if this.isVisible():
            block = this.editor.firstVisibleBlock()
            height = this.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(this)
            painter.fillRect(event.rect(), lineBarColor)
            if config['editor']['NumberBarBox'] is True:
                painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)

            font = painter.font()

            current_block = this.editor.textCursor().block().blockNumber() + 1

            while block.isValid():
                block_geometry = this.editor.blockBoundingGeometry(block)
                offset = this.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1
                rect = QRect(0, block_top, this.width() - 5, height)

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


class Console(QWidget):
    errorSignal = pyqtSignal(str)
    outputSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.editor = PlainTextEdit(self)
        self.editor.setReadOnly(True) 
        self.custom = Customize()
        self.font = QFont()
        self.numbers = TerminalBar(self.editor, index=self.custom.index)

        self.dialog = MessageBox()
        self.font.setFamily(editor["editorFont"])
        self.terminateButton = QPushButton()
        self.terminateButton.setIcon(QIcon("resources/square.png"))
        self.terminateButton.clicked.connect(self.terminate)
        self.font.setPointSize(12)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.numbers)
        self.layout.addWidget(self.editor, 1)
        self.layout.addWidget(self.terminateButton)

        self.setLayout(self.layout)
        self.output = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.error = None
        self.finished = False
        self.editor.setFont(self.font)

        self.process = QProcess()
        self.state = None
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)

    def onReadyReadStandardError(self):
        try:
            self.error = self.process.readAllStandardError().data().decode()

            self.editor.appendPlainText(self.error)

            self.errorSignal.emit(self.error)
            if self.error == "":
                pass
            else:
                self.error = self.error.split(os.linesep)[-2]
                self.dialog.helpword = str(self.error)
                self.dialog.getHelp()
        except IndexError as E:
            print(E)

    def onReadyReadStandardOutput(self):
        try:
            self.result = self.process.readAllStandardOutput().data().decode()
        except UnicodeDecodeError as E:
            print(E)
        self.editor.appendPlainText(self.result.strip("\n"))
        self.state = self.process.state()

        self.outputSignal.emit(self.result)

    def ifFinished(self, exitCode, exitStatus):
        self.finished = True

    def run(self, command):
        """Executes a system command."""
        # clear previous text
        self.editor.clear()
        # self.editor.setPlainText("[" + str(getpass.getuser()) + "@" + str( socket.gethostname()) + "]" +
                                 #"   ~/" + str(os.path.basename(os.getcwd())) + " >$")

        if self.process.state() == 1 or self.process.state() == 2:
            self.process.kill()
            self.editor.setPlainText("Process already started, terminating")
        else:
            self.process.start(command)

    def terminate(self):

        if self.process.state() == 2:
            self.process.kill()


class PlainTextEdit(QPlainTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.font = QFont()
        self.size = 12
        self.dialog = MessageBox()
        self.menu_font = QFont()
        self.menu_font.setFamily("Iosevka")
        self.menu_font.setPointSize(10)
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.focused = None

        self.replace_tabs = 4
        self.setWordWrapMode(4)
        self.setFont(self.font)
        self.l = 0
        self.highlightingRules = []
        self.indexes = None
        
        self.setTabStopWidth(editor["TabWidth"])
        self.createStandardContextMenu()

        self.setWordWrapMode(QTextOption.NoWrap)
        
       
        
    def newFile(self):
        """This and most of the functions below will just be wrappers for the functions defined in Main"""
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.parent.parent.newFile)
    
    def openFile(self):
        
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.parent.parent.openFileFromMenu)
    
    def runFile(self):
        
        self.run_action = QAction("Run")
        self.run_action.triggered.connect(self.parent.parent.Terminal)
    
    def contextMenuEvent(self, event):
         
        menu = QMenu()
        """Initializing actions"""
        self.newFile()
        self.openFile()
        self.runFile()
        
        menu.addAction(self.new_action)
        menu.addAction(self.open_action)
        menu.addAction(self.run_action)
        
        menu.setFont(self.menu_font)
    
        menu.exec(event.globalPos())
        del menu
    
    def moveCursorPosBack(self):
        textCursor = self.textCursor()
        textCursorPos = textCursor.position()

        textCursor.setPosition(textCursorPos - 1)
        self.setTextCursor(textCursor)

    def keyPressEvent(self, e):
        textCursor = self.textCursor()
        key = e.key()

        if key == Qt.Key_H:
            # self.parent.completer.wordList
            # TODO: implement dynamic completion
            pass
            
        textCursorPos = textCursor.position()
        isSearch = (e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F)
        
        if isSearch:
            try:
                currentWidget = self.parent
                currentFile =  currentWidget.fileName
                currentEditor = currentWidget.editor

                textCursor = currentEditor.textCursor()
                textCursorPos = textCursor.position()
    
            except (AttributeError, UnboundLocalError) as E:
                print(E)
                
            if currentWidget is not None:
                text, okPressed = QInputDialog.getText(self, 'Find', 'Find what: ')
                if okPressed:
                    if text == "":
                        text = " "
                        self.dialog.noMatch(text)
                    self.searchtext = text
                    try:
                        with open(currentFile, 'r') as file:
                            contents = file.read()
                            self.indexes = list(find_all(contents, text))
                            if len(self.indexes) == 0:
                                self.dialog.noMatch(text)
                                
                    except FileNotFoundError as E:
                        print(E)
        
        if key == Qt.Key_QuoteDbl:
            self.insertPlainText('"')
            self.moveCursorPosBack()
            
        if (e.modifiers() == Qt.ControlModifier and e.key() == 61):  # Press Ctrl+Equal key to make font bigger
            
            self.font.setPointSize(self.size + 1)
            self.font.setFamily(editor["editorFont"])
            self.setFont(self.font)    
            self.size += 1
            
        if (e.modifiers() == Qt.ControlModifier and e.key() == 45): # Press Ctrl+Minus key to make font smaller
            
            self.font.setPointSize(self.size - 1)
            
            self.font.setFamily(editor["editorFont"])
            self.setFont(self.font)    
            self.size -= 1   
            
        if key == Qt.Key_F3:
            try:                
                index = self.indexes[0 + self.l]
                currentWidget = self.parent
                currentFile =  currentWidget.fileName
                currentEditor = currentWidget.editor
                textCursor.setPosition(index)
                textCursor.movePosition(textCursor.Right, textCursor.KeepAnchor, len(self.searchtext))
                currentEditor.setTextCursor(textCursor)
                self.l += 1
            except IndexError:
                self.l = 0
                
        if key == 39:
            self.insertPlainText("'")
            self.moveCursorPosBack()

        if key == Qt.Key_BraceLeft:
            self.insertPlainText("}")
            self.moveCursorPosBack()

        if key == Qt.Key_BracketLeft:
            self.insertPlainText("]")
            self.moveCursorPosBack()
            
        if key == Qt.Key_ParenLeft:
            
            self.insertPlainText(")")
            self.moveCursorPosBack()
            
        if key == Qt.Key_ParenRight:
            textCursor = self.textCursor()
            textCursor.select(QTextCursor.WordUnderCursor)
            if textCursor.selectedText() == "()" or "()" in textCursor.selectedText():
                return    
                
        if key == Qt.Key_BraceRight:
            textCursor = self.textCursor()
            textCursor.select(QTextCursor.WordUnderCursor)
            if textCursor.selectedText == "":
                return    
                
        if key not in [16777217, 16777219, 16777220]:
            
            super().keyPressEvent(e)
            return

        e.accept()
        cursor = self.textCursor()
        if key == 16777217: # and self.replace_tabs:
            amount = 4 - self.textCursor().positionInBlock() % 4
            self.insertPlainText(' ' * amount)

        elif key == 16777219 and cursor.selectionStart() == cursor.selectionEnd() and self.replace_tabs and \
                cursor.positionInBlock():
            position = cursor.positionInBlock()
            end = cursor.position()
            start = end - (position % 4)

            if start == end and position >= 4:
                start -= 4

            string = self.toPlainText()[start:end]
            if not len(string.strip()): # if length is 0 which is binary for false
                for i in range(end - start):
                    cursor.deletePreviousChar()
            else:
                super().keyPressEvent(e)
            

        elif key == 16777220:
            end = cursor.position()
            start = end - cursor.positionInBlock()
            line = self.toPlainText()[start:end]
            indentation = len(line) - len(line.lstrip())
            
            chars = '\t'
            if self.replace_tabs:
                chars = '    '
                indentation /= self.replace_tabs

            if line.endswith(':'):
                if self.replace_tabs:
                    indentation += 1

            super().keyPressEvent(e)
            self.insertPlainText(chars * int(indentation))
            
        else:
            super().keyPressEvent(e)


class ConsoleWidget(RichJupyterWidget, QThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font_size = 12
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel(show_banner=False)
        kernel_manager.kernel.gui = 'qt'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()
            sys.exit()

        self.exit_requested.connect(stop)

    def push_vars(self, variableDict):
        """
        Given a dictionary containing name / value pairs, push those variables
        to the Jupyter console widget
        """
        self.kernel_manager.kernel.shell.push(variableDict)

    def clear(self):
        """
        Clears the terminal
        """
        self._control.clear()

        # self.kernel_manager

    def print_text(self, text):
        """
        Prints some plain text to the console
        """
        self._append_plain_text(text)

    def execute_command(self, command):
        """
        Execute a command in the frame of the console widget
        """
        self._execute(command, False)


class MessageBox(QWidget, QObject):
    def __init__(self, error=None, helpword=None, index=choiceIndex):
        super().__init__()
        self.helpword = helpword
        self.layout = QHBoxLayout(self)

        self.index = str(index)
        self.screen_geomtery = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.width = self.screen_geomtery.width() 
        self.height = self.screen_geomtery.height()
        self.path = None
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
        self.saveButton = QPushButton("Save")

        self.deleteButton.clicked.connect(self.delete)
        self.cancel.clicked.connect(self.dont)
        self.button.clicked.connect(self.dont)
        self.getHelpButton.clicked.connect(self.gettingHelp)
        
        self.saved = None
        
        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)

        self.setFont(self.font)
        
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

        self.label.setText("Theme " + str(index) + " selected\nNOTE: For some changes to work you need to restart PyPad")
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
                print(E)
        
        def _hide():
                self.hide()
                    
        self.label.setText("Warning, you have unsaved changes!")
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
        webbrowser.open(self.url)
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
                print(E)
                
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
                
    def getHelp(self):

        try:
            self.layout.removeWidget(self.deleteButton)
            self.layout.removeWidget(self.button)

        except AttributeError as E:
            print(E)
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


class Directory(QTreeView):
    def __init__(self, callback):
        super().__init__()

        directoryFont = QFont()
        directoryFont.setFamily(editor["directoryFont"])
        directoryFont.setPointSize(editor["directoryFontSize"])
        self.open_callback = callback
        self.setFont(directoryFont)
        self.layout = QHBoxLayout()
        self.model = QFileSystemModel()
        self.setModel(self.model)
        self.model.setRootPath(QDir.rootPath())
        self.setMaximumWidth(300)
        self.setIndentation(10)
        self.setAnimated(True)

        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")
        self.hideColumn(1)
        self.resize(200, 600)
        self.hideColumn(2)
        self.confirmation = MessageBox()
        self.hideColumn(3)
        # self.layout.addWidget(self)
        self.doubleClicked.connect(self.openFile)

    def focusInEvent(self, event):
        # If we are focused then we change the selected item highlighting color
        self.focused = True
        palette.setColor(QPalette.Highlight, QColor(editor["HighlightColor"]).lighter())

        app.setPalette(palette)

    def focusOutEvent(self, event):
        # If we un focus from the QTreeView then we make the highlighted item color white
        palette.setColor(QPalette.Highlight, QColor(editor["UnfocusedHighlightColor"]).lighter())
        # self.clearSelection() Uncomment this if you want to remove all highlighting when unfocused
        app.setPalette(palette)

    def openDirectory(self, path):
        self.setRootIndex(self.model.index(path))

    def openFile(self, signal):
        file_path = self.model.filePath(signal)
        self.open_callback(file_path)
        return file_path

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:

            try:
                self.fileObject = self.selectedIndexes()[0]
                fileName = self.model.filePath(self.fileObject)
                self.confirmation.run("Are you sure you want to delete ", str(fileName))

            except IndexError:
                print("No file selected")


class Completer(QCompleter):
    insertText = pyqtSignal(str)

    def __init__(self, myKeywords=None, parent=None):
        self.wordList = wordList
        QCompleter.__init__(self, myKeywords, parent)
        
        self.activated.connect(self.changeCompletion)

    def changeCompletion(self, completion):

        self.insertText.emit(completion)


class Image(QWidget):

    def __init__(self, fileName, baseName):
        super().__init__()
        self.baseName = baseName
        self.fileName = fileName

        self.image = QPixmap(self.fileName)
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.image)


class Content(QWidget):
    def __init__(self, text, fileName, baseName, themeIndex, parent):
        super().__init__()
        self.editor = PlainTextEdit(self)
        self.text = text
        self.parent = parent
        self.wordlist = wordList
        self.fileName = fileName
        self.baseName = baseName
        self.temporary = 0
        self.font = QFont()
        self.custom = Customize()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])
        self.tabSize = editor["TabWidth"]
        self.editor.textChanged.connect(self.changeSaved)
        self.custom = Customize()
        self.saved = True
        self.editor.setPlainText(str(text))
        
        if self.baseName.endswith(".py"):
            self.highlighter = PyHighlighter(self.editor.document(), index=self.custom.index)
            self.tokenize_file()
        else:
            pass

        self.hbox = QHBoxLayout(self)
        self.vbox = QVBoxLayout()
        # Create a widget for the line numbers
        self.numbers = NumberBar(self.editor, index=themeIndex)
        self.hbox.addWidget(self.numbers)
        self.hbox.addWidget(self.editor)
        self.completer = Completer(self.wordlist)
        self.moveCursorRight = QShortcut(QKeySequence(editor["moveCursorRight"]), self)
        self.moveCursorLeft = QShortcut(QKeySequence(editor["moveCursorLeft"]), self)
        self.selectAllBeforeCursor = QShortcut(QKeySequence(editor["selectAllWordsBeforeCursor"]), self)
        self.moveUp = QShortcut(QKeySequence(editor["moveCursorUp"]), self)
        self.moveDown = QShortcut(QKeySequence(editor["moveCursorDown"]), self)
        
        self.moveDown.activated.connect(self.moveCursorDown)
        self.moveUp.activated.connect(self.moveCursorUp)
        self.selectAllBeforeCursor.activated.connect(self.selectBeforeCursor)
        self.moveCursorRight.activated.connect(self.moveCursorRightFunc)
        self.moveCursorLeft.activated.connect(self.moveCursorLeftFunc)
        self.editor.textChanged.connect(self.changeSaved)
        self.setCompleter(self.completer)
        
    def tokenize_file(self):

        for i in tokenize(self.fileName):
            for j in i:
                if j not in self.wordlist:
                    self.wordlist.append(j)
                    self.completer = Completer(self.wordlist)
                    self.setCompleter(self.completer)
                        
    def getTextCursor(self):
        textCursor = self.editor.textCursor()
        textCursorPos = textCursor.position()
        
        return textCursor, textCursorPos
         
    def changeSaved(self):
        
        self.modified = self.editor.document().isModified()
        
        try:
            if self.modified:
                ex.setWindowTitle("PyPad ~ " + str(self.baseName) + " [UNSAVED]")
            else:
                pass
                    
        except NameError as E:
            print(E)
                
    def moveCursorRightFunc(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.setPosition(textCursorPos + 1)
        self.editor.setTextCursor(textCursor)
        
    def moveCursorUp(self):
        textCursor, textCursorPos = self.getTextCursor()
        
        textCursor.movePosition(textCursor.Up)
        self.editor.setTextCursor(textCursor)    
        
    def moveCursorDown(self):
        textCursor, textCursorPos = self.getTextCursor()
        
        textCursor.movePosition(textCursor.Down)
        self.editor.setTextCursor(textCursor)    
        
    def moveCursorLeftFunc(self):
        textCursor, textCursorPos = self.getTextCursor()

        textCursor.setPosition(textCursorPos - 1)
        self.editor.setTextCursor(textCursor)
        
    def selectBeforeCursor(self):
        textCursor, textCursorPos = self.getTextCursor()
        text = self.textUnderCursor()
        
        textCursor.movePosition(textCursor.StartOfWord, textCursor.KeepAnchor, len(text))
        self.editor.setTextCursor(textCursor)
        
    def setCompleter(self, completer):

        self.completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = completer

        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        textCursor = self.editor.textCursor()

        extra = (len(completion) - len(self.completer.completionPrefix()))
        
        textCursor.movePosition(QTextCursor.Left)
        textCursor.movePosition(QTextCursor.EndOfWord)
        textCursor.insertText(completion[-extra:])

        if completion.endswith("()"):
            cursorPos = textCursor.position()
            textCursor.setPosition(cursorPos - 1)

        self.editor.setTextCursor(textCursor)

    def textUnderCursor(self):
        textCursor = self.editor.textCursor()
        textCursor.select(QTextCursor.WordUnderCursor)

        return textCursor.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
            QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return
        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_Space)

        if not self.completer or not isShortcut:

            QPlainTextEdit.keyPressEvent(self.editor, event)

        completionPrefix = self.textUnderCursor()

        if not isShortcut:
            if self.completer.popup():
                self.completer.popup().hide()
            return
        self.completer.setCompletionPrefix(completionPrefix)

        popup = self.completer.popup()
        popup.setFont(self.font)
        popup.setCurrentIndex(
            self.completer.completionModel().index(0, 0))

        cr = self.editor.cursorRect()
        cr.translate(QPoint(10, 10))
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)


class Customize(QWidget, QObject):
    def __init__(self):
        super().__init__()

        self.setFixedSize(800, 600)
        with open("default.json", "r") as selectedIndex:
            self.index = selectedIndex.read()
            if self.index == "":
                self.index = 0

            selectedIndex.close()
        self.conf = MessageBox()
        self.opened = False
        self.vbox = QVBoxLayout(self)  # Creating the layout

        self.setWindowIcon(QIcon('resources/Python-logo-notext.svg_.png'))

        self.initUI()

    def initUI(self):

        self.LayoutImage = QLabel(self)
        self.LayoutText = QLabel(self)

        self.hbox = QHBoxLayout()

        editor = config0['editor']

        self.font = QFont()
        self.font.setFamily(editor["editorFont"])
        self.font.setPointSize(editor["editorFontSize"])

        self.combo = QComboBox(self)
        self.combo.addItem("Theme 1")
        self.combo.addItem("Theme 2")
        self.combo.addItem("Theme 3")
        self.combo.currentIndexChanged.connect(self.themes)
        self.combo.setFont(self.font)

        self.theme1 = QPixmap('resources/layout1.png')  # These are the pictures of themes
        self.theme2 = QPixmap('resources/layout1.png')
        self.theme3 = QPixmap('resources/layout1.png')

        self.vbox.addWidget(self.combo)  # Adding Combobox to vertical boxlayout so it would look better

        self.LayoutText.setFont(self.font)

        self.hbox.addWidget(self.LayoutText)
        self.hbox.addWidget(self.LayoutImage)

        self.LayoutImage.setPixmap(self.theme1)  # This is the "main" theme
        self.LayoutImage.resize(415, 287)

        self.LayoutText.setText("Dark theme")

        self.vbox.addLayout(self.hbox)

        self.selector = QPushButton(self)
        self.selector.setFixedSize(100, 30)
        self.selector.setLayoutDirection(Qt.RightToLeft)
        self.selector.setText("Select")
        self.selector.setFont(self.font)

        self.vbox.addWidget(self.selector)
        self.setLayout(self.vbox)

    def run(self):
        self.show()

    def themes(self, index):

        if index == 0:
            self.LayoutImage.setPixmap(self.theme1)
            self.LayoutText.setText("Dark theme")

        elif index == 1:

            self.LayoutImage.setPixmap(self.theme3)
            self.LayoutText.setText("Fancy theme")

        elif index == 2:

            self.LayoutImage.setPixmap(self.theme2)
            self.LayoutText.setText("Light theme")

        else:
            pass

    def test(self):
        index = self.combo.currentIndex()
        self.index = str(index)
        self.conf.confirmation(index+1)
        with open("default.json", "w+") as write:
            write.write(str(self.index))
            write.close()
        if index == 0:
            editor = config0['editor']
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

        elif index == 1:
            editor = config1['editor']
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

        elif index == 2:
            editor = config2['editor']
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


class Tabs(QWidget):

    def __init__(self, callback):
        super().__init__()

        self.layout = QHBoxLayout(self)  # Change main layout to Vertical
        # Initialize tab screen
        self.tabs = QTabWidget()  # TODO: This is topright
        font = QFont(editor['tabFont'])
        font.setPointSize(editor["tabFontSize"])  # This is the tab font and font size
        self.tabs.setFont(font)
        
        self.dialog = MessageBox()
        self.tabs.usesScrollButtons()
        self.filelist = []
        
        self.tabSaved = False
        
        self.Console = Console()  # This is the terminal widget and the SECOND thread
        self.term = ConsoleWidget()
        self.directory = Directory(callback)  # TODO: This is top left
        self.directory.clearSelection()
        self.tabCounter = []
        # Add tabs
        self.tab_layout = QHBoxLayout()  # Create new layout for original tab layout
        self.tab_layout.addWidget(self.tabs)  # Add tab widget to tab layout
        self.search_layout = QHBoxLayout()

        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(editor['tabMovable'])  # Let's you make the tabs movable

        if editor['tabShape'] is True:  # If tab shape is true then they have this rounded look
            self.tabs.setTabShape(1)

        else:
            self.tabs.setTabShape(0)  # If false, it has this boxy look

        self.tabs.tabCloseRequested.connect(self.closeTab)

        # Add Console
        self.console_layout = QHBoxLayout()  # Create console layout
        self.console_layout.addWidget(self.term)  # Add console to console layout

        # Build Layout
        self.layout.addLayout(self.tab_layout)  # Adds 'TOP' layout : tab + directory
        self.layout.addLayout(self.search_layout)

        # Creating horizontal splitter
        self.splitterH = QSplitter(Qt.Horizontal)

        # Creating vertical splitter
        self.splitterV = QSplitter(Qt.Vertical)
        self.splitterV.addWidget(self.splitterH)
        self.layout.addWidget(self.splitterV)
        self.splitterV.setSizes([300, 10])
        self.setLayout(self.layout)  # Sets layout of QWidget

        self.closeShortcut = QShortcut(QKeySequence(editor["closeTabShortcut"]), self)
        self.closeShortcut.activated.connect(self.closeTabShortcut)
        
        self.getAllOpenTabs = QShortcut(QKeySequence("Ctrl+Shift+W"), self)
        self.getAllOpenTabs.activated.connect(self.getAllOpenTabsFunc)
        
        currentTab = self.tabs.currentWidget()
        self.hideDirectory()
        """
    def hideDirectory(self):
        self.tab_layout.removeWidget(self.directory)
        self.directory.setVisible(False)"""

    @pyqtSlot()
    def closeTabShortcut(self):
        self.index = self.tabs.currentIndex()
        self.closeTab(self.index)
        
    def getAllOpenTabsFunc(self):
        word = 'import'
        for tab in range(self.tabs.count()):
            file = self.tabs.widget(tab).fileName
            if file not in self.filelist:
                self.filelist.append(file)
                
        for file in self.filelist:
            openedFileContents = open(file, 'r').read()
        
    def closeTab(self, index):
        try:
           
            tab = self.tabs.widget(index)
            
            if tab.saved is True and tab.modified is False:
                tab.deleteLater()
                self.tabCounter.pop(index)
                self.filelist.pop(index)
                self.tabs.removeTab(index)
                
            elif tab.modified is True:
                self.dialog.saveMaybe(tab, self.tabCounter, self.tabs, index)
                
        except (AttributeError, IndexError) as E:
            try:
                tab.deleteLater()
                self.tabCounter.pop(index)
                self.filelist.pop(index)
                self.tabs.removeTab(index)
            except (AttributeError, IndexError) as E:
                print(E)
                
    def showDirectory(self):
        self.directory.setVisible(True)
        self.tab_layout.removeWidget(self.tabs)
        self.splitterH.addWidget(self.directory)  # Adding that directory widget in the Tab class BEFORE the tabs
        self.splitterH.addWidget(self.tabs)  # Adding tabs, now the directory tree will be on the left

    def hideDirectory(self):
        self.tab_layout.removeWidget(self.directory)
        self.directory.setVisible(False)

    """
    Because the root layouts are set all you have to do now is just add/remove widgets from the parent layout associated.
    This keeps the UI order set as intended as built above when initialized.
    """

    def showConsole(self):
        pass

    def currentTab(self):
        return self.tabs.currentWidget()


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.onStart(choiceIndex)
        self.custom = Customize()
        # Initializing the main widget where text is displayed
        self.tab = Tabs(self.openFile)
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
        self.search = documentSearch()
        self.os = sys.platform
        self.openPy()
        self.openTerm()
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
            currentFileDocument = self.tab.tabs.currentWidget().editor.document()

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
        self.statusBar()  # Initializing the status bar

        self.font.setFixedPitch(True)
        menuFont = QFont()
        menuFont.setFamily(editor["menuFont"])
        menuFont.setPointSize(editor['menuFontSize'])
        menu = self.menuBar()
        menu.setFont(menuFont)
        # Creating the file menu

        fileMenu = menu.addMenu('File')

        # Adding options to the file menu

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
        
    def openPy(self):
        self.openPyAct = QAction('IPython console', self)
        self.openPyAct.setShortcut('Ctrl+Y')

        self.openPyAct.setStatusTip('Open IPython console')
        self.openPyAct.triggered.connect(self.Console)

    def openTerm(self):
        self.openTermAct = QAction('Run', self)
        self.openTermAct.setShortcut('Shift+F10')

        self.openTermAct.setStatusTip('Run your code')
        self.openTermAct.triggered.connect(self.Terminal)

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
                        tab = Content(text, filename, basename, self.custom.index, self)  # Creating a tab object *IMPORTANT*
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
                tab = Content(text, filename, basename, self.custom.index, self)  # Creating a tab object *IMPORTANT*
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
        file = Content(text, fileName, fileName, self.custom.index, self)

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
                    newTab = Content(str(text), fileName, baseName, self.custom.index, self)

                    self.tab.tabs.removeTab(active_index)  # When user changes the tab name we make sure we delete the old one
                    index = self.tab.tabs.addTab(newTab, newTab.fileName)  # And add the new one!

                    self.tab.tabs.setCurrentIndex(index)
                    newActiveTab = self.tab.tabs.currentWidget()

                    newActiveTab.editor.setFont(self.font)
                    newActiveTab.editor.setFocus()

                    if fileName.endswith(".py"):  # If we are dealing with a python file we use highlighting on it
                        self.pyhighlighter = PyHighlighter(newActiveTab.editor.document(), index=self.custom.index)

                        newActiveTab.editor.setTabStopWidth(self.tabSize)
                    elif fileName.endswith(".c"):

                        self.chighlighter = CHighlighter(newActiveTab.editor.document())
                        newActiveTab.editor.setTabStopWidth(self.tabSize)

                    saveFile.close()
                ex.setWindowTitle("PyPad ~ " + str(active_tab.baseName) + " [SAVED]")

            else:
                print("No file opened")

        except FileNotFoundError:
            print("File dialog closed")

    def Console(self):

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

    def Terminal(self):

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


class CHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, *args):
        super(CHighlighter, self).__init__(parent, *args)

        python = config['files']['c']

        self.highlightingRules = []
        self.formats = {}

        self.regex = {
            "class": "\\bclass\\b",
            "function": "[A-Za-z0-9_]+(?=\\()",
            "magic": "\\__[^']*\\__",
            "decorator": "@[^\n]*",
            "quotation": "\"[^\"]*\"",

            "singleLineComment": "#[^\n]*",
            "multiLineComment": "[-+]?[0-9]+",
            "int": "[-+]?[0-9]+",
        }

        cKeywordPatterns = ["auto", "break", "case", "char", "const", "const", "continue", "default", "do", "double", "else",
        "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof",
        "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(python['highlighting']['keyword']['color']))
        keywordFormat.setFontWeight(QFont.Bold)

        self.highlightingRules = [(QRegExp('\\b' + pattern + '\\b'), keywordFormat) for pattern in cKeywordPatterns]

        for name, values in self.regex.items():
            self.formats[name] = QTextCharFormat()

            if name == "class":
                self.formats[name].setFontWeight(QFont.Bold)

            elif name == "function":
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
    if True: # checkVersion("version.txt") != checkVerOnlineFunc():
        pass  # TODO: implement an updater
    else:
        print("Up to date")

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
