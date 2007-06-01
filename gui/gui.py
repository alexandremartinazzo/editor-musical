# Gui.py
# This module is responsible for initializing the Graphical User Interface

try:
    from sugar.activity import activity
    sugar = True
except: sugar = False
import gtk,os
from gridInterface import Grid
import sound

class Interface:
    """This class builds the main window and its components"""
    def __init__(self, octaveList):
        # Some useful colors
        self.bgcolor = gtk.gdk.Color(64507,58596,32125)
        self.color1 = gtk.gdk.Color(40863, 47545, 56026)
        self.color2 = gtk.gdk.Color(40863, 49545, 59026)
        self.color3 = gtk.gdk.Color(53423,55708,48865)
        self.color4 = gtk.gdk.Color(61423,62708,52865)

        self.createFixed()
        self.createBackground() # the color is set to yellow
        self.createGrid(octaveList)
        self.createButtons()

        # parameters
        self.dragging = {}
        self.octaveNumbers = {'1':self.octave1,'2':self.octave2,'3':self.octave3,'4':self.octave4,'5':self.octave5,'6':self.octave6,'7':self.octave7}
        self.notesToPlay = {'a':11,'w':10,'s':9,'e':8,'d':7,'f':6,'t':5,'g':4,'y':3,'h':2,'u':1,'j':0}

    def destroy(self, widget = None, data = None):
        gtk.main_quit()
              
    def createFixed(self):
        """Create a fixed to put the objects in"""
        self.fixed = gtk.Fixed()
        self.fixed.set_size_request(1200,900)
        self.fixed.set_has_window(True)
        self.fixed.show()

    def key_press(self, widget, event):
        if event.string in self.octaveNumbers.keys():
            self.octaveNumbers[event.string].set_active(True)
        elif event.string == '[':
            octave = self.grid.currentOctave
            if octave > 1:
                self.octaveNumbers[str(octave-1)].set_active(True)
        elif event.string == ']':
            octave = self.grid.currentOctave
            if octave < 7:
                self.octaveNumbers[str(octave+1)].set_active(True)
        elif event.string in self.notesToPlay.keys():
            line = self.notesToPlay[event.string]
            column = self.grid.column
            self.dragging[event.string] = True
            paint = (column,line)
            self.grid.buttonPress(None,None,paint)
            self.grid.dragging = False
        elif gtk.gdk.keyval_name(event.keyval) == 'plus':
            self.grid.setAction("columns",50)
        elif gtk.gdk.keyval_name(event.keyval) in ('Left','Right'):
            key = gtk.gdk.keyval_name(event.keyval)
            if key == 'Left':
                if self.grid.column>0:
                    self.grid.column -= 1
            else:
                self.grid.column += 1
                for pressed_notes in self.dragging.keys():
                    line = self.notesToPlay[pressed_notes]
                    column = self.grid.column
                    paint = (column,line)
                    self.grid.motionNotify(None,None,paint)
                    
    def key_release(self, widget, event):
        if event.string in self.notesToPlay.keys():
            try: del self.dragging[event.string]
            except: pass
        

    def createBackground(self):
        self.background = gtk.Image()
        if sugar: self.background.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "background.png"))
        else: self.background.set_from_file('pixmaps/background.png')
        self.fixed.put(self.background, 0, 0)
        self.background.show()

    def createGrid(self, octaveList):
        # Create the Grid Interface
        self.grid = Grid(octaveList)

        # Create a ScrolledWindow
        self.scrolledWindow = gtk.ScrolledWindow(None,None)
        self.scrolledWindow.add_with_viewport(self.grid)
        self.scrolledWindow.set_size_request(720,738)
        self.scrolledWindow.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_NEVER)
        self.fixed.put(self.scrolledWindow, 360,30)
        self.scrolledWindow.show()
                
        # Create a Second Table to show/hide notes
        self.tablenotes = gtk.Table(12, 1, True)
        self.tablenotes.set_col_spacings(1)
        self.tablenotes.set_row_spacings(1)
        self.tablenotes.show()
        
        # Create a Second Viewport to show/hide notes
        self.viewport2 = gtk.Viewport()
        self.viewport2.modify_bg(gtk.STATE_NORMAL, self.color1)
        self.viewport2.set_size_request(60, 720)
        self.viewport2.add(self.tablenotes)
        self.fixed.put(self.viewport2, 1078, 30)
        self.viewport2.show()
        self.viewport2.set_child_visible(True)

        # Create notes' column
        notes = ("Si", "La#", "La", "Sol#", "Sol", "Fa#", "Fa", "Mi", "Re#", "Re", "Do#", "Do")
        for i in range(0,12):
            eventbox = gtk.EventBox()
            note = gtk.Label()
            note.set_markup("<span font_family='arial' size='8000' color = '#0f70e8'><b>%s</b></span>" % notes[i])
            eventbox.modify_bg(gtk.STATE_NORMAL, self.color4)
            eventbox.set_size_request(59,59)
            eventbox.add(note)
            note.show()
            eventbox.show()
            self.tablenotes.attach(eventbox, 0, 1, i, i+1)
        
        # Create the octaves' Toggle Buttons
        self.octave1 = gtk.ToggleButton("Do1", False)
        self.octave1.set_size_request(75, 56)
        self.octave1.set_focus_on_click(False)
        self.octave1.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave1.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave1.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave1.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave1, 293, 459)
        self.octave1.show()

        self.octave2 = gtk.ToggleButton("Do2", False)
        self.octave2.set_focus_on_click(False)
        self.octave2.set_size_request(75, 56)
        self.octave2.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave2.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave2.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave2.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave2, 293, 407)
        self.octave2.show()

        self.octave3 = gtk.ToggleButton("Do3", False)
        self.octave3.set_size_request(75, 56)
        self.octave3.set_focus_on_click(False)
        self.octave3.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave3.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave3.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave3.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave3, 293, 354)
        self.octave3.show()

        self.octave4 = gtk.ToggleButton("Do4", False)
        self.octave4.set_size_request(75, 56)
        self.octave4.set_focus_on_click(False)
        self.octave4.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave4.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave4.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave4.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave4, 293, 302)
        self.octave4.show()

        self.octave5 = gtk.ToggleButton("Do5", False)
        self.octave5.set_size_request(75, 56)
        self.octave5.set_focus_on_click(False)
        self.octave5.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave5.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave5.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave5.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave5, 293, 249)
        self.octave5.show()

        self.octave6 = gtk.ToggleButton("Do6", False)
        self.octave6.set_size_request(75, 56)
        self.octave6.set_focus_on_click(False)
        self.octave6.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave6.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave6.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave6.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave6, 293, 197)
        self.octave6.show()

        self.octave7 = gtk.ToggleButton("Do7", False)
        self.octave7.set_size_request(75, 56)
        self.octave7.set_focus_on_click(False)
        self.octave7.modify_bg(gtk.STATE_NORMAL, self.color3)
        self.octave7.modify_bg(gtk.STATE_ACTIVE, self.color4)
        self.octave7.modify_bg(gtk.STATE_PRELIGHT, self.color4)
        self.octave7.unset_flags(gtk.CAN_FOCUS)
        self.fixed.put(self.octave7, 293, 144)
        self.octave7.show()

    def createButtons(self):
        # Instruments Button
        self.instrumentsImage = gtk.Image()
        if sugar: self.instrumentsImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "instruments.png"))
        else: self.instrumentsImage.set_from_file('pixmaps/instruments.png')
        self.instrumentsImage.show()
        self.instrumentsBox = gtk.EventBox()
        self.instrumentsBox.add(self.instrumentsImage)
        self.instrumentsBox.set_visible_window(False)
        self.fixed.put(self.instrumentsBox, 75, 120)
        self.instrumentsBox.show()
       
        # Stop Button
        self.stopImage = gtk.Image()
        if sugar: self.stopImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "stop.png"))
        else: self.stopImage.set_from_file('pixmaps/stop.png')
        self.stopImage.show()
        self.stopBox = gtk.EventBox()
        self.stopBox.add(self.stopImage)
        self.stopBox.set_visible_window(False)
        self.fixed.put(self.stopBox, 38, 478)
        self.stopBox.show()

        # Play Button
        self.playImage = gtk.Image()
        if sugar: self.playImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "play.png"))
        else: self.playImage.set_from_file('pixmaps/play.png')
        self.playImage.show()
        self.playBox = gtk.EventBox()
        self.playBox.add(self.playImage)
        self.playBox.set_visible_window(False)
        self.fixed.put(self.playBox, 131, 478)
        self.playBox.show()

        # Show/Hide Notes Button
        self.notesImage = gtk.Image()
        if sugar: self.notesImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "notes.png"))
        else: self.notesImage.set_from_file('pixmaps/notes.png')
        self.notesImage.show()
        self.notesBox = gtk.EventBox()
        self.notesBox.add(self.notesImage)
        self.notesBox.set_visible_window(False)
        self.fixed.put(self.notesBox, 141, 553)
        self.notesBox.show()

        # More Columns Button
        self.columnsImage = gtk.Image()
        if sugar: self.columnsImage.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/" + "column.png"))
        else: self.columnsImage.set_from_file('pixmaps/column.png')
        self.columnsImage.show()
        self.columnsBox = gtk.EventBox()
        self.columnsBox.add(self.columnsImage)
        self.columnsBox.set_visible_window(False)
        self.fixed.put(self.columnsBox, 80, 300)
        self.columnsBox.show()        

        # Open Button
        self.openImage = gtk.image_new_from_stock(gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON)
        self.openImage.show()
        self.openBox = gtk.EventBox()
        self.openBox.add(self.openImage)
        self.openBox.set_visible_window(False)
        #self.fixed.put(self.openBox, 19, 28)
        self.openBox.show()   
            
        # Save Button
        self.saveImage = gtk.image_new_from_stock(gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON)
        self.saveImage.show()
        self.saveBox = gtk.EventBox()
        self.saveBox.add(self.saveImage)
        self.saveBox.set_visible_window(False)
        #self.fixed.put(self.saveBox, 75, 34)
        self.saveBox.show()

        # Save As Button
        self.saveAsImage = gtk.image_new_from_stock(gtk.STOCK_SAVE_AS, gtk.ICON_SIZE_BUTTON)
        self.saveAsImage.show()
        self.saveAsBox = gtk.EventBox()
        self.saveAsBox.add(self.saveAsImage)
        self.saveAsBox.set_visible_window(False)
        #self.fixed.put(self.saveAsBox, 113, 34)
        self.saveAsBox.show()

    def selectInstrument(self):
        dialog = InstrumentSelection(self.fixed.get_parent(), self.grid.soundCC)
        instrument = dialog.run()
        dialog.destroy()
        return instrument

