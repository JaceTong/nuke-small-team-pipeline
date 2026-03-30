try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from my_pipeline.ui.project_setup_widget import ProjectSetupWidget


class MyPipelineWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyPipelineWindow, self).__init__()
        self.setWindowTitle("My Nuke Pipeline")
        self.resize(700, 420)
        self.build_ui()

    def build_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)

        # 左侧导航
        self.nav_list = QtWidgets.QListWidget()
        self.nav_list.setFixedWidth(180)
        self.nav_list.addItem("Project Setup")
        self.nav_list.addItem("Nuke Info")
        self.nav_list.addItem("Tools")

        # 右侧页面区
        self.stack = QtWidgets.QStackedWidget()

        self.project_setup_page = ProjectSetupWidget()
        self.nuke_info_page = self._build_placeholder("Nuke Info page coming soon.")
        self.tools_page = self._build_placeholder("Tools page coming soon.")

        self.stack.addWidget(self.project_setup_page)
        self.stack.addWidget(self.nuke_info_page)
        self.stack.addWidget(self.tools_page)

        self.nav_list.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav_list.setCurrentRow(0)

        main_layout.addWidget(self.nav_list)
        main_layout.addWidget(self.stack)

    def _build_placeholder(self, text):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        label = QtWidgets.QLabel(text)
        layout.addWidget(label)
        layout.addStretch()
        return widget