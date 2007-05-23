#!/usr/bin/python
import csnd,time

class CsndPlayer(object):
	"""Classe que representa a instancia do csound. Recebe os sinais para tocar ou parar de tocar notas."""
	notas = {
		'c':66,
		'csus':70,
		'd':74,
		'dsus':78,
		'e':82,
		'f':88,
		'fsus':93,
		'g':99,
		'gsus':105,
		'a':110,
		'asus':117,
		'b':123,
	}
	def __init__(self,csd):
		"""csd: arquivo com as definicoes do(s) instrumento(s)"""
		self.cs = csnd.Csound() # nova instancia do Csound
		self.cs.Compile(csd) # Compila arquivo .csd 
		self.th = csnd.CsoundPerformanceThread(self.cs) # Inicializa uma thread executar para a partitura
	def play(self,note,octave=4):
		"""Toca 'note'. Pode receber a oitava, por padrao eh a 4"""
		if note not in self.notas.keys():
			return 1
		self.cs.SetChannel('freq', self.notas[note]*octave) # seta o canal freq de comunicacao com a instancia do csnd
		self.th.Play() 	# toca 
		return 0
	def pause(self):
		return self.th.Pause() #pausa o som
		