class InstrumentSelection:
    def destroy(self):
        self.dialog.destroy()

    def __init__(self, parentWindow, csoundCC):
        self.__selected = None # selected instrument
        # Create a gtk.Dialog
        self.dialog = gtk.Dialog(None, parentWindow, gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL,
                            gtk.RESPONSE_REJECT))
        self.dialog.set_size_request(600,600)
        self.dialog.set_resizable(False)
        self.dialog.set_decorated(False)
        self.dialog.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(64507,58596,32125))
        self.dialog.connect('response', self.response_event)
        self.dialog.connect('key_press_event',self.key_press) 
        self.dialog.show()
        self.oct = 4
        self.notes=dict(a='DO',w='DOs',s='RE',e='REs',d='MI',f='FA',t='FAs',g='SOL',y='SOLs',h='LA',u='LAs',j='SI',c=500,v=2000,b=1000,n=3000)
        self.soundCC = csoundCC

        # Create a table to display instruments and put it in gtk.Dialog
        table = gtk.Table(5,5,True)
        self.dialog.vbox.add(table)
        table.show()

        # Add instument's buttons to the table
        images = ('CLARINET','ORGAN','SENO','SIMPLE_DRUM','HIHAT','contrabass','mellophone',
                  'trombone','guitar','trumpet','tuba','violin','sax','violoncelo','xylophone',                 
                  'timbale', 'guiter2','Lyre','MANDOLIN','Pupsing','flute1','Recorder1','grandPiano')
        i,j,k,l = (0,1,0,1)
        for name in images:
            image = gtk.Image()
            if sugar: image.set_from_file(os.path.join(activity.get_bundle_path(), "pixmaps/instruments/" + name + '.png'))
            else: image.set_from_file('pixmaps/instruments/' + name + '.png')
            button = gtk.Button()
            button.add(image)
            button.connect('button_press_event', self.select, name)
            image.show()
            button.show()
            if i==5:
                i,j = (0,1)
                k += 1
                l += 1
            table.attach(button, i, j, k, l)
            i += 1
            j += 1

    def select(self, widget, event, name):
        self.__selected = name

    def key_press(self, widget, event):
        if event.string == '[':
            self.oct-=1
            return 
        elif event.string == ']':
            self.oct+=1
            return
        elif event.string in ('1','2','3','4','5','6','7'):
            self.oct = int(event.string)
        elif event.string in self.notes.keys() and self.__selected:
            properties = (self.notes[event.string],self.oct, self.__selected)
            soundEvent = sound.SoundEvent(1, properties)
            self.soundCC.send(soundEvent)

    def response_event(self, widget, response_id):
        if response_id == gtk.RESPONSE_ACCEPT:
            widget.destroy()
        elif response_id == gtk.RESPONSE_REJECT:
            self.__selected = None
            widget.destroy()

    def run(self):
        self.dialog.run()
        return self.__selected

# Interface Test
if __name__ == "__main__":
    window = Interface()
    gtk.main()
