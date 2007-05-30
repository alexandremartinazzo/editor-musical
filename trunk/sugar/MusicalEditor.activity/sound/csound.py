#!/usr/bin/python
import csnd,time


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
	def __init__(self):
		"""csd: arquivo com as definicoes do(s) instrumento(s)"""
		self.playing  = False
		self.cs = csnd.Csound() # nova instancia do Csound
		self.cs.Compile('instruments.csd') # Compila arquivo .csd 
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

	def play(self):
		self.playing = True
		return self.th.Play()

	def stop(self):
		self.playing = False
		self.th.Stop()
		self.th = csnd.CsoundPerformanceThread(self.cs)
		
if __name__ == "__main__":
	"""Exemplo de como usar o CsndPlayer"""
	player = CsndPlayer()
	player.playInstr(SIMPLE_DRUM,LA,2,4)
	raw_input()
	player.stop()
	import sys
	sys.exit()
