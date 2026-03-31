import os


IGNORED_TOP_LEVEL_FOLDERS = {
    "assets",
    "plates",
    "comp",
    "render",
    "publish",
    "scripts",
    "reference",
}


def get_project_root(base_path, project_name):
    return os.path.join(base_path, project_name)


def list_sequence_folders(base_path, project_name):
    project_root = get_project_root(base_path, project_name)

    if not os.path.exists(project_root):
        return []

    folders = []
    for name in os.listdir(project_root):
        full_path = os.path.join(project_root, name)
        if os.path.isdir(full_path) and name not in IGNORED_TOP_LEVEL_FOLDERS:
            folders.append(name)

    folders.sort()
    return folders


def list_shot_folders(base_path, project_name, sequence_name):
    sequence_path = os.path.join(base_path, project_name, sequence_name)

    if not os.path.exists(sequence_path):
        return []

    folders = []
    for name in os.listdir(sequence_path):
        full_path = os.path.join(sequence_path, name)
        if os.path.isdir(full_path):
            folders.append(name)

    folders.sort()
    return folders


def list_task_folders(base_path, project_name, sequence_name, shot_name):
    shot_path = os.path.join(base_path, project_name, sequence_name, shot_name)

    if not os.path.exists(shot_path):
        return []

    folders = []
    for name in os.listdir(shot_path):
        full_path = os.path.join(shot_path, name)
        if os.path.isdir(full_path):
            folders.append(name)

    folders.sort()
    return folders