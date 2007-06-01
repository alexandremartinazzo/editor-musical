# buttons.py
# Manage the interface's buttons

class Buttons:
    def __init__(self, base):
        self.base = base
        # Connecting Open, Save, Save As Buttons
        #base.gui.openBox.connect("button_press_event", self.open)
        #base.gui.saveBox.connect("button_press_event", self.save)
        #base.gui.saveAsBox.connect("button_press_event", self.saveAs)

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

    def open(self, widget, context):
        open = self.base.information.open(self.base.gui.mainwindow)
        if open != None:
            self.base.instrument.instruments = open[1]
            self.base.information.activeInstrument = None
            self.base.instrumentMenu.changeMenu()
            octave = self.base.information.octavelist[self.base.current_octave - 1]
            
            # TODO: CONSTRUIR NA GRADE A COMPOSICAO QUE FOI ABERTA
            #self.base.rebuild_grid(octave, octave, 0, True)
    
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
