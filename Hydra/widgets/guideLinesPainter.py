
from PyQt5.QtGui import QPainter, QColor, QPaintEvent
from PyQt5.QtCore import Qt
from Hydra.widgets.Editor import Editor


class guideLines:

    def __init__(self, editor: Editor):

        self.editor = editor
        self.guideLineColor = QColor(Qt.red)
        self.guideLineColor.setAlpha(0.25)

        self.editor.updateRequest.connect(self.editor.viewport().update)
        self.editor.painted.connect(self.drawLines)

    def drawLines(self, event: QPaintEvent):
        pass
