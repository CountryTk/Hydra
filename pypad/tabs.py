import os

from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QFileDialog


from pypad import directory, editor, window


class Tabs(QTabWidget):

    def __init__(self):
        """
        create tab bar widget
        """
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.change_tab)

    def close_tab(self, index):
        """
        close a tab and destroy the editor instance
        :param index: tab index that has been closed
        """
        tab = self.widget(index)
        tab.save()
        tab.deleteLater()
        self.removeTab(index)

    def get_current(self):
        """
        get the widget that is currently selected
        :return: selected widget
        """
        return self.widget(self.currentIndex())

    def change_tab(self, index):
        """
        when clicking a tab on the bar, change to selected tab
        :param index: index of the tab that has been selected
        """
        widget = self.widget(index)
        if widget:
            window.main_window.set_filename(widget.get_name())

    def new_tab(self, path: str=''):
        """
        create a new editor instance and add it as a tab
        :param path: file path to open, empty string means a new file
        """
        tab = editor.Editor(path)
        index = self.addTab(tab, tab.get_name())
        self.setCurrentIndex(index)

    def open(self):
        """
        create a dialog to select a file to open as a new tab
        """
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(window.main_window, 'Open a file', '',
                                                'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                options=options)
        if files:
            directory.directory_tree.set_root(os.path.dirname(files[0]))
            self.new_tab(files[0])


tabs = Tabs()
