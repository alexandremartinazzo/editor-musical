#!/usr/bin/python

import time, os, pdb

try: 
	import csnd
except ImportError: 
	print "You need to install CSound and put csnd.py in your 'python2.x/site-package/' folder"
	import sys
	sys.exit(1)

# Some constants defined here. 

#NOTES
DO 		= 65.41
DOs		= 69.3
RE 		= 73.42
REs		= 77.78
MI 		= 82.41
FA 		= 87.31
FAs		= 92.50
SOL		= 98.00
SOLs		= 103.83
LA 		= 110.01
LAs		= 116.55
SI 		= 123.48

#INSTRUMENTS
SENO=[1,'']
SIMPLE_DRUM=[2,10000]
ORGAN=[3,300]
CLARINET=[4,7000]
HIHAT=[5,'']
"""
PIANO
ORGAN
GUITAR
DRUM
"""

class CsndPlayer(object):
	"""Classe que representa a instancia do csound. Recebe os sinais para tocar ou parar de tocar notas."""
	def __init__(self,csd):
		"""csd: arquivo com as definicoes do(s) instrumento(s)"""
		self.csd = csd
		self.playing  = False
		self.cs = csnd.Csound() # nova instancia do Csound
		self.cs.Compile(self.csd) # Compila arquivo .csd 
		self.th = csnd.CsoundPerformanceThread(self.cs) # Inicializa uma thread executar para a partitura
	
	def playInstr(self, instr, note, dur=1.0,octave=4,*args):
		"""Toca 'note'. Pode receber a oitava, por padrao eh a 4"""
		msg = "i %d 0 %f %f %s" % (instr[0], dur, note*octave,str(instr[1]))
		if args:
			msg = msg + " ".join([ str(x) for x in args ])
		self.th.InputMessage(msg)

		if not self.playing:
			self.th.Play() 	# toca
			self.playing = True
		return 0

	def play(self,instr,note=LA, octave=4): 
		self.playInstr(instr,note,30,octave)
		self.playing = True

	def stop(self):
		self.playing = False
		self.th.SetScoreOffsetSeconds(0)
		
if __name__ == "__main__":
	"""Exemplo de como usar o CsndPlayer"""
	player = CsndPlayer('instruments.csd')
	player.play(ORGAN,LA,4)
	raw_input()
	player.stop()
	player.play(ORGAN,RE,4)
	raw_input()
	player.stop()
	import sys
	sys.exit()
