import os


def create_project_structure(base_path, project_name, selected_folders):
    project_root = os.path.join(base_path, project_name)

    created_paths = []

    
    os.makedirs(project_root, exist_ok=True)
    created_paths.append(project_root)

    for folder_name in selected_folders:
        folder_path = os.path.join(project_root, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        created_paths.append(folder_path)

    return created_paths