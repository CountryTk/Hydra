import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class terminal(QWidget):

    def __init__(self):
        super().__init__()
        self.process = QProcess(self)

        self.terminal = QWidget()
        print(self.terminal.width())
        self.terminal.setMinimumWidth(782)
        self.terminal.setMinimumHeight(160)
        # Works also with urxvt:
        self.layout = QGridLayout()
        self.process.start(
                'xterm', ['-into', str(int(self.terminal.winId()))])
        self.layout.setColumnStretch(1, 5)
        self.layout.addWidget(self.terminal, 1, 1)
        self.setLayout(self.layout)

