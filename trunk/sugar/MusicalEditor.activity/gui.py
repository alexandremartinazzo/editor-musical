################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

# Gui.py
# This module is responsible for initializing the Graphical User Interface

from sugar.activity import activity
import gtk
from gridInterface import Grid
import os

class Interface:
    """This class builds the main window and its components"""
    def __init__(self):
        # Some useful colors
        self.bgcolor = gtk.gdk.Color(64507,58596,32125)
        self.color1 = gtk.gdk.Color(40863, 47545, 56026)
        self.color2 = gtk.gdk.Color(40863, 49545, 59026)
        self.color3 = gtk.gdk.Color(53423,55708,48865)
        self.color4 = gtk.gdk.Color(61423,62708,52865)
        
        self.createFixed()
        self.createBackground() # the color is set to yellow
        self.createGrid()
        self.createButtons()

        # Changes the mouse cursor
        #pix = gtk.gdk.pixbuf_new_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" +"composeCursor.png"))
        #cursor = gtk.gdk.Cursor(gtk.gdk.display_get_default(), pix, 0, 0)
        #self.fixed.window.set_cursor(cursor)
              
    def createFixed(self):
        """Create a fixed to put the objects in"""
        self.fixed = gtk.Fixed()
        self.fixed.set_size_request(1200,900)
        self.fixed.set_has_window(True)
        self.fixed.show()

    def createBackground(self):
        self.background = gtk.Image()
        self.background.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "background.png"))
        self.fixed.put(self.background, 0, 0)
        self.background.show()

    def createGrid(self):
        # Create the Grid Interface
        self.grid = Grid()

        # Create a ScrolledWindow
        self.scrolledWindow = gtk.ScrolledWindow(None,None)
        self.scrolledWindow.add_with_viewport(self.grid)
        self.scrolledWindow.set_size_request(720,738)
        self.scrolledWindow.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
        self.fixed.put(self.scrolledWindow, 360,30)
        self.scrolledWindow.show()
                
        # Create a Second Table to show/hide notes
        self.tablenotes = gtk.Table(12, 1, True)
        self.tablenotes.set_col_spacings(1)
        self.tablenotes.set_row_spacings(1)
        self.tablenotes.show()
        
        # Create a Second Viewport to show/hide notes
        self.viewport2 = gtk.Viewport()
        self.viewport2.modify_bg(gtk.STATE_NORMAL, self.color1)
        self.viewport2.set_size_request(60, 720)
        self.viewport2.add(self.tablenotes)
        self.fixed.put(self.viewport2, 1078, 30)
        self.viewport2.show()
        self.viewport2.set_child_visible(True)

        # Create notes' column
        notes = ("Si", "La#", "La", "Sol#", "Sol", "Fa#", "Fa", "Mi", "Re#", "Re", "Do#", "Do")
        for i in range(0,12):
            eventbox = gtk.EventBox()
            note = gtk.Label()
            note.set_markup("<span font_family='arial' size='15000' color = '#0f70e8'><b>%s</b></span>" % notes[i])
            eventbox.modify_bg(gtk.STATE_NORMAL, self.color4)
            eventbox.set_size_request(59,59)
            eventbox.add(note)
            note.show()
            eventbox.show()
            self.tablenotes.attach(eventbox, 0, 1, i, i+1)

        # Create the octaves' Toggle Buttons
        self.octave1 = gtk.ToggleButton("Do1", False)
        self.octave1.set_size_request(75, 56)
        self.octave1.set_focus_on_click(False)
        self.octave1.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave1.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave1.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave1.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave1, 293, 459)
        self.octave1.show()

        self.octave2 = gtk.ToggleButton("Do2", False)
        self.octave2.set_focus_on_click(False)
        self.octave2.set_size_request(75, 56)
        self.octave2.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave2.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave2.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave2.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave2, 293, 407)
        self.octave2.show()

        self.octave3 = gtk.ToggleButton("Do3", False)
        self.octave3.set_size_request(75, 56)
        self.octave3.set_focus_on_click(False)
        self.octave3.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave3.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave3.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave3.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave3, 293, 354)
        self.octave3.show()

        self.octave4 = gtk.ToggleButton("Do4", False)
        self.octave4.set_size_request(75, 56)
        self.octave4.set_focus_on_click(False)
        self.octave4.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave4.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave4.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave4.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave4, 293, 302)
        self.octave4.show()

        self.octave5 = gtk.ToggleButton("Do5", False)
        self.octave5.set_size_request(75, 56)
        self.octave5.set_focus_on_click(False)
        self.octave5.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave5.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave5.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave5.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave5, 293, 249)
        self.octave5.show()

        self.octave6 = gtk.ToggleButton("Do6", False)
        self.octave6.set_size_request(75, 56)
        self.octave6.set_focus_on_click(False)
        self.octave6.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave6.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave6.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave6.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave6, 293, 197)
        self.octave6.show()

        self.octave7 = gtk.ToggleButton("Do7", False)
        self.octave7.set_size_request(75, 56)
        self.octave7.set_focus_on_click(False)
        self.octave7.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave7.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave7.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave7.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave7, 293, 144)
        self.octave7.show()

    def createButtons(self):
        # Instruments Button
        self.instrumentsImage = gtk.Image()
        self.instrumentsImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "instruments.png"))
        self.instrumentsImage.show()
        self.instrumentsBox = gtk.EventBox()
        self.instrumentsBox.add(self.instrumentsImage)
        self.instrumentsBox.set_visible_window(False)
        self.fixed.put(self.instrumentsBox, 75, 150)
        self.instrumentsBox.show()
        
        # Compose Button
        self.composeImage = gtk.Image()
        self.composeImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "compose1.png"))
        self.composeImage.show()
        self.composeBox = gtk.EventBox()
        self.composeBox.add(self.composeImage)
        self.composeBox.set_visible_window(False)
        self.fixed.put(self.composeBox, 9, 253)
        self.composeBox.show()

        # Clear Button
        self.clearImage = gtk.Image()
        self.clearImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "clear1.png"))
        self.clearImage.show()
        self.clearBox = gtk.EventBox()
        self.clearBox.add(self.clearImage)
        self.clearBox.set_visible_window(False)
        self.fixed.put(self.clearBox, 75, 253)
        self.clearBox.show()

        # Select Button
        self.selectImage = gtk.Image()
        self.selectImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "select1.png"))
        self.selectImage.show()
        self.selectBox = gtk.EventBox()
        self.selectBox.add(self.selectImage)
        self.selectBox.set_visible_window(False)
        self.fixed.put(self.selectBox, 141, 244)
        self.selectBox.show()

        # Copy Button
        self.copyImage = gtk.Image()
        self.copyImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "copy.png"))
        self.copyImage.show()
        self.copyBox = gtk.EventBox()
        self.copyBox.add(self.copyImage)
        self.copyBox.set_visible_window(False)
        self.fixed.put(self.copyBox, 9, 356)
        self.copyBox.show()

        # Cut Button
        self.cutImage = gtk.Image()
        self.cutImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "cut.png"))
        self.cutImage.show()
        self.cutBox = gtk.EventBox()
        self.cutBox.add(self.cutImage)
        self.cutBox.set_visible_window(False)
        self.fixed.put(self.cutBox, 84, 356)
        self.cutBox.show()        

        # Paste Button
        self.pasteImage = gtk.Image()
        self.pasteImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "paste.png"))
        self.pasteImage.show()
        self.pasteBox = gtk.EventBox()
        self.pasteBox.add(self.pasteImage)
        self.pasteBox.set_visible_window(False)
        self.fixed.put(self.pasteBox, 169, 356)
        self.pasteBox.show()
       
        # Stop Button
        self.stopImage = gtk.Image()
        self.stopImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "stop.png"))
        self.stopImage.show()
        self.stopBox = gtk.EventBox()
        self.stopBox.add(self.stopImage)
        self.stopBox.set_visible_window(False)
        self.fixed.put(self.stopBox, 38, 478)
        self.stopBox.show()

        # Play Button
        self.playImage = gtk.Image()
        self.playImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "play.png"))
        self.playImage.show()
        self.playBox = gtk.EventBox()
        self.playBox.add(self.playImage)
        self.playBox.set_visible_window(False)
        self.fixed.put(self.playBox, 131, 478)
        self.playBox.show()

        # Show/Hide Notes Button
        self.notesImage = gtk.Image()
        self.notesImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "notes.png"))
        self.notesImage.show()
        self.notesBox = gtk.EventBox()
        self.notesBox.add(self.notesImage)
        self.notesBox.set_visible_window(False)
        self.fixed.put(self.notesBox, 141, 553)
        self.notesBox.show()


        # Open Button
        self.openImage = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON)
        self.openImage.show()
        self.openBox = gtk.EventBox()
        self.openBox.add(self.openImage)
        self.openBox.set_visible_window(False)
        self.fixed.put(self.openBox, 19, 28)
        self.openBox.show()   
            
        # Save Button
        self.saveImage = gtk.image_new_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON)
        self.saveImage.show()
        self.saveBox = gtk.EventBox()
        self.saveBox.add(self.saveImage)
        self.saveBox.set_visible_window(False)
        self.fixed.put(self.saveBox, 75, 34)
        self.saveBox.show()

        # Save As Button
        self.saveAsImage = gtk.image_new_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_BUTTON)
        self.saveAsImage.show()
        self.saveAsBox = gtk.EventBox()
        self.saveAsBox.add(self.saveAsImage)
        self.saveAsBox.set_visible_window(False)
        self.fixed.put(self.saveAsBox, 113, 34)
        self.saveAsBox.show()

# Interface Test
if __name__ == "__main__":
    window = Interface()
    gtk.main()
