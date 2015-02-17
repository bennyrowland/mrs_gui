__author__ = 'ben'

from PySide import QtGui, QtCore
import stevedore


class PluginModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(PluginModel, self).__init__(parent)
        self.extension_manager = stevedore.extension.ExtensionManager(namespace="mrs.flow.step")

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        else:
            return len(self.extension_manager.names())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role not in [QtCore.Qt.DisplayRole]:
            return None
        return self.extension_manager.names()[index.row()]

    def flags(self, index=QtCore.QModelIndex()):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable

    def mimeTypes(self):
        return ["application/flow"]

    def mimeData(self, indexes):
        if len(indexes) > 1:
            return None
        index = indexes[0]
        if not index.isValid():
            return None
        mime_data = QtCore.QMimeData()
        mime_data.setData("/application/flow", self.extension_manager.names()[index.row()])
        return mime_data