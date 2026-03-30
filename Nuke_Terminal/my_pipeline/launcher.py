try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets

import importlib
import my_pipeline.ui.main_window
import sys


def reload_my_pipeline():
    modules = [
        (name, module)
        for name, module in sys.modules.items()
        if name.startswith("my_pipeline")
    ]
    modules.sort(key=lambda x: len(x[0]), reverse=True)

    for name, module in modules:
        try:
            importlib.reload(module)
            print(f"Reloaded: {name}")
        except Exception as e:
            print(f"Failed to reload {name}: {e}")






pipeline_window = None

def show_pipeline_window():
    global pipeline_window

    try:
        if pipeline_window is not None:
            pipeline_window.close()
    except Exception:
        pass

    reload_my_pipeline()

    pipeline_window = my_pipeline.ui.main_window.MyPipelineWindow()
    pipeline_window.show()
