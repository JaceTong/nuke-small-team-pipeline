import nuke
from my_pipeline.launcher import show_pipeline_window

toolbar = nuke.menu("Nuke")
menu = toolbar.addMenu("LJ_Pipeline")
menu.addCommand("Open Pipeline Terminal", show_pipeline_window)