from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QFileDialog


from pypad import window, editor


class Tabs(QTabWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.change_tab)

    def close_tab(self, index):
        tab = self.widget(index)
        tab.save()
        tab.deleteLater()
        self.removeTab(index)

    def get_current(self):
        return self.widget(self.currentIndex())

    def change_tab(self, index):
        name = self.widget(index).get_name()
        window.main_window.set_filename(name)

    def new_tab(self, path: str=''):
        tab = editor.Editor(path)
        self.addTab(tab, tab.get_name())

    def open(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(window.main_window, 'Open a file', '',
                                                'All Files (*);;Python Files (*.py);;Text Files (*.txt)',
                                                options=options)
        if files:
            self.new_tab(files[0])


tabs = Tabs()
