#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
from csound import *

notes=dict(a=DO,
w=DOs,
s=RE,
e=REs,
d=MI,
f=FA,
t=FAs,
g=SOL,
y=SOLs,
h=LA,
u=LAs,
j=SI,
c=500,
v=2000,
b=1000,
n=3000)

class XOKeyBoard:
	""" interface para testar a classe CsndPlayer """
	oct=4
	playing = []
	def key_press(self,widget,event,data=None):
		if event.string == '[':
			self.oct-=1
			return 
		elif event.string == ']':
			self.oct+=1
			return
		if event.string in notes.keys() and event.string not in self.playing:
			self.playing.append(event.string)
			self.csound.play(ORGAN,notes[event.string],self.oct)
	def key_release(self,widget,event,data=None):
		if event.string in notes.keys() and event.string in self.playing:
			self.playing.pop(self.playing.index(event.string))
			self.csound.stop()
	def destroy(self, widget, data=None):
 		gtk.main_quit()
	def __init__(self):
		self.csound = CsndPlayer('instruments.csd')
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("key_press_event",self.key_press) 
		self.window.connect("key_release_event",self.key_release) 
		self.window.connect("destroy", self.destroy)
		self.window.show()
	def main(self):
		gtk.main()

if __name__ == "__main__":
	xkb = XOKeyBoard()
	xkb.main()
