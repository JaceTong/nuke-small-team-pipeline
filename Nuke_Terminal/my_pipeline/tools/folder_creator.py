import os


DEFAULT_SUBFOLDERS = [
    "assets",
    "plates",
    "comp",
    "render",
    "publish",
    "scripts",
    "reference",
]


def list_project_folders(base_path):
    if not os.path.exists(base_path):
        return []

    folders = []
    for name in os.listdir(base_path):
        full_path = os.path.join(base_path, name)
        if os.path.isdir(full_path):
            folders.append(name)

    folders.sort()
    return folders


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


def create_new_project_with_default_structure(
    base_path,
    project_name,
    sequence_name="0010",
    shot_name="010",
    task_name="TEST",
    subfolders=None,
):
    if subfolders is None:
        subfolders = DEFAULT_SUBFOLDERS

    project_root = os.path.join(base_path, project_name)
    task_root = os.path.join(project_root, sequence_name, shot_name, task_name)

    created_paths = []

    if os.path.exists(project_root):
        raise Exception("Project already exists:\n{}".format(project_root))

    os.makedirs(task_root, exist_ok=True)

    # 记录主结构
    created_paths.append(project_root)
    created_paths.append(os.path.join(project_root, sequence_name))
    created_paths.append(os.path.join(project_root, sequence_name, shot_name))
    created_paths.append(task_root)

    # 创建 task 下的默认文件夹
    for folder_name in subfolders:
        folder_path = os.path.join(task_root, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        created_paths.append(folder_path)

    return created_paths