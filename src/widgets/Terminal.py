import sys
from builtins import print, property

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import getpass
import socket
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QRegExp

lineBarColor = QColor(53, 53, 53)


class PlainTextEdit(QPlainTextEdit):
    commandSignal = pyqtSignal(str)
    commandZPressed = pyqtSignal(str)

    def __init__(self, parent=None, movable=False):
        super().__init__(parent)

        self.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
            os.getcwd()) + " >$ "
        self.appendPlainText(self.name)
        self.movable = movable
        self.parent = parent
        self.setStyleSheet("QPlainTextEdit{background-color: black; color: white; padding: 0;}")
        self.font = QFont()
        self.font.setFamily("Iosevka")
        self.font.setPointSize(12)
        self.setFont(self.font)
        self.document_file = self.document()
        self.document_file.setDocumentMargin(-1)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        if self.movable is True:
            self.parent.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.movable is True:
            self.parent.mouseMoveEvent(event)

    def keyPressEvent(self, e):
        cursor = self.textCursor()

        if self.parent:

            if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_A:
                return

            if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Z:
                self.commandZPressed.emit("True")
                return

            if e.key() == 16777220:
                text = self.textCursor().block().text()
                self.commandSignal.emit(text)
                self.appendPlainText(self.name)
                print("Command sent: " + str(text))

                return

            if e.key() == 16777219:
                if cursor.positionInBlock() <= len(self.name):
                    return

                else:
                    cursor.deleteChar()

            super().keyPressEvent(e)

        e.accept()


class Terminal(QWidget):
    errorSignal = pyqtSignal(str)
    outputSignal = pyqtSignal(str)

    def __init__(self, movable=False):
        super().__init__()

        self.setWindowFlags(
            Qt.Widget |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )
        self.movable = movable
        self.layout = QVBoxLayout()
        # self.button = QPushButton("Click me")
        self.pressed = False
        self.process = QProcess(self)
        # self.editor = PlainTextEdit(self, self.movable)

        self.name = None

       # self.layout.addWidget(self.editor)
       # self.layout.addWidget(self.button)

        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.setLayout(self.layout)
        self.setStyleSheet("QWidget {background-color:invisible;}")

        # self.showMaximized() # comment this if you want to embed this widget

    def ispressed(self):
        return self.pressed

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def add(self):
        self.added()
        self.button = QPushButton("Hide terminal")
        self.button.setStyleSheet("""
        height: 20;
        """)
        self.button.setFixedWidth(100)
        self.editor = PlainTextEdit(self, self.movable)
        self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()), str(socket.gethostname()),
                                            str(os.getcwd()))
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.editor)
        self.editor.commandSignal.connect(self.handle)
        self.button.clicked.connect(self.remove)
        self.editor.commandZPressed.connect(self.handle)

    def added(self):
        self.pressed = True

    def remove(self):
        self.editor.deleteLater()
        self.button.deleteLater()
        self.pressed = False

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def onReadyReadStandardError(self):
        self.error = self.process.readAllStandardError().data().decode()
        self.editor.appendPlainText(self.error.strip('\n'))
        self.errorSignal.emit(self.error)

    def onReadyReadStandardOutput(self):
        self.result = self.process.readAllStandardOutput().data().decode()
        self.editor.appendPlainText(self.result.strip('\n'))
        self.state = self.process.state()
        self.outputSignal.emit(self.result)

    def run(self, command):
        """Executes a system command."""
        if self.process.state() != 2:
            self.process.start(command)
            print("Command executed, process state is now: " + str(self.process.state()))

    def handle(self, command):

        """Split a command into list so command echo hi would appear as ['echo', 'hi']"""
        real_command = command.replace(self.editor.name, "")

        if command == "True":
            if self.process.state() == 2:
                self.process.kill()
                self.editor.appendPlainText("Program execution killed, press enter")
        if real_command.startswith("python"):
            # TODO: start a python thread....
            pass

        if real_command != "":
            command_list = real_command.split()
        else:
            command_list = None
        """Now we start implementing some commands"""
        if real_command == "clear":
            self.editor.clear()

        elif "&&" in command_list:
            pass
            # print(command_list)
            # print(command_list.index("&&"))
            # print(command_list[command_list.index("&&")+1:])

        elif command_list is not None and command_list[0] == "echo":
            self.editor.appendPlainText(" ".join(command_list[1:]))

        elif real_command == "exit":
            qApp.exit()

        elif command_list is not None and command_list[0] == "cd" and len(command_list) > 1:
            try:
                os.chdir(" ".join(command_list[1:]))
                self.editor.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
                    os.getcwd()) + " >$ "
                if self.highlighter:
                    del self.highlighter
                self.highlighter = name_highlighter(self.editor.document(), str(getpass.getuser()),
                                                    str(socket.gethostname()), str(os.getcwd()))

            except FileNotFoundError as E:
                self.editor.appendPlainText(str(E))

        elif len(command_list) == 1 and command_list[0] == "cd":
            os.chdir(str(Path.home()))
            self.editor.name = "[" + str(getpass.getuser()) + "@" + str(socket.gethostname()) + "]" + "  ~" + str(
                os.getcwd()) + " >$ "

        elif self.process.state() == 2:
            self.process.write(real_command.encode())
            self.process.closeWriteChannel()

        elif command == self.editor.name + real_command:
            self.run(real_command)

        else:
            pass  # When the user does a command like ls and then presses enter then it wont read the line where the cursor is on as a command


