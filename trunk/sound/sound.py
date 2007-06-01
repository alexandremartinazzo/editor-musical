# sound.py
# Get sound's events

from csound import *
try:
    from sugar.activity import activity
    sugar = True
except: sugar = False

class SoundEvent:
    def __init__(self, type, properties = None):
        self.PLAY_TYPE = 1        # Play a note untill receiveing a stop 
                                  # SoundEvent.
                                  # properties = (note,octave, instrument)

        self.STOP_TYPE = 2        # Stop playing everything
                                  # properties = None

        self.PLAYFORX_TYPE = 3    # Play a note for x seconds
                                  # properties = (note,octave, instrument, x)

        self.type = type          # type index
        self.properties = properties
     
class SoundConnectionCenter:
    def __init__(self):
        """ This class receives Sound's Events"""
        if sugar: csd = os.path.join(activity.get_bundle_path(),"sound/instruments.csd")
        else: csd = 'sound/instruments.csd'
        self.csound = CsndPlayer(csd)
        self.instruments = {'SENO':SENO,'SIMPLE_DRUM':SIMPLE_DRUM,'ORGAN':ORGAN,'CLARINET':CLARINET,'HIHAT':HIHAT}
        self.notes = {'DO':DO,'DOs':DOs,'RE':RE,'REs':REs,'MI':MI,'FA':FA,'FAs':FAs,'SOL':SOL,'SOLs':SOLs,'LA':LA,'LAs':LAs,'SI':SI}
    def send(self, soundEvent):
        type, properties = soundEvent.type, soundEvent.properties
        if type == 1:
            note, octave, instrument = properties
            dur = 0.5
            if instrument in self.instruments.keys():
                self.csound.playInstr(self.instruments[instrument],self.notes[note],dur,octave)
#        elif type == 2:
#           self.csound.stop()
        elif type == 3:
            note, octave, x, instrument = properties
            print "PLAY FOR SIGNAL --> playing %s octave %s for %s seconds" % (note,octave,x)
            
