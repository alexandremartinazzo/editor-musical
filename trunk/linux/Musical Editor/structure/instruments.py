################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

import gtk
    
class Menu:
    def __init__(self, base):
        self.instruments = [None,None,None,None,None,None,None,None,None,None,None]
        self.base = base
        self.menu = gtk.Menu()
        self.menuItem = {}
        for position in range(1,11):
            # self.menuItem[position] = menuItem = gtk.MenuItem(menuText)
            menuText = "Instrumento %s" % position
            self.menuItem[position] = gtk.MenuItem(menuText)
            self.menu.append(self.menuItem[position])
            self.menuItem[position].show()
            subMenu = gtk.Menu()
            subMenuItem = gtk.MenuItem("Escolha")
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
        instrument = self.base.gui.selectInstrument()
        if instrument:
            self.base.gui.grid.instrument = instrument # current active instrument
            self.base.information.activeInstrument = position # current active instrument index
            self.instruments[position] = instrument
            self.rebuildMenu()
       
    def rebuildMenu(self, delete = None):
        for position in range(1,11):
            instrument = self.instruments[position]
            self.menuItem[position].remove_submenu()
            self.menuItem[position].get_children()[0].set_label(instrument)
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
        if delete:
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
        self.rebuildMenu()

    def changeInstrument(self, widget, position):
        pass
    
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
