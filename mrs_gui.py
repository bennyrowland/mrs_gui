__author__ = 'ben'

from PySide import QtGui, QtCore
import sys

from pyflow.view import FlowView
from pyflow.model import FlowModel

if __name__ == "__main__":
    my_app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    main_window.resize(400, 400)
    main_window.setWindowTitle("MRS GUI tool v0.1")

    flow_view = FlowView()
    flow_view.setBackgroundBrush(QtCore.Qt.black)
    #flow_view.resize(400, 400)

    main_window.setCentralWidget(flow_view)

    flow_model = FlowModel()
    flow_model.add_item()

    flow_view.set_model(flow_model)

    flow_model.add_item()
    flow_model.set_data(0, "name", "Hello")
    flow_model.set_data(0, "position", QtCore.QPoint(50, 50))

    main_window.show()
    sys.exit(my_app.exec_())