from PyQt5.QtCore import pyqtSignal, Qt, QProcess
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


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
