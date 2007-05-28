################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

import gtk
    
class Menu:
    def __init__(self, base):
        self.base = base
        self.menu = gtk.Menu()
        self.menuItem = {}
        for position in range(1,11):
            # self.menuItem[position] = menuItem = gtk.MenuItem(menuText)
            menuText = "Instrument %s" % position
            self.menuItem[position] = gtk.MenuItem(menuText)
            self.menu.append(self.menuItem[position])
            self.menuItem[position].show()
            subMenu = gtk.Menu()
            subMenuItem = gtk.MenuItem("Choose")
            subMenu.append(subMenuItem)
            subMenuItem.show()
            subMenuItem.connect("activate", self.chooseInstrument, position)
            self.menuItem[position].set_submenu(subMenu)
            subMenu.show()
        self.menu.show()
        # Connecting the Instruments Box
        self.base.gui.instrumentsBox.connect_object("event", self.instrumentButton, self.menu)

    def instrumentButton(self, widget, event):
        if event.type == gtk.gdk.BUTTON_PRESS:
            if event.button == 1:
                widget.popup(None, None, None, event.button, event.time)
                return True
            return False
        
    def chooseInstrument(self, widget, position):
        #openTreeview = Treeview(position, self.base)
        self.base.gui.selectInstrument()
       
    def rebuildMenu(self, delete = None):
        for position in self.base.instrument.instruments.keys():
            instrument = self.base.instrument.instruments[position]
            nameOfInstrument = self.base.instrument.names[instrument]
            self.menuItem[position].remove_submenu()
            self.menuItem[position].get_children()[0].set_label(nameOfInstrument)
            subMenu = gtk.Menu()
            if self.base.information.activeInstrument != position:
                stateItem = gtk.MenuItem("Activate")
                subMenu.append(stateItem)
                stateItem.show()
                stateItem.connect("activate", self.activateInstrument, position)
            else:
                stateItem = gtk.MenuItem("Activated")
                subMenu.append(stateItem)
                stateItem.show()
            changeItem = gtk.MenuItem("Change Instrument")
            subMenu.append(changeItem)
            changeItem.show()
            changeItem.connect("activate", self.changeInstrument, position)
            deleteItem = gtk.MenuItem("Delete")
            subMenu.append(deleteItem)
            deleteItem.show()
            deleteItem.connect("activate", self.deleteInstrument, position) 
            self.menuItem[position].set_submenu(subMenu)
        if delete != None:
            position = delete
            self.menuItem[position].remove_submenu()
            menuText = "Instrument %s" % position
            self.menuItem[position].get_children()[0].set_label(menuText)
            subMenu = gtk.Menu()
            subMenuItem = gtk.MenuItem("Choose")
            subMenu.append(subMenuItem)
            subMenuItem.show()
            subMenuItem.connect("activate", self.chooseInstrument, position)
            self.menuItem[position].set_submenu(subMenu)
            subMenu.show()

    def activateInstrument(self, widget, position):
        self.base.information.activeInstrument = position
        #TODO: DIZER PARA O RESTO DOS MODULOS QUAL EH O NOVO INSTRUMENTO ATIVO
        self.rebuildMenu()

    def changeInstrument(self, widget, position):
        openTreeview = Treeview(position, self.base, change = True)
        
    def changeMenu(self, widget = None):
        self.rebuildMenu()
    
    def deleteInstrument(self, widget, position):
        self.base.instrument.delInstrument(position)
        noteToDelete = {}
        for octave in range(0, 7):
            for note in self.base.information.octavelist[octave]:
                try: 
                    del self.base.information.octavelist[octave][note][2][position]
                    if self.base.information.octavelist[octave][note][2] == {}:
                        try: noteToDelete[note] += [octave]
                        except: noteToDelete[note] = [octave]
                except: pass
        octaveList = self.base.information.octavelist[self.base.current_octave - 1]
        self.base.rebuild_base(octaveList, octaveList, 0, True)
        for note in noteToDelete.keys():
            for octave in noteToDelete[note]:
                del self.base.information.octavelist[octave][note]
        self.rebuildMenu(position)
        self.base.information.activeInstrument = None
        
