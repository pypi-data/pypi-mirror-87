from PySide2.QtCore import QStringListModel, QObject, Slot


class ListController(QObject):
    list_model = []
    list_user = []
    current_indexes_selected = []

    def set_list_model(self, new_list):
        self.list_user = new_list
        self.list_model = QStringListModel()
        self.list_model.setStringList(self.list_user)

    @Slot(str, result=list)  # also works: @pyqtSlot(QVariant, result=QVariant)
    def add_item_selected(self, item):
        if item in self.current_indexes_selected:
            self.current_indexes_selected = sorted(self.current_indexes_selected)
            self.current_indexes_selected.pop(int(item))
        else:
            self.current_indexes_selected.append(item)
        return self.current_indexes_selected
