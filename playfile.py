import re
from objects import Note, ChNote, Rest, ChRest, Properties, ChStep, LineError
import pyaudio
from pyaudio import PyAudio
import os
import threading

p = PyAudio()

chrestEvent = threading.Event()

FILTERS = {
	"float": re.compile(r"^(\d+|(?:\d+)?\.\d+)$"),
	"int": re.compile(r"^(\d+)$")
	}


				
def playMusic(music, p):

def mainMenu(p):
	stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
	done = False
	while not done:
		filename = input("Enter path to file:\n")
		if os.path.isfile(filename):
			#do xml init stuff here
			done = True
		else:
			print("File '%s' does not exist." % filename)
	stream.stop_stream()
	stream.close()
	p.terminate()

mainMenu(p)