from PySide import QtCore, QtGui
import sys
import samtestpy

class Output_pref(QtGui.QDialog, samtestpy.Ui_in_out_settings):

    def __init__(self):
        super(Output_pref, self).__init__()

        self.setModal(True)
        self.setupUi(self)

    def set_index(self, index):
        self.index = index
        self.refresh()

    def refresh(self):
        input_list_index = self.index.model().index(1, 0, self.index)
        output_list_index = self.index.model().index(0, 0, self.index)
        self.input_proxy_model = StepProxyModel(input_list_index)
        self.inputView.setModel(self.input_proxy_model)
        self.output_proxy_model = StepProxyModel(output_list_index)
        self.outputView.setModel(self.output_proxy_model)

    def add_input(self):
        if self.input_proxy_model is not None:
            self.input_proxy_model.addRow(self.input_proxy_model.rowCount())

class StepProxyModel(QtGui.QAbstractProxyModel):
    def __init__(self, index):
        print "creating new StepProxyModel"
        super(StepProxyModel, self).__init__()
        self.parent_index = index
        self.setSourceModel(self.parent_index.model())

    def mapToSource(self, proxyIndex):
        print "mapToSource called with index %s" % proxyIndex
        print self.parent_index.internalPointer().__class__
        #if proxyIndex.isValid():
        print "mapToSource %s return " % proxyIndex,
        print "%s" % self.parent_index.model().index(proxyIndex.row(), proxyIndex.column(), self.parent_index)
        return self.sourceModel().index(proxyIndex.row(), proxyIndex.column(), self.parent_index)

        #else:
            #return QtCore.QModelIndex()

    def mapFromSource(self, sourceIndex):
        print "mapFromSource called with index %s" % sourceIndex
        if sourceIndex.parent() == self.parent_index:
            return self.createIndex(sourceIndex.row(), sourceIndex.column(), QtCore.QModelIndex)
        else:
            return QtCore.QModelIndex()

    def hasChildren(self, parent):
        #print "hasChildren called"
        if parent.isValid():
            # we want to display a flat list so no item has children
            return False
        # null parent refers to the entire list so return True if the source
        # list has entries in it
        return self.sourceModel.rowCount(self.parent_index) > 0

    def rowCount(self, parent=QtCore.QModelIndex()):
        print "rowCount called"
        print parent
        if parent.isValid():
            return 0
        print self.sourceModel().rowCount(self.parent_index)
        return self.sourceModel().rowCount(self.parent_index)
        #return self.index.model().rowCount(self.index.parent())

    def columnCount(self, parent=QtCore.QModelIndex()):
        print "columnCount called"
        if parent.isValid():
            return 0
        return 2

    def index(self, rows, columns, parent):
        print "create index called"
        return self.createIndex(rows, columns, QtCore.QModelIndex())

    def parent(self, index):
        return QtCore.QModelIndex()

def run_settings(index):

    #app = QApplication(sys.argv)
    form = Output_pref()
    form.set_index(QtCore.QPersistentModelIndex(index))
    form.show()
    form.exec_()