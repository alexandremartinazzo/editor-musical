################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

# main.py
# Responsible for initializing the software

import sys
sys.path.append("Data Structure")
sys.path.append("gui")
import gui, base, information
import gtk

class MusicalEditor:
    def __init__(self):
        self.information = information.Information()
        self.gui = gui.Interface()
        self.grid = base.Base(self.gui, self.information)
        self.gui.mainwindow.show_all()

# Initialize Musical Editor
if __name__ == "__main__":
    editor = MusicalEditor()
    gtk.main()
    
