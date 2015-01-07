__author__ = 'ben'

from PySide import QtGui, QtCore
import sys

from pyflow.view import FlowScene
from pyflow.model import FlowModel
import pyflow.save_load
import pyflow

if __name__ == "__main__":
    pyflow.set_colour_for_type(1, QtCore.Qt.magenta)
    pyflow.set_colour_for_type(2, QtCore.Qt.yellow)

    my_app = QtGui.QApplication(sys.argv)

    main_window = QtGui.QMainWindow()

    main_window.resize(400, 400)
    main_window.setWindowTitle("MRS GUI tool v0.1")

    flow_scene = FlowScene()
    flow_view = QtGui.QGraphicsView()
    flow_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    flow_view.setScene(flow_scene)
    flow_view.setBackgroundBrush(QtCore.Qt.gray)

    main_window.setCentralWidget(flow_view)

    flow_model = FlowModel()
    flow_model.add_item()

    flow_scene.set_model(flow_model)

    flow_model.add_item()
    flow_model.set_data(0, "name", "SVS Recon")
    flow_model.set_data(0, "position", QtCore.QPoint(50, 50))

    flow_model.add_item()
    flow_model.set_data(1, "name", "World")
    flow_model.set_data(1, "position", QtCore.QPoint(500, 100))

    flow_model.add_item()
    flow_model.set_data(3, "name", "Hello")
    flow_model.set_data(2, "name", "!!!!!")
    flow_model.set_data(2, "position", QtCore.QPoint(500, 150))

    flow_model.set_data(0, "inputs", [{"name": "Fish", "type": 3}])
    flow_model.set_data(0, "outputs", [{"name": "Data", "type": 2}])
    flow_model.set_data(0, "inputs", [{"name": "Data", "type": 1},
                                      {"name": "Water Ref", "type": 1},
                                      ])
    flow_model.set_data(1, "inputs", [{"name": "Grom", "type": 2}])
    flow_model.set_data(0, "connections", [{"output": 0,
                                            "input": 0,
                                            "step": 1}])

    flow_model.remove_item(3)

    #flow_model = FlowModel()
    #flow_model.add_item()
    #flow_model.set_data(0, "name", "Mystery")
    #flow_scene.set_model(flow_model)

    #flow_view.fitInView(flow_scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    # load
    #flow_model = pyflow.save_load.load_model("C:/Users/Sam/PycharmProjects/pyflow/tests/save_test.txt", flow_model)

    # save
    #pyflow.save_load.save_model("C:/Users/Sam/PycharmProjects/pyflow/tests/save_test.txt", flow_model)

    main_window.show()

    sys.exit(my_app.exec_())

