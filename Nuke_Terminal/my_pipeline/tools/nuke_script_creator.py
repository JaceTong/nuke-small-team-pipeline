import os
import nuke


def create_initial_nuke_script(base_path, project_name):
    scripts_dir = os.path.join(base_path, project_name, "scripts")

    if not os.path.exists(scripts_dir):
        raise Exception("Scripts folder does not exist. Please create project folders first.")

    script_name = f"{project_name}_comp_v001.nk"
    script_path = os.path.join(scripts_dir, script_name)

    if os.path.exists(script_path):
        raise Exception("Script already exists:\n" + script_path)

    nuke.scriptClear()
    nuke.scriptSaveAs(script_path)

    return script_path