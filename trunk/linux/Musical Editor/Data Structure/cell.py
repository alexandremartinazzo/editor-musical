################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

import gtk
import MidiMaker
import gobject
import threading
from os import system

class Cell:
    """Cells' attributes, layout and methods""" 
    def __init__(self, grid):
        self.grid = grid
       
    def create(self, i, j):
        return CreateCell(i,j, self.grid)    
        
class CreateCell:
    """Cells' attributes, layout and methods"""
    lastLine = None
    lastColumn = None
    
    # Commom parameters
    composeIcon = gtk.gdk.pixbuf_new_from_file("pixmaps/composeCursor.png")
    clearIcon = gtk.gdk.pixbuf_new_from_file("pixmaps/clearCursor.png")
    selectIcon = gtk.gdk.pixbuf_new_from_file("pixmaps/selectCursor.png")
    targets = [("string", gtk.TARGET_SAME_APP, 13012005)] # 13012005 is a special number, it's an identifier
    color = gtk.gdk.Color(61423,62708,52865)
        
    def __init__(self, i, j, grid):
        self.grid = grid
        self.i = i # self.i is the grid and note column
        self.j = j # self.j is the grid column
        self.newj = j # self.newj is the note column

        # Cell's parameters
        self.cell_painted = False # if the cell is painted
        self.paintedInstr = {} # the list of instruments that interact with the cell (painted instruments)
        self.note = "(%s,%s)" % (self.i, self.j) # line, column of the note
        self.selected = False # if the cell is selected

        # Create an EventBox to each cell
        self.eventbox = gtk.EventBox()
        self.eventbox.set_size_request(30, 30)
        self.eventbox.modify_bg(gtk.STATE_NORMAL, CreateCell.color)
        self.eventbox.show()

        # Create a Fixed to each cell
        self.fixed = gtk.Fixed()
        self.fixed.put(self.eventbox, 0, 0)
        self.fixed.set_size_request(30,30)
        self.fixed.show()

        # The cells can be painted using drag and drop, so the cell is a source and a destination Widget
        self.fixed.drag_source_set(gtk.gdk.BUTTON1_MASK, CreateCell.targets, gtk.gdk.ACTION_COPY)
        self.fixed.drag_dest_set(gtk.DEST_DEFAULT_MOTION, CreateCell.targets, gtk.gdk.ACTION_COPY)
        #self.fixed.drag_source_set_icon_pixbuf(composeIcon)
        self.fixed.connect("button_press_event", self.event)
        self.fixed.connect("drag_motion", self.event)

    def event(self, widget = None, event = None, arg = None, *args):
        self.newj = self.j + self.grid.columnLimit[0]
        self.note = "(%s,%s)" % (self.i, self.newj)
        try:
            if arg == None:
                if event.type == gtk.gdk.BUTTON_PRESS:
                    if event.button == 1:
                        # Called button1 press event
                        self.callback("press")
            else:
                # called drag motion event
                self.callback() 
        except: pass
        
    def callback(self, event=None):
        lastNote = "(%s,%s)" % (CreateCell.lastLine, CreateCell.lastColumn)
        if self.note != lastNote or event == "press":
            try: paint = self.grid.information.octavelist[self.grid.current_octave - 1][self.note][2][self.grid.information.activeInstrument]
            except: paint = [False, True, False] 
            # paint defines where the cell is painted
            # the orientation is [left, midle, right]
            if event == None:
                if CreateCell.lastLine == self.i:
                    try: lastPaint = self.grid.information.octavelist[self.grid.current_octave - 1][lastNote][2][self.grid.information.activeInstrument]
                    except: lastPaint = [False, True, False]
                    if CreateCell.lastColumn == self.newj-1:
                        lastPaint[2] = True
                        paint[0] = True
                    elif CreateCell.lastColumn == self.newj+1:
                        lastPaint[0] = True
                        paint[2] = True
                    lastNote = "(%s,%s)" % (CreateCell.lastLine, CreateCell.lastColumn)
                    self.grid.information.octavelist[self.grid.current_octave - 1][lastNote][2][self.grid.information.activeInstrument] = lastPaint

            if self.grid.method == "select":
                    self.methodSelect()
            else:           
                if self.grid.information.activeInstrument == None:
                    print "Select an instrument"
                else:
                    if self.grid.method == "compose":
                        if event == "press":
                            playNote =  PlayThread(self.i,self.grid)
                            playNote.start()
                        elif CreateCell.lastLine != self.i:
                            playNote = PlayThread(self.i,self.grid, True)
                            playNote.start()
                        try:
                            instruments = self.grid.information.octavelist[self.grid.current_octave-1][self.note][2]
                            try: del instruments[self.grid.information.activeInstrument]
                            except: pass
                        except:
                            instruments = {}
                        instruments[self.grid.information.activeInstrument] = paint
                        if paint[0] == True or paint[2] == True:
                            parameters = (self.i, self.newj, self.grid.current_octave, instruments, CreateCell.lastLine, CreateCell.lastColumn)
                        else:
                            parameters = (self.i, self.newj, self.grid.current_octave, instruments)
                        self.grid.refreshGrid(0, parameters)
                    else:
                        # CLEAR THE CELL
                        if self.cell_painted == False:
                            print "This cell is already Clear"
                        else:
                            parameters = (self.i, self.newj, self.grid.current_octave, self.grid.information.activeInstrument)
                        self.grid.refreshGrid(1, parameters)
            CreateCell.lastLine = self.i
            CreateCell.lastColumn = self.newj        

    def method_compose(self, instruments):
        height = 3 # the height of the painted box that will appear in the cell
        self.method_clear("all")
        for position in instruments.keys():
            instrument = self.grid.instrument.instruments[position]
            self.paintedInstr[position] = gtk.EventBox()
            self.paintedInstr[position].modify_bg(gtk.STATE_NORMAL, self.grid.instrument.colors[instrument])
            width = 0
            # Setting the width and the position of the cells' paintings
            initialPosition = 8
            if instruments[position][0] == True:
                width += 8
                initialPosition = -1
            if instruments[position][1] == True:
                width += 15
            if instruments[position][2] == True:
                width += 8
            self.paintedInstr[position].set_size_request(width, height)
            self.fixed.put(self.paintedInstr[position], initialPosition, (position - 1)*height)
            self.paintedInstr[position].show()
        self.cell_painted = True

    def method_clear(self, instrument = None):
        if instrument == "all":
            for i in self.paintedInstr.keys():
                    self.paintedInstr[i].destroy()
                    del self.paintedInstr[i]
            self.cell_painted = False
        else:
            # Clear what active instrument has painted on cell
            self.paintedInstr[instrument].destroy()
            del self.paintedInstr[instrument]
            counter = 0
            for i in self.paintedInstr.keys():
                counter += 1
            if counter == 0:
                self.cell_painted = False

    def methodSelect(self):
        if self.selected == False:
            selectColor = gtk.gdk.Color(54334, 65335, 63797)
            self.eventbox.modify_bg(gtk.STATE_NORMAL, selectColor)
            self.selected = True 
            #try: self.grid.selectedCells[self.note] = [self.i, self.newj, self.grid.information.octavelist[self.grid.current_octave-1][note][2]]
            #except: self.grid.selectedCells[self.note] = [self.i, self.newj]
            self.grid.selectedCells[self.note] = [self.i, self.newj, self.grid.current_octave]
        else:
            self.eventbox.modify_bg(gtk.STATE_NORMAL, CreateCell.color)
            self.selected = False
            del self.grid.selectedCells[self.note]

gobject.threads_init()
class PlayThread(threading.Thread):
    def __init__(self, line, grid, continuous = False):
        super(PlayThread, self).__init__()
        self.quit = False
        self.grid = grid
        self.height = (11-line)+12*(self.grid.current_octave-1)
        self.continuous = continuous

    def makeMid(self):
        self.mm = MidiMaker.MidiMaker()
        self.mm.newMidi(1)
        position = self.grid.information.activeInstrument
        instrument = self.grid.instrument.instruments[position]
        numberInstrument = self.grid.instrument.numbers[instrument]
        self.mm.startTrack(0,numberInstrument)
        start = 0
        if self.continuous: end = 50*self.grid.information.metronome
        else: end = 5*self.grid.information.metronome
        self.mm.addNote(start, end, self.height)
        self.mm.make()

    def run(self):
        try: system("killall timidity")
        except: pass
        self.makeMid()
        self.mm.playTimidity()