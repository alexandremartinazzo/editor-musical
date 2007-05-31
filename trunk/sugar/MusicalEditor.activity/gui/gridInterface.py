################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

# grid.py
# Grid is a new gtk widget created for this software

import gtk, gobject
import sound

class Notes:
    def __init__(self, octaveList):
        self.octaveList = octaveList

    def create(self, column, line, octave, instrument):
        duration = 1 # duration: the number of cells the note is painted, helpful to differentiate 'dragging' from 'button press'
        try: self.octaveList[octave][instrument] += [(line, column, duration)]
        except: self.octaveList[octave][instrument] = [(line, column, duration)]

    def createDragging(self, column, line, octave, instrument):
        aux = len(self.octaveList[octave][instrument]) - 1
        oline, ocolumn, oduration = self.octaveList[octave][instrument][aux]
        self.octaveList[octave][instrument][aux] = (oline, ocolumn, oduration+1)

class Grid(gtk.DrawingArea):
    # Colors given by (Red, Green, Blue)
    STRING = (1,0,0) # Red
    PERCUSSION = (0,1,0) # Green
    BLOW = (1,0,1) # Purple
    OTHERS = (1,1,0) # Don't know yet
    INSTRUMENT_COLOR = {'SENO':STRING, 'SIMPLE_DRUM':PERCUSSION, 'HIHAT':PERCUSSION, 'ORGAN':PERCUSSION, 'contrabass':STRING,
                        'Lyre':STRING, 'violoncelo':STRING, 'MANDOLIN':STRING, 'guiter2':STRING, 'tuba':BLOW, 'Pupsing':OTHERS,
                        'grandPiano':PERCUSSION, 'flute1':BLOW, 'mellophone':BLOW, 'xylophone':PERCUSSION,'timbale':PERCUSSION,
                        'CLARINET':BLOW, 'Recorder1':BLOW, 'trombone':BLOW, 'trumpet':BLOW, 'sax':BLOW} # instrument colors
    def __init__(self, octaveList):
        #gtk.DrawingArea.__init__(self)
        super(Grid,self).__init__()
        self.octaveList = Notes(octaveList)
        self.connect("expose_event", self.expose)
        self.connect("motion_notify_event", self.motionNotify)
        self.connect("button_press_event", self.buttonPress)
        self.connect("button_release_event", self.buttonRelease)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(61423,62708,52865))
        self.width = 6000
        self.height = 720
        self.set_size_request(self.width, self.height)
        self.columns = False
        self.column = 0 # the last painted column
        self.paintNotes = False
        self.noteToPaint = {}
        self.dragging = False
        self.lastCell = None
        self.currentOctave = 4
        self.instrument = None # Name of the active instrument
        self.positions = [None,None,None,None,None,None,None,None,None,None,None] # index of instruments
        self.instrumentPosition = None # index of active instrument
        self.show()
        self.soundCC = sound.SoundConnectionCenter()
        self.notes = ("DO", "DOs", "RE", "REs", "MI", "FA", "FAs", 
                 "SOL", "SOLs", "LA", "LAs", "SI")

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

    def changeOctave(self):
        self.noteToPaint = {} # key:value >> instrument:[notes], note = (line,column,duration)
        octaveDict = self.octaveList.octaveList[self.currentOctave]
        for instrument in octaveDict:
            self.noteToPaint[instrument] = []
            position = self.positions.index(instrument)
            for properties in octaveDict[instrument]:
                line, column, duration = properties
                line = 12 - line
                column -= 1
                x = column*60 + 15 # Horizonatal center
                y = line*60 + (position-1)*6 + 3 # height defined by instrument index
                begin = (x,y)
                end = (x+30 + (duration-1)*60, y)
                self.noteToPaint[instrument] += [(begin,end)]
        self.setAction()

    def buttonPress(self, widget=None, event=None, paint=None):
        if self.instrument:
            self.dragging = True
            if paint:
                self.lastCell = paint
            else:
                self.lastCell = ( int(event.x)/60 , int(event.y)/60 )
            self.column = self.lastCell[0]
            self.octaveList.create(1 + self.lastCell[0], 12 - self.lastCell[1], self.currentOctave, self.instrument)
        
            # Create a sound event
            properties = (self.notes[self.lastCell[1]],self.currentOctave, self.instrument)
            soundEvent = sound.SoundEvent(1, properties)
            self.soundCC.send(soundEvent)

            position = self.positions.index(self.instrument)

            x = self.lastCell[0]*60 + 15 # Horizonatal center
            y = self.lastCell[1]*60 + (position-1)*6 + 3 # height defined by instrument index
            begin = (x,y)
            end = (x+30,y)
            self.setAction("note", (begin,end))
        
        
    def motionNotify(self, widget=None, event=None, paint = None):
        if self.dragging:
            if (int(event.x)/60 != self.lastCell[0] and int(event.y)/60 == self.lastCell[1]):
                # Cells at the same line
                self.lastCell = ( int(event.x)/60 , int(event.y)/60 )
                self.octaveList.createDragging(1 + self.lastCell[0], 12 - self.lastCell[1], self.currentOctave, self.instrument)
                newEndx = self.lastCell[0]*60 + 45
                counter = len(self.noteToPaint[self.instrument])
                oldEndx = self.noteToPaint[self.instrument][counter-1][1][0]
                if newEndx > oldEndx:
                    begin, end = self.noteToPaint[self.instrument][counter-1]
                    end = (newEndx, end[1])
                    self.noteToPaint[self.instrument][counter-1] = (begin,end)
                    self.setAction()
            elif int(event.y-1)/60 != self.lastCell[1]:
                # Create a sound event for stoping
                soundEvent = sound.SoundEvent(2)
                self.soundCC.send(soundEvent)
                
                # Cells at the same column
                self.lastCell = ( int(event.x)/60 , int(event.y)/60 )
                self.octaveList.create(1 + self.lastCell[0], 12 - self.lastCell[1], self.currentOctave, self.instrument)

                # Create a sound event for playing
                properties = (self.notes[self.lastCell[1]],self.currentOctave, self.instrument)
                soundEvent = sound.SoundEvent(1, properties)
                self.soundCC.send(soundEvent)

                position = self.positions.index(self.instrument)

                x = self.lastCell[0]*60 + 15
                y = self.lastCell[1]*60 + (position-1)*6 + 3 # height defined by instrument index
                begin = (x,y)
                end = (x+30,y)
                self.setAction("note", (begin,end))
        if paint:
            self.lastCell = paint
            self.octaveList.createDragging(1 + self.lastCell[0], 12 - self.lastCell[1], self.currentOctave, self.instrument)
            newEndx = self.lastCell[0]*60 + 45
            counter = len(self.noteToPaint[self.instrument])
            oldEndx = self.noteToPaint[self.instrument][counter-1][1][0]
            if newEndx > oldEndx:
                begin, end = self.noteToPaint[self.instrument][counter-1]
                end = (newEndx, end[1])
                self.noteToPaint[self.instrument][counter-1] = (begin,end)
                self.setAction()

    def buttonRelease(self, widget, event):
        self.dragging = False
        # Create an event to pause the sound
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
        if self.paintNotes:
            self.drawNote()

    def setAction(self, event = None, properties = None):
        if event == "columns":
            self.columns = True
            self.quantityOfColumns = properties
            self.width, self.height = self.get_size_request()
            self.width += self.quantityOfColumns*60
            self.set_size_request(self.width, self.height)
        elif event == "note":
            self.paintNotes = True
            try:
                knownNote = properties in self.noteToPaint[self.instrument] # Verify if the note is already painted
                if not knownNote: self.noteToPaint[self.instrument] += [properties]
            except:
                self.noteToPaint[self.instrument] = [properties]
        alloc = self.get_allocation()
        rect = gtk.gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
        self.window.invalidate_rect(rect, True)
        self.window.process_updates(True)
        
    def drawNote(self):
        self.context.set_line_width(5)
        for instrument in self.noteToPaint:
            r, g, b = Grid.INSTRUMENT_COLOR[instrument]
            self.context.set_source_rgb(r, g, b)
            for note in self.noteToPaint[instrument]:
                self.context.save()
                begin = note[0][0]
                end = note[1][0]
                if end - begin > 30:
                    self.context.move_to(note[0][0],note[0][1])
                    self.context.line_to(note[0][0]+30,note[0][1])
                    self.context.stroke()
                    self.context.restore()
                    self.context.save()
                    self.context.set_line_width(2)
                    self.context.move_to(note[0][0]+30,note[0][1])
                    self.context.line_to(note[1][0],note[1][1])
                else:
                    self.context.set_line_width(5)
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
