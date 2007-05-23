"""-------------------------------"""
""" File from the Musical Editor  """
""" For OLPC Educative Software   """
""" Author: Rafael Barbolo Lopes  """
""" Organization: LSI             """
""" Version: 0.1                  """
"""-------------------------------"""

import gtk

class InstrumentSelection:
    """This class builds the Initial Window"""
    def __init__(self):
        self.createWindow()
        self.createFixed()

        self.window.show()

    # Changes the cursor
    
    def createWindow(self):
        """Create the Window"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(640,480)
        self.window.set_resizable(False)
        self.window.set_decorated(False)

    def createFixed(self):
        self.fixed = gtk.Fixed()
        self.fixed.set_size_request(640,480)
        self.window.add(self.fixed)
        self.fixed.show()
        
#Teste do módulo
selecao = InstrumentSelection()
gtk.main()