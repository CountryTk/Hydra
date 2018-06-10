#! /usr/bin/env python

# Copyright (C) 2018 AnonymousDapper & Fuchsiaff

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os

import argparse

import yaml

import pygments, pygments.lexers

from pygments.formatter import Formatter

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

from resources.main_window import Ui_MainWindow

parser = argparse.ArgumentParser(description="Simplistic text editor written in python")

parser.add_argument("filenames", action="append", nargs="*", type=str)

launch_args = parser.parse_args()

class QtHtmlFormatter(Formatter):
    def __init__(self, style, **kwargs):
        super().__init__(**kwargs)

        self.stylesheet = style

    def _get_class_name(self, token):
        while not token in pygments.token.STANDARD_TYPES:
            token = token.parent

        return pygments.token.STANDARD_TYPES[token]

    def __call__(self, tokens):
        lines = []
        for name, source in tokens:
            lines.append(f"<span class=\"{self._get_class_name(name)}\">{source}</span>")

        newl = "\n"
        return f"<style>{self.stylesheet}</style><pre>{''.join(lines)}</pre>"

class Tab(QtWidgets.QWidget):
    def __init__(self, filepath, filename, tab_index, existing, lexer=None):
        super(QtWidgets.QWidget, self).__init__()

        print(filepath, filename)

        self.lexer = lexer
        self.existing = existing
        self.raw_text = ""
        self.colorscheme = None
        self.debounce = False

        self.file_path = filepath
        self.file_name = filename
        self.setObjectName(self.file_name)

        self.editor_font = QtGui.QFont()
        self.editor_font.setFamily("Iosevka")
        self.editor_font.setPointSize(12)

        self.grid_layout = QtWidgets.QGridLayout(self)
        self.grid_layout.setContentsMargins(3, 3, 3, 3)
        self.grid_layout.setHorizontalSpacing(6)
        self.grid_layout.setObjectName(f"editorGridLayout_{tab_index}")

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(f"editorSplitter_{tab_index}")

        self.number_pane = QtWidgets.QTextEdit(self.splitter)
        self.number_pane.setMaximumSize(QtCore.QSize(50, 16777215))
        self.number_pane.setFont(self.editor_font)
        self.number_pane.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.number_pane.setFrameShadow(QtWidgets.QFrame.Plain)
        self.number_pane.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.number_pane.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.number_pane.setUndoRedoEnabled(False)
        self.number_pane.setReadOnly(True)
        self.number_pane.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.number_pane.setObjectName(f"lineNumberPane_{tab_index}")

        self.editor_pane = QtWidgets.QTextEdit(self.splitter)
        self.editor_pane.setFont(self.editor_font)
        self.editor_pane.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.editor_pane.setFrameShadow(QtWidgets.QFrame.Plain)
        self.editor_pane.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.editor_pane.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.editor_pane.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.editor_pane.setObjectName(f"editorPane_{tab_index}")

        self.grid_layout.addWidget(self.splitter, 0, 0, 1, 1)

        self.editor_pane.textChanged.connect(self.text_updated)
        self.editor_pane.verticalScrollBar().valueChanged.connect(self.sync_scroll)

        self.text_updated()
        self.editor_pane.setFocus()
        self.editor_pane.moveCursor(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)

    def sync_scroll(self, value):
        if self.number_pane.verticalScrollBar().value() != value:
            self.number_pane.verticalScrollBar().setSliderPosition(value)

    def text_updated(self):
        if self.debounce:
            self.debounce = False

        else:
            self.raw_text = self.editor_pane.toPlainText()

            self.number_pane.setHtml("\n".join(f"<p align='right' style='margin-top:0px; margin-bottom:0px'>{x}</p>" for x in range(1, len(self.text.split("\n")) + 1)))
            self.sync_scroll(self.editor_pane.verticalScrollBar().value())

            # syntax lexing/highlighting
            if self.lexer is not None and self.colorscheme is not None:
                #cursor = self.editor_pane.textCursor()

                tokens = pygments.lex(self.text, self.lexer)
                format_result = self.formatter(tokens)

                #print(format_result)
                self.debounce = True
                self.editor_pane.setHtml(format_result)

                #self.editor_pane.setTextCursor(cursor)
                self.editor_pane.ensureCursorVisible()

    @property
    def text(self):
        return self.raw_text

    @text.setter
    def text(self, text):

        self.editor_pane.setPlainText(text)

    @property
    def modified(self):
        return self.editor_pane.document().isModified()

    def load_colorscheme(self, scheme_def):
        style_lines = []

        self.editor_pane.setStyleSheet(f"QTextEdit {{ background: {scheme_def['Body']['background']}; color: {scheme_def['Body']['color']}; }}")
        for name, data in scheme_def.items():
            style_lines.append(f"{data['css_class']}{{{'color:' + data['color'] if data.get('color') is not None else ''};{'background:' + data['background'] if data.get('background') is not None else ''};{''.join(self._get_font_style(style) for style in data['font']) if data['font'] is not None else ''}}}")

        self.colorscheme = "\n".join(style_lines)
        self.formatter = QtHtmlFormatter(self.colorscheme)

    def _get_font_style(self, style_name):
        if style_name == "bold":
            return "font-weight: bold;"

        elif style_name == "italic":
            return "font-style: italic;"

        elif style_name == "underline":
            return "text-decoration: underline;"

        else:
            raise RuntimeError(f"Invalid text style '{style_name}'")

