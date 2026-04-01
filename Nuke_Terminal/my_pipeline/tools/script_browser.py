import os


def list_nuke_scripts(base_path, project_name, sequence_name, shot_name, task_name):
    task_path = os.path.join(base_path, project_name, sequence_name, shot_name, task_name)

    if not os.path.exists(task_path):
        return []

    scripts = []
    for name in os.listdir(task_path):
        full_path = os.path.join(task_path, name)
        if os.path.isfile(full_path) and name.lower().endswith(".nk"):
            scripts.append(name)

    scripts.sort()
    return scripts