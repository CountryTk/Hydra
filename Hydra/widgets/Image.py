from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap


class Image(QWidget):
    def __init__(self, fileName, baseName):
        super().__init__()
        self.baseName = baseName
        self.fileName = fileName

        self.image = QPixmap(self.fileName)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)

        self.layout = QHBoxLayout()

        self.layout.addWidget(self.imageLabel)
        self.setLayout(self.layout)
