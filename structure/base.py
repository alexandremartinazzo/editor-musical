# base.py
# This module is the data structure's base and it makes conecctions between modules
import instruments
import buttons
           
class Base:
    def __init__(self, gui, information):
        """Initialize the grid"""
        self.gui = gui
        self.information = information
        self.octaves = [gui.octave1, gui.octave2, gui.octave3, gui.octave4, gui.octave5, gui.octave6, gui.octave7] # It's the list of octaves buttons
        self.method = None # can be "compose", "clear" or "select"
        self.gui.octave4.set_active(True)
        self.buttons = buttons.Buttons(self)
        self.instrumentMenu = instruments.Menu(self)
