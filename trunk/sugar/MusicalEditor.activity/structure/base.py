################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

# base.py
# This module is the data structure's base
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
