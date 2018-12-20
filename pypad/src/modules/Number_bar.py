from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget
from src.config import config

config0 = config.read(0)
config1 = config.read(1)
config2 = config.read(2)

with open("default.json") as choice:
    choiceIndex = int(choice.read())


class NumberBar(QWidget):
    def __init__(self, parent=None, index=choiceIndex):
        super().__init__(parent)
        self.editor = parent
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')
        self.line_bar_color =QColor(153, 153, 153)
        self.index = index

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 28
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.index == "0":
            config = config0
        elif self.index == "1":
            config = config1
        elif self.index == "2":
            config = config2
        else:

            config = config0
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QPainter(self)
            painter.fillRect(event.rect(), self.lineBarColor)
            if config['editor']['NumberBarBox'] is True:
                painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)

            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            while block.isValid():
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1
                rect = QRect(0, block_top, self.width() - 5, height)

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
