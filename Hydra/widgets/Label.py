from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont


class StatusLabel(QLabel):

    def __init__(self, text: str, font: QFont):

        super().__init__()

        self.setText(text)
        self.setFont(font)