class PyPad(Ui_MainWindow):
    def __init__(self, window, parent=None):
        Ui_MainWindow.__init__(self)

        self.tabs = []
        self.window = window

        try:
            with open("./config.yaml", "r", encoding="utf-8") as f:
                self.config = yaml.load(f)

        except Exception as e:
            print(f"Error loading config: [{e.__class__.__name__}]: {e}")
            sys.exit(1)

        try:
            with open(f"{self.config['colorscheme']['search_dir']}/{self.config['colorscheme']['active_scheme']}.yaml", "r", encoding="utf-8") as f:
                self.colorscheme = yaml.load(f)

        except yaml.scanner.ScannerError as e:
            print(f"Could not parse colorscheme '{self.config['colorscheme']['active_scheme']}': {e}")
            sys.exit(1)

        except FileNotFoundError as e:
            print(f"Cannot find the requested colorscheme: {e}")
            sys.exit(1)

        except Exception as e:
            print(f"Error loading scheme: [{e.__class__.__name__}]: {e}")
            sys.exit(1)

        self.setupUi(window)

        window.setWindowTitle("PyPad")

        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        # Action connections
        self.actionOpen.triggered.connect(self.open_file)
        self.actionQuit.triggered.connect(self.exit)
        self.actionNew.triggered.connect(self.new_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionSaveAs.triggered.connect(self.save_file_as)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrintPreview.triggered.connect(self.preview_print)

        self.actionUndo.triggered.connect(self.editor_undo)
        self.actionRedo.triggered.connect(self.editor_redo)

        self.actionCut.triggered.connect(self.editor_cut)
        self.actionCopy.triggered.connect(self.editor_copy)
        self.actionPaste.triggered.connect(self.editor_paste)

        self.actionSelectAll.triggered.connect(self.editor_select_all)

        self.actionFind.triggered.connect(self.find_in_file)
        self.actionReplace.triggered.connect(self.replace_in_file)

        window.show()

        if launch_args.filenames:
            for file in launch_args.filenames[0]:
                self.load_file(file)

        else:
            self.new_file()

    @property
    def active_tab(self):
        return self.tabWidget.currentWidget()

    def open_tab(self, filepath=None, existing=False):
        if self.active_tab:
            if self.active_tab.existing is False and self.active_tab.modified is False:
                self.close_tab(self.tabWidget.currentIndex())

        if filepath is None:
            file_name = "untitled"
            filepath = os.getcwd()
        else:
            file_name = filepath.split("/")[-1]
            filepath = "/".join(filepath.split("/")[:-1])

        try:
            lexer = pygments.lexers.get_lexer_for_filename(file_name)
        except pygments.util.ClassNotFound:
            print("No lexer for filetype")
            lexer = None

        tab_idx = len(self.tabs)
        tab = Tab(filepath, file_name, tab_idx, existing, lexer)
        tab.load_colorscheme(self.colorscheme)

        self.tabs.append(tab)

        self.tabWidget.addTab(tab, tab.file_name)
        self.tabWidget.setCurrentIndex(tab_idx)

        return tab

    def close_tab(self, tab_idx):
        print(tab_idx)
        if self.tabs[tab_idx]:
            self.tabWidget.removeTab(tab_idx)
            del self.tabs[tab_idx]

    def load_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            tab = self.open_tab(filepath, existing=True)
            tab.text = content

        except Exception as e:
            print(f"Cannot open '{filepath}': [{e.__class__.__name__}]: {e}")

    def reload_file(self, filepath):
        self.close_tab(self.tabWidget.currentIndex())

        self.load_file(filepath)

    def exit(self):
        self.window.close()
        sys.exit()

    def open_file(self):
        files, _filter = QtWidgets.QFileDialog.getOpenFileNames(None, "Open File")

        for file in files:
            self.load_file(file)

    def new_file(self):
        self.open_tab()

    def save_file(self):
        active_tab = self.active_tab
        file = f"{active_tab.file_path}/{active_tab.file_name}"
        print(active_tab.existing)

        if not active_tab.existing:
            self.save_file_as()
        else:
            with open(file, "w", encoding="utf-8") as f:
                f.write(active_tab.text)

    def save_file_as(self):
        file_name, _filter = QtWidgets.QFileDialog.getSaveFileName(None, "Save File")

        if file_name == "":
            print("File dialog closed")
            return

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(self.active_tab.text)

        self.reload_file(file_name)

    def print_file(self):
        print_dialog = QtPrintSupport.QPrintDialog()
        if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.active_tab.editor_pane.document().print_(print_dialog.printer())

    def preview_print(self):
        print_dialog = QtPrintSupport.QPrintPreviewDialog()
        print_dialog.paintRequested.connect(self.active_tab.editor_pane.print_)
        print_dialog.exec_()

    def editor_undo(self):
        if self.active_tab:
            self.active_tab.editor_pane.undo()

    def editor_redo(self):
        if self.active_tab:
            self.active_tab.editor_pane.redo()

    def editor_cut(self):
        if self.active_tab:
            self.active_tab.editor_pane.cut()

    def editor_copy(self):
        if self.active_tab:
            self.active_tab.editor_pane.copy()

    def editor_paste(self):
        if self.active_tab:
            self.active_tab.editor_pane.paste()

    def editor_select_all(self):
        if self.active_tab:
            self.active_tab.editor_pane.select_all()

    def find_in_file(self):
        print("Find")

    def replace_in_file(self):
        print("Replace")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()
    pypad = PyPad(window)

    sys.exit(app.exec_())

        #     self.tab = QtWidgets.QWidget()
        # self.tab.setObjectName("tab")
        # self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        # self.gridLayout_2.setContentsMargins(3, 3, 3, 3)
        # self.gridLayout_2.setHorizontalSpacing(6)
        # self.gridLayout_2.setObjectName("gridLayout_2")
        # self.splitter = QtWidgets.QSplitter(self.tab)
        # self.splitter.setOrientation(QtCore.Qt.Horizontal)
        # self.splitter.setChildrenCollapsible(False)
        # self.splitter.setObjectName("splitter")
        # self.textEdit_2 = QtWidgets.QTextEdit(self.splitter)
        # self.textEdit_2.setMaximumSize(QtCore.QSize(50, 16777215))
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.textEdit_2.setFont(font)
        # self.textEdit_2.setStyleSheet("")
        # self.textEdit_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.textEdit_2.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.textEdit_2.setUndoRedoEnabled(False)
        # self.textEdit_2.setReadOnly(True)
        # self.textEdit_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        # self.textEdit_2.setObjectName("textEdit_2")
        # self.textEdit = QtWidgets.QTextEdit(self.splitter)
        # font = QtGui.QFont()
        # font.setPointSize(12)
        # self.textEdit.setFont(font)
        # self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        # self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        # self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        # self.textEdit.setObjectName("textEdit")
        # self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        # self.tabWidget.addTab(self.tab, "")