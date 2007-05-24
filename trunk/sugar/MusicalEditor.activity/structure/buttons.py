################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

from sugar.activity import activity
import gtk, os

class Buttons:
    def __init__(self, grid):
        self.grid = grid
        self.copiedCells = {}
        self.method = None

        # Connecting Open, Save, Save As Buttons
        #grid.gui.openBox.connect("button_press_event", self.open)
        #grid.gui.saveBox.connect("button_press_event", self.save)
        #grid.gui.saveAsBox.connect("button_press_event", self.saveAs)

        # Initialize Octaves' Togglebuttons
        grid.gui.octave1.connect("toggled", self.togglegrid, 1)
        grid.gui.octave2.connect("toggled", self.togglegrid, 2)
        grid.gui.octave3.connect("toggled", self.togglegrid, 3)
        grid.gui.octave4.connect("toggled", self.togglegrid, 4)
        grid.gui.octave5.connect("toggled", self.togglegrid, 5)
        grid.gui.octave6.connect("toggled", self.togglegrid, 6)
        grid.gui.octave7.connect("toggled", self.togglegrid, 7)
        
        # Connecting Compose, Clear and Select Buttons
        grid.gui.composeBox.connect("button_press_event", self.callbackComposePress)
        grid.gui.composeBox.connect("button_release_event", self.callbackComposeRelease)
        grid.gui.clearBox.connect("button_press_event", self.callbackClearPress)
        grid.gui.clearBox.connect("button_release_event", self.callbackClearRelease)
        grid.gui.selectBox.connect("button_press_event", self.callbackSelectPress)
        grid.gui.selectBox.connect("button_release_event", self.callbackSelectRelease)

        # Connecting Copy, Cut and Paste Buttons:
        #grid.gui.copyBox.connect("button_press_event", self.copy)
        #grid.gui.cutBox.connect("button_press_event", self.cut)
        #grid.gui.pasteBox.connect("button_press_event", self.paste)
        
        # Connecting Play/Stop Buttons
        #grid.gui.playBox.connect("button_press_event", self.play)
        #grid.gui.stopBox.connect("button_press_event", self.stop)

        # Connecting Show/Hide ToggleButton
        self.showNotes = True
        grid.gui.notesBox.connect("button_press_event", self.exhibitnote)

        # Connecting AddMoreColumns Button
        grid.gui.columnsBox.connect("button_press_event", self.addColumns)

    def open(self, widget, context):
        open = self.grid.information.open(self.grid.gui.mainwindow)
        if open != None:
            self.grid.instrument.instruments = open[1]
            self.grid.information.activeInstrument = None
            self.grid.instrumentMenu.changeMenu()
            octave = self.grid.information.octavelist[self.grid.current_octave - 1]
            
            # TODO: CONSTRUIR NA GRADE A COMPOSICAO QUE FOI ABERTA
            #self.grid.rebuild_grid(octave, octave, 0, True)
    
    def togglegrid(self, octave, number):
        """This function is resposible for not allowing the grid to have more than
        one octave activated"""
        old = self.grid.currentOctave
        if octave.get_active():
            for i in range(1,8):
                if i != number:
                    self.grid.octaves[i-1].set_active(False)
            self.grid.currentOctave = number                
        else:
            #This works if the user want to toggle off an octave
            is_active = 0
            for i in range(1,8):
                if self.grid.octaves[i-1].get_active() == True:
                    is_active = number
            if is_active == 0:
                octave.set_active(True)

    def deselectAllButtons(self):
        self.grid.gui.composeImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"compose1.png"))
        self.grid.gui.clearImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"clear1.png"))
        self.grid.gui.selectImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"select1.png"))

    def callbackComposePress(self, widget, context):
        # Highlight the box
        self.deselectAllButtons()
        self.grid.gui.composeImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"compose2.png"))
        self.grid.method = "compose"
        
    def callbackComposeRelease(self, widget, context):
        # TODO: Mudar o Mouse no Sugar
        pass

    def callbackClearPress(self, widget, context):
        # Highlight the box
        self.deselectAllButtons()
        self.grid.gui.clearImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"clear2.png"))
        self.grid.method = "clear"
        
    def callbackClearRelease(self, widget, context):
        # TODO: MOUSE
        #pix = gtk.gdk.pixbuf_new_from_file("pixmaps/clearCursor.png")
        #cursor = gtk.gdk.Cursor(gtk.gdk.display_get_default(), pix, 0, 0)
        #self.grid.gui.fixed.gui.set_cursor(cursor)
        pass
    
    def callbackSelectPress(self, widget, context):
        # Highlight the box
        self.deselectAllButtons()
        self.grid.gui.selectImage.set_from_file(os.path.join(activity.get_bundle_path(), "gui/pixmaps/" +"select2.png"))
        self.grid.method = "select"
        
    def callbackSelectRelease(self, widget, context):
        # TODO: MOUSE
        pass

    def exhibitnote(self, widget, context):
        """This function shows or hide notes (Do, Do#, Re, ... , Si)"""
        if self.showNotes == True:
            # Hide them
            self.grid.gui.viewport2.set_child_visible(False)
            self.showNotes = False
        else:
            # Show them
            self.grid.gui.viewport2.set_child_visible(True)
            self.showNotes = True

    def addColumns(self, widget, context):
        numberOfColumnsToAdd = 100
        self.grid.gui.grid.setAction("columns", numberOfColumnsToAdd)
