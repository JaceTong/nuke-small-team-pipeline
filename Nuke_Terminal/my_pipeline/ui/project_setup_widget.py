import nuke

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

from my_pipeline.tools.folder_creator import create_project_structure


class FolderSelectionDialog(QtWidgets.QDialog):
    def select_all(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)


    def clear_all(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
    
    
    
    def __init__(self, folder_names, parent=None):
        super(FolderSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Folders to Create")
        self.resize(300, 300)

        self.checkboxes = {}
        self.build_ui(folder_names)

    def build_ui(self, folder_names):
        layout = QtWidgets.QVBoxLayout(self)

        info_label = QtWidgets.QLabel("Choose which folders to create:")
        layout.addWidget(info_label)

        for folder_name in folder_names:
            checkbox = QtWidgets.QCheckBox(folder_name)
            checkbox.setChecked(True)  
            self.checkboxes[folder_name] = checkbox
            layout.addWidget(checkbox)

        layout.addStretch()

        # ===== 新增：Select / Clear 按钮 =====
        select_row = QtWidgets.QHBoxLayout()

        self.select_all_button = QtWidgets.QPushButton("Select All")
        self.clear_all_button = QtWidgets.QPushButton("Clear All")

        select_row.addWidget(self.select_all_button)
        select_row.addWidget(self.clear_all_button)

        layout.addLayout(select_row)

        # ===== OK / Cancel =====
        button_row = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_row.addStretch()
        button_row.addWidget(self.ok_button)
        button_row.addWidget(self.cancel_button)

        layout.addLayout(button_row)

        # ===== 连接信号 =====
        self.select_all_button.clicked.connect(self.select_all)
        self.clear_all_button.clicked.connect(self.clear_all)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)




        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_selected_folders(self):
        selected = []
        for folder_name, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                selected.append(folder_name)
        return selected

## Add your folder preference here:

class ProjectSetupWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ProjectSetupWidget, self).__init__()
        self.default_folder_names = [
            "assets",
            "plates",
            "comp",
            "render",
            "publish",
            "scripts",
            "reference",
        ]
        self.build_ui()



## UI here:
    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        title = QtWidgets.QLabel("Project Setups")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        base_path_label = QtWidgets.QLabel("Base Path:")
        self.base_path_input = QtWidgets.QLineEdit()
        self.browse_button = QtWidgets.QPushButton("Browse")

        base_path_row = QtWidgets.QHBoxLayout()
        base_path_row.addWidget(self.base_path_input)
        base_path_row.addWidget(self.browse_button)

        project_name_label = QtWidgets.QLabel("Project Name:")
        self.project_name_input = QtWidgets.QLineEdit()
        self.project_name_input.setPlaceholderText("e.g. shortfilm_001")

        self.create_button = QtWidgets.QPushButton("Create Project Folders")

        self.log_box = QtWidgets.QTextEdit()
        self.log_box.setReadOnly(True)

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(base_path_label)
        layout.addLayout(base_path_row)
        layout.addWidget(project_name_label)
        layout.addWidget(self.project_name_input)
        layout.addSpacing(12)
        layout.addWidget(self.create_button)
        layout.addSpacing(12)
        layout.addWidget(QtWidgets.QLabel("Log:"))
        layout.addWidget(self.log_box)

        self.browse_button.clicked.connect(self.browse_folder)
        self.create_button.clicked.connect(self.on_create_clicked)

    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Base Folder")
        if folder:
            self.base_path_input.setText(folder)

    def on_create_clicked(self):
        base_path = self.base_path_input.text().strip()
        project_name = self.project_name_input.text().strip()

        if not base_path:
            nuke.message("Please select a base path.")
            return

        if not project_name:
            nuke.message("Please enter a project name.")
            return

        dialog = FolderSelectionDialog(self.default_folder_names, self)
        result = dialog.exec()

        if not result:
            self.log_box.append("Folder creation cancelled.")
            return

        selected_folders = dialog.get_selected_folders()

        if not selected_folders:
            nuke.message("Please select at least one folder.")
            return

        try:
            created_paths = create_project_structure(
                base_path,
                project_name,
                selected_folders
            )

            self.log_box.clear()
            self.log_box.append("Created folders:\n")
            for path in created_paths:
                self.log_box.append(path)

            nuke.message("Project folders created successfully.")

        except Exception as e:
            nuke.message("Failed to create project folders:\n{}".format(str(e)))