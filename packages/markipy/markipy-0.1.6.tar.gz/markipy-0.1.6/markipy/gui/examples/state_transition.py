from markipy.basic import File

from markipy.gui import QApp
from markipy.gui import QTView
from markipy.gui import DEFAULT_QML_VIEW_FOLDER
import sys

if __name__ == '__main__':
    # Start a QTApp
    app = QApp(sys.argv)

    # Create view
    view = QTView(960, 500)

    # Retrieve list.qml
    qml_list_file = File(DEFAULT_QML_VIEW_FOLDER() / "state_transition.qml")
    # Retrieve the absolute path as str
    qml_path = str(qml_list_file().absolute())
    # Add qml to the view
    view.addView(qml_path)

    # Show view
    view.show()

    # Run the application
    app.run()
