from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap


class Image(QWidget):

    def __init__(self, fileName, baseName):
        super().__init__()
        self.baseName = baseName
        self.fileName = fileName

        self.image = QPixmap(self.fileName)
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(self.image)
