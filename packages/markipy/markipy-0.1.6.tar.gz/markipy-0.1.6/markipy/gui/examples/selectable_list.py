from PySide2.QtCore import QStringListModel

from markipy.basic import File

from markipy.gui import QApp
from markipy.gui import QTView
from markipy.gui import ListController
from markipy.gui import DEFAULT_QML_VIEW_FOLDER
import sys

if __name__ == '__main__':
    # Start a QTApp
    app = QApp(sys.argv)

    # Create view
    view = QTView(960, 500)

    # Create the list controller
    list_controller = ListController()

    # Add data to the list controller
    data = ['Python', 'is ', 'awesome']
    list_controller.set_list_model(data)
    # Expose the controllers to the Qml code
    my_model = QStringListModel()
    my_model.setStringList(data)

    # Set Qml Context
    view.addModel('myListControl', list_controller)
    view.addModel('myModel', my_model)

    # Retrieve list.qml
    qml_list_file = File(DEFAULT_QML_VIEW_FOLDER() / "list.qml")
    # Retrieve the absolute path as str
    qml_path = str(qml_list_file().absolute())
    # Add qml to the view
    view.addView(qml_path)

    # Show view
    view.show()

    # Run the application
    app.run()
