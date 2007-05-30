# MusicalEditorActivity.py
# Running Musical Editor as a XO activity

from sugar.activity import activity

import sys, os
sys.path.append(os.path.join(activity.get_bundle_path(), "structure"))
sys.path.append(os.path.join(activity.get_bundle_path(), "gui"))
sys.path.append(os.path.join(activity.get_bundle_path(), "sound"))
import gui, base, information
import gtk

class MusicalEditorActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.hide()
        self.information = information.Information()
        self.interface = gui.Interface(self.information.octaveList)
        self.base = base.Base(self.interface, self.information)
        self.add(self.interface.fixed)
        self.set_title('Musical Editor')
        self.show()
