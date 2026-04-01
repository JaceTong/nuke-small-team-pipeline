import os


def list_nuke_scripts(base_path, project_name, sequence_name, shot_name, task_name):
    scripts_path = os.path.join(
        base_path,
        project_name,
        sequence_name,
        shot_name,
        task_name,
        "scripts"
    )

    if not os.path.exists(scripts_path):
        return []

    scripts = []
    for name in os.listdir(scripts_path):
        full_path = os.path.join(scripts_path, name)
        if os.path.isfile(full_path) and name.lower().endswith(".nk"):
            scripts.append(name)

    scripts.sort()
    return scripts