#!/usr/bin/env python

import sys

from PyQt5.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    from pypad import window

    window.main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
