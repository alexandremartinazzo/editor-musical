# instruments.py
# Where the instruments' menu is build and managed.
try:
    from sugar.activity import activity
    sugar = True
except: sugar = False
import gtk,os
    
class Menu:
    def __init__(self, base):
        self.instruments = base.gui.grid.positions
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
            self.base.gui.grid.instrumentPosition = position # current active instrument index
            self.instruments[position] = instrument
            self.rebuildMenu()

    def changeInstrument(self, widget, position):
        instrument = self.base.gui.selectInstrument()
        if instrument:
            instrumentBefore = self.instruments[position]
            if self.base.gui.grid.instrument == instrumentBefore: self.base.gui.grid.instrument = instrument
            self.instruments[position] = instrument # set the new instrument
            for octave in range(1,8):
                try:
                    self.base.gui.grid.octaveList.octaveList[octave][instrument] = self.base.gui.grid.octaveList.octaveList[octave][instrumentBefore]
                    del self.base.gui.grid.octaveList.octaveList[octave][instrumentBefore]
                except: pass
            self.base.gui.grid.changeOctave()
            self.rebuildMenu()
       
    def rebuildMenu(self, position_to_delete = None):
        self.base.gui.instrumentsImage.clear()
        name = self.base.gui.grid.instrument
        if name:
            if sugar: self.base.gui.instrumentsImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/instruments/" + name + '.png'))
            else: self.base.gui.instrumentsImage.set_from_file('pixmaps/instruments/' + name + '.png')
        else:
            if sugar: self.base.gui.instrumentsImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/instruments.png"))
            else: self.base.gui.instrumentsImage.set_from_file('pixmaps/instruments.png')
        self.base.gui.instrumentsImage.show()
        for position in range(1,11):
            instrument = self.instruments[position]
            if instrument:
                self.menuItem[position].remove_submenu()
                self.menuItem[position].get_children()[0].set_label(instrument)
                subMenu = gtk.Menu()
                if self.base.gui.grid.instrumentPosition != position:
                    stateItem = gtk.MenuItem("Ativar")
                    subMenu.append(stateItem)
                    stateItem.show()
                    stateItem.connect("activate", self.activateInstrument, position)
                changeItem = gtk.MenuItem("Trocar")
                subMenu.append(changeItem)
                changeItem.show()
                changeItem.connect("activate", self.changeInstrument, position)
                deleteItem = gtk.MenuItem("Excluir")
                subMenu.append(deleteItem)
                deleteItem.show()
                deleteItem.connect("activate", self.deleteInstrument, position) 
                self.menuItem[position].set_submenu(subMenu)
        if position_to_delete:
            self.menuItem[position_to_delete].remove_submenu()
            menuText = "Instrumento %s" % position_to_delete
            self.menuItem[position_to_delete].get_children()[0].set_label(menuText)
            subMenu = gtk.Menu()
            subMenuItem = gtk.MenuItem("Choose")
            subMenu.append(subMenuItem)
            subMenuItem.show()
            subMenuItem.connect("activate", self.chooseInstrument, position_to_delete)
            self.menuItem[position_to_delete].set_submenu(subMenu)
            subMenu.show()

    def activateInstrument(self, widget, position):
        self.base.gui.grid.instrument = self.instruments[position]
        self.base.gui.grid.instrumentPosition = position
        self.rebuildMenu()
    
    def deleteInstrument(self, widget, position):
        instrument = self.instruments[position]
        self.instruments[position] = None
        if instrument == self.base.gui.grid.instrument:
            self.base.gui.grid.instrument = None
            self.base.gui.grid.instrumentPosition = None                    
        for octave in range (1,8):
            try:
                del self.base.gui.grid.octaveList.octaveList[octave][instrument]
                del self.base.gui.grid.noteToPaint[instrument]
                self.base.gui.grid.setAction()
            except: pass
        self.rebuildMenu(position)
