from PyQt5.QtWidgets import QHBoxLayout, QWidget, QStyle, QStyleOptionViewItem, QApplication
from PyQt5.QtCore import QRect, QRectF, QPointF, Qt, QEvent
from PyQt5.QtGui import QPaintEvent, QTextBlock, QPainter, QColor, QMouseEvent, QCursor
from PyQt5.QtTest import QTest
from Hydra.widgets.Editor import Editor
import re

FOLDED_STATE = -1
UNFOLDED_STATE = 0
FOLDING_PATTERN = "\\s*(def|class|with|if|else|elif|for|while|async).*:"


class FoldArea(QWidget):
    def __init__(self, editor: Editor):
        super(FoldArea, self).__init__()

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
        self.setFixedWidth(space)

    def updateOnScroll(self, rect: QRect, scroll: int):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def mousePressEvent(self, event: QMouseEvent):

        pattern = re.compile(FOLDING_PATTERN)
        blockedClickedOn: QTextBlock = self.getBlockUnderCursor(event)

        if pattern.match(blockedClickedOn.text()):

            if blockedClickedOn.userState() == 0:  # block and its contents are unfolded

                self.fold(blockedClickedOn)

            else:

                self.unfold(blockedClickedOn)

    def unfold(self, block: QTextBlock):

        foldableBlocks: list = self.editor.getFoldableBlocks(block)

        for foldableBlock in foldableBlocks:

            foldableBlock.setVisible(True)

            self.editor.document().markContentsDirty(block.position(), foldableBlock.position())

        block.setUserState(UNFOLDED_STATE)

    def fold(self, block: QTextBlock):

        foldableBlocks: list = self.editor.getFoldableBlocks(block)

        for foldableBlock in foldableBlocks:

            foldableBlock.setVisible(False)
            self.editor.document().markContentsDirty(block.position(), foldableBlock.position())

        block.setUserState(FOLDED_STATE)  # blocks are now in a "folded" state

    def getBlockUnderCursor(self, event: QMouseEvent) -> QTextBlock:

        height = self.editor.fontMetrics().height()
        y = event.pos().y()

        for array in self.editor.currentlyVisibleBlocks:

            if array[0] < y < height + array[0]:

                return array[1]

    def paintEvent(self, event: QPaintEvent):

        if self.isVisible():

            block: QTextBlock = self.editor.firstVisibleBlock()
            height: int = self.fontMetrics().height()
            number: int = block.blockNumber()

            painter = QPainter(self)
            painter.fillRect(event.rect(), QColor(53, 53, 53))
            font = painter.font()
            font.setPointSize(15)

            for blocks in self.editor.currentlyVisibleBlocks:

                bl: QTextBlock = blocks[-1]
                blockGeometry: QRectF = self.editor.blockBoundingGeometry(bl)
                offset: QPointF = self.editor.contentOffset()
                blockTop: int = int(blockGeometry.translated(offset).top() + 1)
                pattern = re.compile(
                    "\\s*(def|class|with|if|else|elif|for|while|async).*:")
                if pattern.match(bl.text()):

                    options = QStyleOptionViewItem()
                    options.rect = QRect(0, blockTop, self.width(), height)
                    options.state = (QStyle.State_Active |
                                     QStyle.State_Item |
                                     QStyle.State_Children)

                    if bl.userState() == UNFOLDED_STATE:
                        options.state |= QStyle.State_Open

                    self.style().drawPrimitive(QStyle.PE_IndicatorBranch, options,
                                               painter, self)
            painter.end()

    def leaveEvent(self, event: QEvent) -> None:

        self.returnCursorToNormal()

    def returnCursorToNormal(self) -> None:

        cursor: QCursor = QCursor(Qt.ArrowCursor)
        QApplication.setOverrideCursor(cursor)
        QApplication.changeOverrideCursor(cursor)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:

        pattern = re.compile(FOLDING_PATTERN)
        block: QTextBlock = self.editor.getBlockUnderCursor(event)

        if pattern.match(block.text()):

            cursor: QCursor = QCursor(Qt.PointingHandCursor)
            QApplication.setOverrideCursor(cursor)
            QApplication.changeOverrideCursor(cursor)

        else:

            self.returnCursorToNormal()
