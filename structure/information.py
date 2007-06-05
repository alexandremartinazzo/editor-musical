# information.py
# this module may save information from the activity
#TODO: manipular strings para arquivos com final .edi

import gtk
try:
    import cPickle as pickle
except ImportError:
    import pickle # fall back on Python version

class Information:
    def __init__(self):
        # This variables contain all the necessary information to reproduce the composition
        self.octaveList = [None, {},{},{},{},{},{},{}] # painted cells in each octave
        self.positions = [None,None,None,None,None,None,None,None,None,None,None] # index of instruments
        self.width = 6000 # grid's width

    def open(self, parentWindow):
        openDialog = Chooser(parentWindow, "open", 'Editor Musical', '*.edi')
        path = openDialog.run()
        openDialog.destroy()
        # Get the file
        if path == None:
            return False
        try:
            openFile = file(path, "r") # open the file for reading
            openObject = pickle.load(openFile)
            self.octaveList, self.positions, self.width = openObject
            self.path = path
            return openObject
        except:
            return False

    def save(self):
        if self.path:
            saveObject = (self.octaveList, self.positions, self.width) # the serializable object
            saveFile = file(self.path, "w") # open the archive for writing
            pickle.dump(saveObject, saveFile)

    def saveAs(self, parentWindow):
        saveObject = (self.octaveList, self.positions, self.width) # the serializable object
        saveDialog = Chooser(parentWindow, "save", 'Editor Musical', '*.edi')
        self.path = saveDialog.run()
        saveDialog.destroy()
        if self.path:
            self.path += ".edi"
            saveFile = file(self.path, "w") # open the archive for writing the saveObject
            pickle.dump(saveObject, saveFile)

class Chooser:
    __retorno = None
    def response_event(self, widget, data):
        if data == gtk.RESPONSE_OK:
            self.__retorno = self.dialog.get_filename()
        elif data == gtk.RESPONSE_CANCEL:
            self.__retorno = None
    def run(self):
        self.dialog.run()
        return self.__retorno
    
    def destroy(self):
        self.dialog.destroy()
    
    def __init__(self, parent, type = None, title=None, *mime):
        
        if type == "open": self.dialog = gtk.FileChooserDialog("Selecionar Arquivo",
                                                               parent,
                                                               gtk.FILE_CHOOSER_ACTION_OPEN)
        elif type == "save": self.dialog = gtk.FileChooserDialog("Selecionar Arquivo",
                                                               parent,
                                                               gtk.FILE_CHOOSER_ACTION_SAVE)
        self.dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OK,     gtk.RESPONSE_OK)
        if mime:
            filter = gtk.FileFilter()
            filter.set_name(title)
            for type in mime:
                filter.add_pattern(type)
            self.dialog.add_filter(filter)
        self.dialog.connect('response', self.response_event)
        
