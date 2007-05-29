# sound.py
# Get sound's events

#from csound import *

class SoundEvent:
    def __init__(self, type, properties = None):
        self.PLAY_TYPE = 1        # Play a note untill receiveing a stop 
                                  # SoundEvent.
                                  # properties = (note,octave)

        self.STOP_TYPE = 2        # Stop playing everything
                                  # properties = None

        self.PLAYFORX_TYPE = 3    # Play a note for x seconds
                                  # properties = (note,octave,x)
        
        self.type = type          # type = number related to type
        self.properties = properties
        
class SoundConnectionCenter:
    def __init__(self):
        """ This class receives Sound's Events"""
#        self.csound = CsndPlayer()
    
    def send(self, soundEvent):
        type, properties = soundEvent.type, soundEvent.properties
        if type == 1:
            note, octave = properties
 #           self.csound.play(ORGAN,note,1,octave)
#       elif type == 2:
#           self.csound.pause()
        elif type == 3:
            note, octave, x = properties
            print "PLAY FOR SIGNAL --> playing %s octave %s for %s seconds" % (note,octave,x)
            
