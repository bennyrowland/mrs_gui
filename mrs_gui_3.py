__author__ = 'ben'

from PySide import QtGui, QtCore

from window import MainWindow

import pyflow


import sys
if __name__ == "__main__":
    pyflow.set_colour_for_type(0, QtCore.Qt.cyan)
    pyflow.set_colour_for_type(1, QtCore.Qt.magenta)
    pyflow.set_colour_for_type(2, QtCore.Qt.yellow)
    pyflow.set_colour_for_type(3, QtCore.Qt.blue)
    my_app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()

    main_window.show()

    sys.exit(my_app.exec_())