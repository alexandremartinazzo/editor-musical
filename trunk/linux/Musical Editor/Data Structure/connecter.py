"""-------------------------------"""
""" File from the Musical Editor  """
""" For OLPC Educative Software   """
""" Author: Rafael Barbolo Lopes  """
""" Organization: LSI             """
""" Version: 0.1                  """
"""-------------------------------"""

# TRATAR ESTE ARQUIVO COMO SENDO CLASSE EVENTOS APENAS! E TRANSFERE EVENTOS DA APLICAÇÃO ATRAVÉS DA MESH!

import sys
from ConnectionCenter import ConnectionCenter

class Connecter:
    def __init__(self):
        self.connectioncenter = ConnectionCenter(13012005)
        self.connectioncenter.becomeMaster()
        #self.connectioncenter.setMaster("127.0.0.1")
        print "Ip da maquina: %s" % self.connectioncenter.ip

class Event:
    def __init__(self, type, parameters):
        """ Constants """
        self.PAINT_TYPE = 0 # parameters = (i,j,octave,instruments, i, j)
        self.CLEAR_TYPE = 1 # parameters = (i, j, octave, active_instrument)
        self.INSTR_SELECT_TYPE = 2 # parameters = Instrument Properties (position, instrument, name)
        self.CHANGE_INSTR = 3 # parameters = Instrument Properties (position, instrument, name)       
        """ Objects """
        self.type = type
        self.parameters = parameters
