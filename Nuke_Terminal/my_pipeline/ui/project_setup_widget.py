import nuke

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from my_pipeline.tools.folder_creator import (
    DEFAULT_SUBFOLDERS,
    list_project_folders,
    create_new_project_with_default_structure,
)
from my_pipeline.tools.nuke_script_creator import create_initial_nuke_script
from my_pipeline.tools.project_browser import (
    list_sequence_folders,
    list_shot_folders,
    list_task_folders,
)


from my_pipeline.tools.settings_manager import get_base_path, set_base_path


class NewProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewProjectDialog, self).__init__(parent)
        self.setWindowTitle("Create New Project")
        self.resize(320, 120)
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel("New Project Name:"))

        self.project_name_input = QtWidgets.QLineEdit()
        self.project_name_input.setPlaceholderText("e.g. OTL")
        layout.addWidget(self.project_name_input)

        button_row = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_row.addStretch()
        button_row.addWidget(self.ok_button)
        button_row.addWidget(self.cancel_button)

        layout.addLayout(button_row)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_project_name(self):
        return self.project_name_input.text().strip()


class ProjectSetupWidget(QtWidgets.QWidget):
    def load_saved_base_path(self):
        saved_base_path = get_base_path()
        self.base_path_input.setText(saved_base_path)

    def __init__(self):
        super(ProjectSetupWidget, self).__init__()
        self.default_folder_names = DEFAULT_SUBFOLDERS
        self.build_ui()
        self.load_saved_base_path()
        self.refresh_projects()

    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # =========================
        # Top section
        # =========================
        top_group = QtWidgets.QGroupBox("Project Setup")
        top_layout = QtWidgets.QVBoxLayout(top_group)

        title = QtWidgets.QLabel("Project Setup")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Base path
        base_path_label = QtWidgets.QLabel("Base Path:")
        self.base_path_input = QtWidgets.QLineEdit()
        self.base_path_input.setReadOnly(True)

        self.browse_button = QtWidgets.QPushButton("Change Base Path")
        self.browse_button.setToolTip("Choose a different base path")

        base_path_row = QtWidgets.QHBoxLayout()
        base_path_row.addWidget(self.base_path_input)
        base_path_row.addWidget(self.browse_button)




        # Project dropdown
        project_name_label = QtWidgets.QLabel("Project Name:")
        self.project_combo = QtWidgets.QComboBox()
        self.project_combo.setToolTip("Projects found under the selected base path")

        project_button_row = QtWidgets.QHBoxLayout()
        self.refresh_projects_button = QtWidgets.QPushButton("Refresh Projects")
        self.create_new_project_button = QtWidgets.QPushButton("Create New Project")
        project_button_row.addWidget(self.refresh_projects_button)
        project_button_row.addWidget(self.create_new_project_button)

        # Other buttons
        action_button_row = QtWidgets.QHBoxLayout()
        self.create_script_button = QtWidgets.QPushButton("Create Initial Nuke Script")
        self.refresh_browser_button = QtWidgets.QPushButton("Refresh Browser")
        action_button_row.addWidget(self.create_script_button)
        action_button_row.addWidget(self.refresh_browser_button)

        # Log
        self.log_box = QtWidgets.QTextEdit()
        self.log_box.setReadOnly(True)

        top_layout.addWidget(title)
        top_layout.addSpacing(8)
        top_layout.addWidget(base_path_label)
        top_layout.addLayout(base_path_row)
        top_layout.addWidget(project_name_label)
        top_layout.addWidget(self.project_combo)
        top_layout.addLayout(project_button_row)
        top_layout.addSpacing(8)
        top_layout.addLayout(action_button_row)
        top_layout.addSpacing(12)
        top_layout.addWidget(QtWidgets.QLabel("Log:"))
        top_layout.addWidget(self.log_box)

        # =========================
        # Bottom section
        # =========================
        bottom_group = QtWidgets.QGroupBox("Project Browser")
        bottom_layout = QtWidgets.QVBoxLayout(bottom_group)

        browser_layout = QtWidgets.QHBoxLayout()

        sequence_layout = QtWidgets.QVBoxLayout()
        sequence_layout.addWidget(QtWidgets.QLabel("Sequence"))
        self.sequence_list = QtWidgets.QListWidget()
        sequence_layout.addWidget(self.sequence_list)

        shot_layout = QtWidgets.QVBoxLayout()
        shot_layout.addWidget(QtWidgets.QLabel("Shot"))
        self.shot_list = QtWidgets.QListWidget()
        shot_layout.addWidget(self.shot_list)

        task_layout = QtWidgets.QVBoxLayout()
        task_layout.addWidget(QtWidgets.QLabel("Task / Process"))
        self.task_list = QtWidgets.QListWidget()
        task_layout.addWidget(self.task_list)

        browser_layout.addLayout(sequence_layout)
        browser_layout.addLayout(shot_layout)
        browser_layout.addLayout(task_layout)

        self.current_path_label = QtWidgets.QLabel("Current Selection: ")
        self.current_path_label.setWordWrap(True)

        bottom_layout.addLayout(browser_layout)
        bottom_layout.addWidget(self.current_path_label)

        main_layout.addWidget(top_group, 3)
        main_layout.addWidget(bottom_group, 2)

        # Signals
        self.browse_button.clicked.connect(self.browse_folder)
        self.refresh_projects_button.clicked.connect(self.refresh_projects)
        self.create_new_project_button.clicked.connect(self.on_create_new_project_clicked)
        self.create_script_button.clicked.connect(self.on_create_script_clicked)
        self.refresh_browser_button.clicked.connect(self.refresh_browser)

        self.project_combo.currentIndexChanged.connect(self.refresh_browser)
        self.sequence_list.itemSelectionChanged.connect(self.on_sequence_changed)
        self.shot_list.itemSelectionChanged.connect(self.on_shot_changed)
        self.task_list.itemSelectionChanged.connect(self.update_current_selection_label)

    def show_info(self, title, message):
        QtWidgets.QMessageBox.information(self, title, message)
        self.window().raise_()
        self.window().activateWindow()

    def show_warning(self, title, message):
        QtWidgets.QMessageBox.warning(self, title, message)
        self.window().raise_()
        self.window().activateWindow()

    def show_error(self, title, message):
        QtWidgets.QMessageBox.critical(self, title, message)
        self.window().raise_()
        self.window().activateWindow()

    def browse_folder(self):
        current_base_path = self.get_base_path()

        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Base Folder",
            current_base_path
        )

        if folder:
            self.base_path_input.setText(folder)
            set_base_path(folder)
            self.refresh_projects()

    def get_base_path(self):
        return self.base_path_input.text().strip()

    def get_project_name(self):
        return self.project_combo.currentText().strip()

    def get_selected_sequence(self):
        item = self.sequence_list.currentItem()
        return item.text() if item else ""

    def get_selected_shot(self):
        item = self.shot_list.currentItem()
        return item.text() if item else ""

    def get_selected_task(self):
        item = self.task_list.currentItem()
        return item.text() if item else ""

    def refresh_projects(self):
        base_path = self.get_base_path()

        self.project_combo.clear()
        self.sequence_list.clear()
        self.shot_list.clear()
        self.task_list.clear()
        self.current_path_label.setText("Current Selection: ")

        if not base_path:
            return

        project_names = list_project_folders(base_path)
        self.project_combo.addItems(project_names)

        if project_names:
            self.refresh_browser()

    def refresh_browser(self):
        base_path = self.get_base_path()
        project_name = self.get_project_name()

        self.sequence_list.clear()
        self.shot_list.clear()
        self.task_list.clear()
        self.current_path_label.setText("Current Selection: ")

        if not base_path or not project_name:
            return

        sequence_names = list_sequence_folders(base_path, project_name)
        self.sequence_list.addItems(sequence_names)

    def on_sequence_changed(self):
        base_path = self.get_base_path()
        project_name = self.get_project_name()
        sequence_name = self.get_selected_sequence()

        self.shot_list.clear()
        self.task_list.clear()

        if not base_path or not project_name or not sequence_name:
            self.update_current_selection_label()
            return

        shot_names = list_shot_folders(base_path, project_name, sequence_name)
        self.shot_list.addItems(shot_names)
        self.update_current_selection_label()

    def on_shot_changed(self):
        base_path = self.get_base_path()
        project_name = self.get_project_name()
        sequence_name = self.get_selected_sequence()
        shot_name = self.get_selected_shot()

        self.task_list.clear()

        if not base_path or not project_name or not sequence_name or not shot_name:
            self.update_current_selection_label()
            return

        task_names = list_task_folders(base_path, project_name, sequence_name, shot_name)
        self.task_list.addItems(task_names)
        self.update_current_selection_label()

    def update_current_selection_label(self):
        project_name = self.get_project_name()
        sequence_name = self.get_selected_sequence()
        shot_name = self.get_selected_shot()
        task_name = self.get_selected_task()

        parts = [project_name] if project_name else []

        if sequence_name:
            parts.append(sequence_name)
        if shot_name:
            parts.append(shot_name)
        if task_name:
            parts.append(task_name)

        display_text = "/".join(parts) if parts else ""
        self.current_path_label.setText("Current Selection: {}".format(display_text))

    def on_create_new_project_clicked(self):
        base_path = self.get_base_path()

        if not base_path:
            self.show_warning("Missing Base Path", "Please select a base path first.")
            return

        dialog = NewProjectDialog(self)
        result = dialog.exec()

        if not result:
            self.log_box.append("New project creation cancelled.")
            return

        project_name = dialog.get_project_name()

        if not project_name:
            self.show_warning("Missing Project Name", "Please enter a new project name.")
            return

        try:
            created_paths = create_new_project_with_default_structure(
                base_path=base_path,
                project_name=project_name,
                sequence_name="0010",
                shot_name="010",
                task_name="TEST",
                subfolders=self.default_folder_names,
            )

            self.log_box.clear()
            self.log_box.append("Created new project:\n")
            for path in created_paths:
                self.log_box.append(path)

            self.refresh_projects()

            index = self.project_combo.findText(project_name)
            if index >= 0:
                self.project_combo.setCurrentIndex(index)

            self.show_info("Success", "New project created successfully.")

        except Exception as e:
            self.show_error("Error", str(e))

    def on_create_script_clicked(self):
        base_path = self.get_base_path()
        project_name = self.get_project_name()

        if not base_path:
            self.show_warning("Missing Base Path", "Please select a base path.")
            return

        if not project_name:
            self.show_warning("Missing Project Name", "Please select a project.")
            return

        try:
            script_path = create_initial_nuke_script(base_path, project_name)

            self.log_box.append("")
            self.log_box.append("Created Nuke script:")
            self.log_box.append(script_path)

            self.show_info("Success", "Nuke script created successfully.")

        except Exception as e:
            self.show_error("Error", str(e))