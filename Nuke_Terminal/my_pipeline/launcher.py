import nuke

try:
    
    from PySide6 import QtWidgets
except ImportError:
    
    from PySide2 import QtWidgets


class MyPipelineWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyPipelineWindow, self).__init__()
        self.setWindowTitle("My Nuke Pipeline")
        self.resize(420, 220)

        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout()

        title = QtWidgets.QLabel("Welcome to My Nuke Pipeline")
        button = QtWidgets.QPushButton("Test Button")

        button.clicked.connect(self.on_test_clicked)

        layout.addWidget(title)
        layout.addWidget(button)
        layout.addStretch()

        self.setLayout(layout)

    def on_test_clicked(self):
        nuke.message("It works!")


_pipeline_window = None


def show_pipeline_window():
    global _pipeline_window

    
    if _pipeline_window is None:
        _pipeline_window = MyPipelineWindow()

    _pipeline_window.show()
    _pipeline_window.raise_()
    _pipeline_window.activateWindow()