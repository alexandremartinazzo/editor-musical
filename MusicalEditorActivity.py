# MusicalEditorActivity.py
# Running Musical Editor as a XO activity

import sys, os, gtk
try:
    from sugar.activity import activity
    sugar = True
    sys.path.append(os.path.join(activity.get_bundle_path(), "structure"))
    sys.path.append(os.path.join(activity.get_bundle_path(), "gui"))
    sys.path.append(os.path.join(activity.get_bundle_path(), "sound"))
    import gui, base, information
    class MusicalEditorActivity(activity.Activity):
        def __init__(self, handle):
            activity.Activity.__init__(self, handle)
            self.hide()
            self.information = information.Information()
            self.interface = gui.Interface(self.information.octaveList)
            self.base = base.Base(self.interface, self.information)
            self.add(self.interface.fixed)
            self.set_title('Musical Editor')
            self.connect('key_press_event',self.interface.key_press)
            self.connect('key_release_event',self.interface.key_release)
            self.show()
            # Changes the mouse cursor
            #pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/cursor.png"))
            #cursor = gtk.gdk.Cursor(gtk.gdk.display_get_default(), pix, 0, 0)
            #self.interface.fixed.window.set_cursor(cursor)
except:
    sugar = False
    sys.path.append("structure")
    sys.path.append("gui")
    sys.path.append("sound")
    import gui, base, information
    class MusicalEditor:
        def __init__(self):
            self.information = information.Information()
            self.interface = gui.Interface(self.information.octaveList)
            self.base = base.Base(self.interface, self.information)
            self.createWindow()
        def createWindow(self):
            self.mainwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.mainwindow.set_title("Musical Editor")
            self.mainwindow.set_position(gtk.WIN_POS_CENTER)
            self.mainwindow.set_size_request(1200, 900)
            self.mainwindow.set_resizable(False)
            self.mainwindow.set_icon_from_file("pixmaps/icon.png")
            self.mainwindow.connect("destroy", self.interface.destroy)
            self.mainwindow.modify_bg(gtk.STATE_NORMAL, self.interface.bgcolor)
            self.mainwindow.set_decorated(False)
            self.mainwindow.add(self.interface.fixed)
            self.mainwindow.show_all()
            # Changes the mouse cursor
            pix = gtk.gdk.pixbuf_new_from_file("pixmaps/cursor.png")
            cursor = gtk.gdk.Cursor(gtk.gdk.display_get_default(), pix, 0, 0)
            self.interface.fixed.window.set_cursor(cursor)

# Initialize Musical Editor in a OS without sugar
if __name__ == "__main__" and not sugar:
    editor = MusicalEditor()
    gtk.main()
