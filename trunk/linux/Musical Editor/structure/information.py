################################
# Project Name: Musical Editor #
# Author: Rafael Barbolo Lopes #
# Organization: LSI            #
# Project based on OLPC        #
################################

import gtk
try:
    import cPickle as pickle
except ImportError:
    import pickle # fall back on Python version

class Information:
    def __init__(self):
        self.octaveList = [None, {},{},{},{},{},{},{}] # It contains iformation of each octave
        self.instruments = {} # Dict of instruments added to composition with their position (1-10)
        self.activeInstrument = None # The active instrument
        self.metronome = 1000

    def open(self, parentWindow):
        openDialog = Arquivo(parentWindow, 'Musical Editor Files', '*.mef')
        path = openDialog.run()
        openDialog.destroy()
        # Get the file
        if path == None:
            return None
        openFile = file(path, "r") # open the file for reading
        openObject = pickle.load(openFile)
        self.octavelist, self.instruments = openObject
        return [self.octavelist, self.instruments]
    
    def save(self):
        saveObject = (self.octavelist, self.instruments) # the serializable object
        self.savePath = '/home/barbolo/Desktop/eclipsedevelopment/Musical editor/src/arquivos salvos/arquivo.mef'
        saveFile = file(self.savePath, "w") # open the archive for writing
        pickle.dump(saveObject, saveFile)
        
    def saveAs(self):
        saveObject = (self.octavelist, self.instruments) # the serializable object
        saveFile = file(self.savePath, "w") # open the archive for writing
        pickle.dump(saveObject, saveFile)        


class Arquivo:
    # Written by Alexandre Martinazzo
    __retorno = None
    
    def response_event(self, widget, data):
        #print widget, data
        if data == gtk.RESPONSE_OK:
            print 'arquivo selecionado:', "%s" % self.janela.get_filename()
            self.__retorno = self.janela.get_filename()
        elif data == gtk.RESPONSE_CANCEL:
            print 'cancelando operacao'
            self.__retorno = None
        
    def run(self):
        self.janela.run()
        return self.__retorno
    
    def destroy(self):
        self.janela.destroy()
    
    def __init__(self, parent, titulo_filtro=None, *mime):
        
        self.janela = gtk.FileChooserDialog("Selecionar Arquivo",
                                            parent,
                                            gtk.FILE_CHOOSER_ACTION_OPEN)
            
        # Usa os botoes padrao do GTK, e define um identificador para
        # reconhecer no tratamento do evento "response"
        self.janela.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OK,     gtk.RESPONSE_OK)
        
        # preciso descobrir como abrir arquivos em localizacoes remotas
        #if self.janela.get_property('local-only') == True:
        #    self.janela.set_property('local-only', False)
        
        # adiciona um filtro para abertura de arquivos
        if mime != None:
            filtro = gtk.FileFilter()
            filtro.set_name(titulo_filtro)
        
            for tipo in mime:
                filtro.add_pattern(tipo)
            self.janela.add_filter(filtro)
        
        self.janela.connect('response', self.response_event)
        
