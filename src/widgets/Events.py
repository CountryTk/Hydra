from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
import io
from contextlib import redirect_stdout
from vulture.core import Vulture
from PyQt5.QtGui import QFont


class Events(QWidget):

    def __init__(self, text=None, file_name=None):
        super().__init__()

        self.dead_code = None

        self.info_bar = QTextEdit()
        self.font = QFont("Iosevka", 11)
        self.label = QLabel("Events")
        self.info_bar.setFont(self.font)
        self.buttons_layout = QHBoxLayout()
        self.layout = QVBoxLayout(self)
        self.info_bar.setReadOnly(True)
        self.layout.addLayout(self.buttons_layout)
        self.buttons_layout.addWidget(self.label)
        self.layout.addWidget(self.info_bar)
        self.setStyleSheet("""
        
        background-color: transparent;
        
        """)

    def look_for_dead_code(self, text):
        self.vultureObject = Vulture()
        self.vultureObject.scan(text)

        with io.StringIO() as buf, redirect_stdout(buf):
            self.vultureObject.report()
            output = buf.getvalue()

        info = output.replace(':', '').split()
        formatted_info = []
        unformatted_info = []
        for word in info:
            try:
                integer = int(word)
                new_word = "<h5 style=\"color: #78ffd6; \">Line {} </h5>".format(integer)
                formatted_info.append("\n")
                formatted_info.append(new_word)
                unformatted_info.append("\n")
                unformatted_info.append("Line {}".format(integer))
            except ValueError:
                formatted_info.append("<font color=#dd3e54>" + word + "</font>")
                unformatted_info.append(word)

        self.dead_code = " ".join(formatted_info)
        self.info_bar.setText(self.dead_code)