class name_highlighter(QSyntaxHighlighter):

    def __init__(self, parent=None, user_name=None, host_name=None, cwd=None):
        super().__init__(parent)
        self.highlightingRules = []
        self.name = user_name
        self.name2 = host_name
        self.cwd = cwd
        # print(self.cwd)
        first_list = []
        most_used = ["cd", "clear", "history", "ls", "man", "pwd", "what", "type",
                     "strace", "ltrace", "gdb", "cat", "chmod", "cp", "chown", "find", "grep", "locate", "mkdir",
                     "rmdir", "rm", "mv", "vim", "nano", "rename",
                     "touch", "wget", "zip", "tar", "gzip", "apt", "bg", "fg", "df", "free", "ip", "jobs", "kill",
                     "killall", "mount", "umount", "ps", "sudo", "echo",
                     "top", "uname", "whereis", "uptime", "whereis", "whoami", "exit"
                     ]  # most used linux commands, so we will highlight them!
        self.regex = {
            "class": "\\bclass\\b",
            "function": "[A-Za-z0-9_]+(?=\\()",
            "magic": "\\__[^']*\\__",
            "decorator": "@[^\n]*",
            "singleLineComment": "#[^\n]*",
            "quotation": "\"[^\"]*\"",
            "quotation2": "'[^\']*\'",
            "multiLineComment": "[-+]?[0-9]+",
            "int": "[-+]?[0-9]+",
        }
        """compgen -c returns all commands that you can run"""

        for f in most_used:
            nameFormat = QTextCharFormat()
            nameFormat.setForeground(QColor("#00ff00"))
            nameFormat.setFontItalic(True)
            self.highlightingRules.append((QRegExp("\\b" + f + "\\b"), nameFormat))

        hostnameFormat = QTextCharFormat()
        hostnameFormat.setForeground(QColor("#12c2e9"))
        self.highlightingRules.append((QRegExp(self.name), hostnameFormat))
        self.highlightingRules.append((QRegExp(self.name2), hostnameFormat))

        otherFormat = QTextCharFormat()
        otherFormat.setForeground(QColor("#f7797d"))
        self.highlightingRules.append((QRegExp("~\/[^\s]*"), otherFormat))

        quotation1Format = QTextCharFormat()
        quotation1Format.setForeground(QColor("#96c93d"))
        self.highlightingRules.append((QRegExp("\"[^\"]*\""), quotation1Format))

        quotation2Format = QTextCharFormat()
        quotation2Format.setForeground(QColor("#96c93d"))
        self.highlightingRules.append((QRegExp("'[^\']*\'"), quotation2Format))

        integerFormat = QTextCharFormat()
        integerFormat.setForeground(QColor("#cc5333"))
        integerFormat.setFontItalic(True)
        self.highlightingRules.append((QRegExp("\\b[-+]?[0-9]+\\b"), integerFormat))

    def highlightBlock(self, text):

        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class PythonThread(QThread):

    def __init__(self):
        super().__init__()

        print("test")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Terminal(True)
    sys.exit(app.exec_())
