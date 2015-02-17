__author__ = 'ben'

from PySide import QtGui, QtCore
import json

from pyflow.model import FlowModel
from pyflow.view.scene import FlowScene
from plugin_manager import PluginModel


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("MRS GUI tool v0.1")
        self.resize(1000, 600)

        file_menu = self.menuBar().addMenu("&File")
        new_action = QtGui.QAction('New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_model_request)
        file_menu.addAction(new_action)
        open_action = QtGui.QAction('Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_model_request)
        file_menu.addAction(open_action)
        save_action = QtGui.QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_model_request)
        file_menu.addAction(save_action)

        help_menu = self.menuBar().addMenu("&Help")
        about_action = QtGui.QAction("About", self)
        help_menu.addAction(about_action)

        self.model = FlowModel()
        flow_scene = FlowScene()
        #flow_scene.set_model(self.model)

        flow_view = QtGui.QGraphicsView()
        flow_view.setBackgroundBrush(QtCore.Qt.gray)
        flow_view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        flow_view.setScene(flow_scene)
        flow_view.setAcceptDrops(True)

        self.setCentralWidget(flow_view)

        #self.model.create_step_with_params({"pos": {"x": 0, "y": 0},
        #                                    "class": "twix_loader",
        #                                    "protocols": ["svs_se_30-PCG",
        #                                                  "svs_se_30-PCG_wref",
        #                                                  "svs_se_30-Left_Temp",
        #                                                  "svs_se_30-Left_Temp_wref"]})

        #self.model.create_step_with_params({"pos": {"x": 100, "y": 75},
        #                                    "class": "twix_svs"})

        #self.model.create_step_with_params({"pos": {"x": 0, "y": 175},
        #                                    "class": "lcmodel"})

        #self.model.create_step_with_params({"pos": {"x": 200, "y": 100},
        #                                    "class": "ps2pdf"})

        self.model.create_step_with_params({"pos": {"x": 30, "y": 300},
                                            "class": "mail"})

        flow_scene.set_model(self.model)

        settings_widget = QtGui.QWidget()
        settings_layout = QtGui.QFormLayout()
        self.settings_name_edit = QtGui.QLineEdit()
        self.settings_name_edit.setText("New Study")
        settings_layout.addRow("Study Name", self.settings_name_edit)
        self.settings_data_edit = QtGui.QLineEdit()
        self.settings_data_edit.setText("/media/mrs_data/")
        settings_layout.addRow("Data Folder", self.settings_data_edit)
        self.settings_proc_edit = QtGui.QLineEdit()
        self.settings_proc_edit.setText("/media/mrs_proc/")
        settings_layout.addRow("Proc Folder", self.settings_proc_edit)
        settings_widget.setLayout(settings_layout)
        settings_float = QtGui.QDockWidget("Network Settings", self)
        settings_float.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        settings_float.setWidget(settings_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, settings_float)

        plugin_widget = QtGui.QListView()
        plugin_model = PluginModel()
        plugin_widget.setModel(plugin_model)
        plugin_widget.setDragEnabled(True)
        plugin_float = QtGui.QDockWidget("Steps", self)
        plugin_float.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)
        plugin_float.setWidget(plugin_widget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, plugin_float)

    def new_model_request(self):
        print "new model requested"
        self.clear_model()

    def clear_model(self):
        for step in self.centralWidget().scene().steps:
            for output in step.outputs:
                for connector in output.connections:
                    pass #output.break_connection(connector["connector"])
        #for i in range(self.model.rowCount()):
        #    self.model.removeRows(0, 2, self.model.index(i, 0))
        self.model.removeRows(0, self.model.rowCount())
        self.centralWidget().scene().set_model(self.model)

    def open_model_request(self):
        filename, filtr = QtGui.QFileDialog.getOpenFileName(self,
                                                            "Open Config File",
                                                            "/media/mrs_proc",
                                                            "Config Files (*.config)")
        if filename:
            self.open_model(filename)
            #self.open_model("/media/mrs_proc/ben/test_proc/CTE.config")

    def open_model(self, filename):
        self.clear_model()
        self.centralWidget().scene().set_model(None)
        with open(filename) as fout:
            load_dict = json.load(fout)
        print load_dict
        self.settings_name_edit.setText(load_dict["study_name"])
        self.settings_data_edit.setText(load_dict["base_data_path"])
        self.settings_proc_edit.setText(load_dict["base_proc_path"])
        for step_dict in load_dict["steps"]:
            print "creating step %s" % step_dict
            self.model.create_step_with_params(step_dict)
        self.centralWidget().scene().set_model(self.model)
        for connection_dict in load_dict["connections"]:
            print "creating connection %s" % connection_dict
            output_step_index = self.model.index(connection_dict["output_id"], 0)

            output_socket_index = self.model.match(self.model.index(0, 0, self.model.index(0, 0, output_step_index)), QtCore.Qt.DisplayRole, connection_dict["output_socket"])[0]
            input_step_index = self.model.index(connection_dict["input_id"], 0)
            print output_socket_index
            input_socket_index = self.model.match(self.model.index(0, 0, self.model.index(1, 0, input_step_index)), QtCore.Qt.DisplayRole, connection_dict["input_socket"])[0]
            print input_socket_index
            self.model.insertRow(0, output_socket_index)
            self.model.setData(self.model.index(0, 0, output_socket_index), input_socket_index)

    def save_model_request(self):
        filename, filtr = QtGui.QFileDialog.getSaveFileName(self,
                                                            "Save Config File",
                                                            "/media/mrs_proc",
                                                            "Config Files (*.config)")
        if filename:
            self.save_model(filename)
            #self.save_model("/media/mrs_proc/ben/test_proc/CTE.config")

    def save_model(self, filename):
        save_dict = {"study_name": self.settings_name_edit.text(),
                     "base_data_path": self.settings_data_edit.text(),
                     "base_proc_path": self.settings_proc_edit.text()}
        # loop over all the steps in the model, getting a dictionary
        # for each of them in turn
        steps_list = []
        for i in range(self.model.rowCount()):
            step_index = self.model.index(i, 0)
            steps_list.append(self.model.dict_for_step(step_index))
        save_dict["steps"] = steps_list
        # now get a list of connections between the steps
        connections_list = []
        for i in range(self.model.rowCount()):
            step_index = self.model.index(i, 0)
            output_list_index = self.model.index(0, 0, step_index)
            for j in range(self.model.rowCount(output_list_index)):
                output_index = self.model.index(j, 0, output_list_index)
                output_name = self.model.data(output_index)
                for k in range(self.model.rowCount(output_index)):
                    connection_index = self.model.index(k, 0, output_index)
                    other_end_index = self.model.data(connection_index, QtCore.Qt.UserRole)
                    if other_end_index is not None:
                        print other_end_index.internalPointer()
                        input_name = self.model.data(other_end_index.parent(), QtCore.Qt.DisplayRole)
                        input_id = other_end_index.parent().parent().parent().row()
                        connections_list.append({"output_id": i,
                                                 "output_socket": output_name,
                                                 "input_id": input_id,
                                                 "input_socket": input_name})
        save_dict["connections"] = connections_list
        print "saving model"
        with open(filename, 'w') as fout:
            json.dump(save_dict, fout, sort_keys=True, indent=4, separators=(',', ": "))