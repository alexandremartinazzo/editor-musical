# sound.py
# Get sound's events

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
        pass
    
    def send(self, soundEvent):
        type, properties = soundEvent.type, soundEvent.properties
        if type == 1:
            note, octave = properties
            print "PLAY SINGAL --> playing %s octave %s" % (note,octave)
        elif type == 2:
            print "STOP SIGNAL --> nothing is playing now"
        elif type == 3:
            note, octave, x = properties
            print "PLAY FOR SIGNAL --> playing %s octave %s for %s seconds" % (note,octave,x)
            