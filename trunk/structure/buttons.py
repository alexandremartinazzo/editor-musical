# buttons.py
# Manage the interface's buttons
import gtk
class Buttons:
    def __init__(self, base):
        self.base = base
        # Connecting Open, Save, Save As Buttons
        base.gui.openBox.connect("button_press_event", self.open)
        base.gui.saveBox.connect("button_press_event", self.save)
        base.gui.saveAsBox.connect("button_press_event", self.saveAs)

        # Initialize Octaves' Togglebuttons
        base.gui.octave1.connect("toggled", self.togglegrid, 1)
        base.gui.octave2.connect("toggled", self.togglegrid, 2)
        base.gui.octave3.connect("toggled", self.togglegrid, 3)
        base.gui.octave4.connect("toggled", self.togglegrid, 4)
        base.gui.octave5.connect("toggled", self.togglegrid, 5)
        base.gui.octave6.connect("toggled", self.togglegrid, 6)
        base.gui.octave7.connect("toggled", self.togglegrid, 7)

        # Connecting Play/Stop Buttons
        #base.gui.playBox.connect("button_press_event", self.play)
        #base.gui.stopBox.connect("button_press_event", self.stop)

        # Connecting Show/Hide ToggleButton
        self.showNotes = True
        base.gui.notesBox.connect("button_press_event", self.exhibitnote)

        # Connecting AddMoreColumns Button
        base.gui.columnsBox.connect("button_press_event", self.addColumns)

    def open(self, widget, event):
        if event.button == 1:
            parentWindow = self.base.gui.fixed.get_parent()
            open = self.base.information.open(parentWindow)
            if open:
                self.base.gui.grid.octaveList.octaveList, self.base.gui.grid.positions, self.base.gui.grid.width = open
                self.base.instrumentMenu.instruments = self.base.gui.grid.positions
                self.base.gui.grid.instrument = None
                self.base.gui.grid.instrumentPosition = None
                self.base.gui.grid.column = 0
                self.base.gui.currentOctave = 4
                self.base.gui.grid.lastCell = None
                self.base.gui.grid.paintNotes = True
                self.base.gui.scrolledWindow.emit('scroll-child', gtk.SCROLL_START, True)
                self.base.gui.grid.changeOctave()
                self.base.instrumentMenu.rebuildMenu()

    def save(self, widget, event):
        if event.button == 1:
            self.base.information.save()

    def saveAs(self, widget, event):
        if event.button == 1:
            parentWindow = self.base.gui.fixed.get_parent()
            self.base.information.saveAs(parentWindow)
    
    def togglegrid(self, octave, number):
        """This function is resposible for not allowing the grid to have more than
        one octave activated"""
        old = self.base.gui.grid.currentOctave
        if octave.get_active():
            for i in range(1,8):
                if i != number:
                    self.base.octaves[i-1].set_active(False)
            self.base.gui.grid.currentOctave = number
            self.base.gui.grid.changeOctave()
        else:
            #This works if the user want to toggle off an octave
            is_active = 0
            for i in range(1,8):
                if self.base.octaves[i-1].get_active() == True:
                    is_active = number
            if is_active == 0:
                octave.set_active(True)

    def exhibitnote(self, widget, context):
        """This function shows or hide notes (Do, Do#, Re, ... , Si)"""
        if self.showNotes == True:
            # Hide them
            self.base.gui.viewport2.set_child_visible(False)
            self.base.gui.scrolledWindow.set_size_request(780, 738)
            self.showNotes = False
        else:
            # Show them
            self.base.gui.viewport2.set_child_visible(True)
            self.base.gui.scrolledWindow.set_size_request(720, 738)
            self.showNotes = True

    def addColumns(self, widget, context):
        numberOfColumnsToAdd = 50
        self.base.gui.grid.setAction("columns", numberOfColumnsToAdd)