class Instrument:
    def __init__(self, base):
        self.base = base
        self.instruments = {} # It organizes the instruments of the composition
        # Getting Instrument Names
        self.names = ["Acoustic Piano", "Electric Piano", "Harpsichord", "Clavinet", "CELESTE",
                      "Acoustic Guitar", "Distortion Guitar", "Violin", "Acoustic Bass", "Viola",
                      "Organ", "Sax", "Trumpet", "Flute", "Clarinet", 
                      "Voice", "Crystal"] # Name of instruments
        self.numbers = [0, 4, 6, 7, 8, 25, 30, 40, 32, 41, 18, 64, 56, 73, 71, 54, 98]
        # Setting the range of colors:
        color = {}
        for i in range(0,5):
            color[i] = gtk.gdk.Color(5911*i, int(65535*(0.8+0.05*i)), 7200*i) # Percussion color
        for i in range(5,10):
            color[i] = gtk.gdk.Color(int((0.8+0.05*(i-4))*65535), 5911*(i-4), 7196*(i-4)) # String color
        for i in range(10, 15):
            color[i] = gtk.gdk.Color(1000, 1000, 65500) # Blow color
        color[15] = gtk.gdk.Color(65535, 0, 50000) # Voice color
        color[16] = gtk.gdk.Color(0, 0, 0) # Crystal color
        self.colors = color # Each instrument has a color, and self.color organizes it

    def addInstrument(self, position, instrument):
        # position = the position (1-10 where) it was put
        # instrument = the related integer of the instrument
        self.instruments[position] = instrument
        self.base.information.instruments[position] = instrument
        
    def delInstrument(self, position):
        del self.instruments[position]
        del self.base.information.instruments[position]
        
class Treeview:
    def __init__(self, position, grid, change = False):
        self.position = position
        self.grid = grid
        self.window = grid.gui.mainwindow
        self.change = change
        
        # Create a window
        self.newwindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.newwindow.set_decorated(False)
        self.newwindow.set_position(gtk.WIN_POS_CENTER)
        self.newwindow.set_title("Choose an Instrument")
        self.newwindow.set_geometry_hints(min_width=200)
        self.newwindow.set_size_request(250,160)
        self.newwindow.set_transient_for(self.window)
                
        # Create a Fixed
        self.fixed = gtk.Fixed()
        self.fixed.show()
                
        # Create a scrolledwindow
        self.sWin = gtk.ScrolledWindow()
        self.sWin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.sWin.set_size_request(250,130)
        self.fixed.put(self.sWin, 0, 0)
                
        # List of items to display
        self.list = gtk.ListStore(int, str)
        for instr in range(0, 17):
            iter = self.list.append( (instr, self.grid.instrument.names[instr],) )
            self.list.set(iter)

        # The Treeview
        self.treeview = gtk.TreeView()
        model = self.treeview.get_selection()
        model.set_mode(gtk.SELECTION_SINGLE)
        r = gtk.CellRendererText()
        #r.set_property('cell-background', 'yellow')
        self.treeview.insert_column_with_attributes(-1, "Choose An Instrument", r, text=1)
        self.treeview.set_model(self.list)
                
        self.treeview.connect("cursor-changed", self.on_treeview_cursor_changed)
        self.treeview.show()
        self.sWin.add_with_viewport(self.treeview)
        self.sWin.show()
        self.newwindow.add(self.fixed)
        self.newwindow.show()

        # Create "OK" and "Cancel" buttons
        self.ok = gtk.Button("OK")
        self.ok.show()
        self.cancel = gtk.Button("Cancel")
        self.cancel.show()

        self.fixed.put(self.ok, 140, 131)
        self.fixed.put(self.cancel, 170, 131)

        self.ok.connect("button_press_event", self.callback_ok)
        self.cancel.connect("button_press_event", self.callback_cancel)

    def callback_ok(self, widget, data):           
        parameters = (self.position, self.data0, self.data1)
        if self.change:
            self.grid.refreshGrid(3, parameters)
        else:
            self.grid.refreshGrid(2, parameters)
        self.newwindow.destroy()

    def callback_cancel(self, widget, data):
        self.newwindow.destroy()
           
    def on_treeview_cursor_changed(self, treeview):
        s = treeview.get_selection()
        (ls, iter) = s.get_selected()
        if iter is None:
            print "nothing selected"
        else:
            self.data0 = ls.get_value(iter, 0)
            self.data1 = ls.get_value(iter, 1)
            Treeview.instrument = self.data0
            print "Selected:", self.data0, self.data1

