from PySide2.QtGui import QGuiApplication


class QApp:
    def __init__(self, argv):
        self.app = QGuiApplication(argv)

    def run(self):
        self.app.exec_()
