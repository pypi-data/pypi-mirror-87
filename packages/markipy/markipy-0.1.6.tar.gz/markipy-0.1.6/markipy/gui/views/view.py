from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QSize, QUrl

import sys


class QTView:
    def __init__(self, width=960, height=500):
        self.view = QQuickView()
        self.view.setMaximumSize(QSize(width, height))
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)

    def addModel(self, model_name, model):
        self.view.rootContext().setContextProperty(model_name, model)

    def addView(self, qml_path):
        self.view.setSource(QUrl.fromLocalFile(qml_path))

    def show(self):
        if self.view.status() == QQuickView.Error:
            sys.exit(-1)
        self.view.show()
