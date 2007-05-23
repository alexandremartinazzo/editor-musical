################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

# grid.py
# Grid is a new gtk widget created for this software

#TODO: CRIAR LISTA SELF.PAINTNOTES COM NOTAS PITADAS EM CADA OITAVA E MANDA
# ATUALIZA-LAS.
#FAZER TESTE NO XO PARA VER SE FICA LENTO NA HORA DE PINTAR (ATUALIZAR TUDO)

import gtk, gobject
import sound

class Grid(gtk.DrawingArea):
    def __init__(self):
        #gtk.DrawingArea.__init__(self)
        super(Grid,self).__init__()
        self.connect("expose_event", self.expose)
        self.connect("motion_notify_event", self.motionNotify)
        self.connect("button_press_event", self.buttonPress)
        self.connect("button_release_event", self.buttonRelease)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(61423,62708,52865))
        self.width = 6000
        self.height = 720
        self.set_size_request(self.width, self.height)
        self.columns = False
        self.paintNotes = False
        self.dragging = False
        self.lastCell = None
        self.currentOctave = 4
        self.octaveNotes = [None,[], [], [], [], [], [], [] ]
        self.show()
        self.soundCC = sound.SoundConnectionCenter()
        self.notes = ("c", "csus", "d", "dsus", "e", "f", "fsus", 
                 "g", "gsus", "a", "asus", "b")

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK)

    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
        self.paintContext = widget.window.cairo_create()
        self.paintContext.stroke()
        self.paintContext.save()
        self.draw(self.context)
        return False
    
    def buttonPress(self, widget, event):
        self.dragging = True
        self.lastCell = ( int(event.x)/60 , int(event.y)/60 )
        
        # Create a sound event
        soundEvent = sound.SoundEvent(1, (self.notes[self.lastCell[1]],self.currentOctave))
        self.soundCC.send(soundEvent)
        
        x = self.lastCell[0]*60 + 15
        y = self.lastCell[1]*60 + 20 # 20 is defined by instrument chosen number
        begin = (x,y)
        end = (x+30,y)
        self.setAction("note", (begin,end))
        
        
    def motionNotify(self, widget, event):
        if self.dragging:
            if int(event.x)/60 != self.lastCell[0] and int(event.y)/60 == self.lastCell[1]:
                # Cells at the same line
                self.lastCell = ( int(event.x)/60 , int(event.y)/60 )
                newEndx = self.lastCell[0]*60 + 45
                counter = 0
                for i in self.noteToPaint:
                    counter += 1
                oldEndx = self.noteToPaint[counter-1][1][0]
                if newEndx > oldEndx:
                    begin, end = self.noteToPaint[counter-1]
                    end = (newEndx, end[1])
                    self.noteToPaint[counter-1] = (begin,end)
                    self.setAction()

            elif int(event.y-1)/60 != self.lastCell[1]:
                # Create a sound event for stoping
                soundEvent = sound.SoundEvent(2)
                self.soundCC.send(soundEvent)
                
                # Cells at the same column
                self.lastCell = ( int(event.x)/60 , int(event.y)/60 )

                # Create a sound event for playing
                soundEvent = sound.SoundEvent(1, (self.notes[self.lastCell[1]],self.currentOctave))
                self.soundCC.send(soundEvent)
                
                x = self.lastCell[0]*60 + 15
                y = self.lastCell[1]*60 + 20 # 20 is defined by instrument chosen number
                begin = (x,y)
                end = (x+30,y)
                self.setAction("note", (begin,end))
            
    def buttonRelease(self, widget, event):
        self.dragging = False
        # Create a sound event for stoping
        soundEvent = sound.SoundEvent(2)
        self.soundCC.send(soundEvent)
        
    def draw(self, context):
        # Set the line's color and its width      
        context.set_source_rgb(0.6, 0.7, 0.6)
        context.set_line_width(1)
        
        # Create the columns border
        column = 0
        while(column<self.width):
            context.save()
            context.move_to(column, 0)
            context.line_to(column, self.height)
            column += 60
            context.stroke()
            context.restore()

        # Create the lines border
        line = 0
        while(line<self.height):
            context.save()
            context.move_to(0,line)
            context.line_to(self.width,line)
            line += 60
            context.stroke()
            context.restore()
            
        if self.columns:
            self.addColumns(self.quantityOfColumns)
        
        if self.paintNotes:
            self.drawNote()

    def setAction(self, event = None, properties = None):
        if event == "columns":
            self.columns = True
            self.quantityOfColumns = properties
        elif event == "note":
            self.paintNotes = True
            try:
                knownNote = False
                for note in self.noteToPaint:
                    if note == properties:
                        knownNote = True
                if not knownNote: self.noteToPaint += [properties]
            except:
                self.noteToPaint = [properties]
        
        alloc = self.get_allocation()
        rect = gtk.gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
        self.window.invalidate_rect(rect, True)
        self.window.process_updates(True)

    def addColumns(self, quantity):
        # Set the lines color and width      
        self.context.set_source_rgb(0.6, 0.7, 0.6)
        self.context.set_line_width(1)

        # New atributes
        column = self.width
        self.width += quantity*58
        line = 0

        # Line border
        while(line<self.height):
            self.context.save()
            self.context.line_to(column,line)
            self.context.line_to(self.width, line)
            line += 58
            self.context.stroke()
            self.context.restore()

        # Column border
        while column<self.width:
            self.context.save()
            self.context.move_to(column,0)
            self.context.line_to(column, self.height)
            column += 58
            self.context.stroke()
            self.context.restore()
        
    def drawNote(self):
        self.context.set_source_rgb(0, 0, 1)
        self.context.set_line_width(5)
        for note in self.noteToPaint:
            self.context.save()
            self.context.move_to(note[0][0],note[0][1])
            self.context.line_to(note[1][0],note[1][1])
            self.context.stroke()
            self.context.restore()

# Test the grid interface
if __name__ == "__main__":
    window = gtk.Window()
    grid = Grid()
    
    window.add(grid)
    window.connect("destroy", gtk.main_quit)
    window.show()

    gtk.main()
