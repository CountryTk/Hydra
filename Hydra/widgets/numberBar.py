from PyQt5.QtWidgets import QHBoxLayout, QWidget, QStyle, QStyleOptionViewItem
from PyQt5.QtCore import QRect, QRectF, QPointF, Qt
from PyQt5.QtGui import QPaintEvent, QTextBlock, QPainter, QColor, QMouseEvent
from PyQt5.QtTest import QTest
from Hydra.widgets.Editor import Editor
import re

FOLDED_STATE = 1
UNFOLDED_STATE = 0


class NumberBar(QWidget):
    def __init__(self, editor: Editor):
        super(NumberBar, self).__init__()

        self.editor = editor
        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.updateRequest.connect(self.updateOnScroll)
        self.updateWidth(0)
        self.setMouseTracking(True)

    def updateWidth(self, blockCount: int):
        digits = 1
        max_value = max(1, self.editor.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 10 + self.fontMetrics().width("9") * digits
        space += 8
        self.setFixedWidth(space)

    def updateOnScroll(self, rect: QRect, scroll: int):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def setFoldLines(self, lines: dict):
        self.lines = lines
        print(self.lines)

    def mousePressEvent(self, event: QMouseEvent):
        pass

    def getBlockUnderCursor(self, event: QMouseEvent) -> QTextBlock:
        height = self.editor.fontMetrics().height()
        y = event.pos().y()
        for array in self.editor.currentlyVisibleBlocks:
            print(array[0], y, height+array[0])
            if array[0] < y < height + array[0]:

                return array[1]

    def paintEvent(self, event: QPaintEvent):
        if self.isVisible():
            block: QTextBlock = self.editor.firstVisibleBlock()
            height: int = self.fontMetrics().height()
            number: int = block.blockNumber()

            painter = QPainter(self)
            painter.fillRect(event.rect(), QColor(53, 53, 53))
            # painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()
            font.setPointSize(15)
            for blocks in self.editor.currentlyVisibleBlocks:
                bl: QTextBlock = blocks[-1]
                blockGeometry: QRectF = self.editor.blockBoundingGeometry(bl)
                offset: QPointF = self.editor.contentOffset()
                blockTop: float = float(blockGeometry.translated(offset).top() + 2)
                rect: QRect = QRect(0, blockTop, self.width(), height)
                painter.drawText(rect, Qt.AlignRight, str(bl.blockNumber() + 1))

            painter.end()