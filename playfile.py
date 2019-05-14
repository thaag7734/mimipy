import re
from objects import *
import pyaudio
from pyaudio import PyAudio
import os
import threading
import defusedxml.ElementTree as ET
from defusedxml.ElementTree import ParseError

p = PyAudio()

chrestEvent = threading.Event()

FILTERS = {
	"float": re.compile(r"^(\d+|(?:\d+)?\.\d+)$"),
	"int": re.compile(r"^(\d+)$"),
	"letter": re.compile(r"^([A-G](?:[#b])?)$")
	}


				
def playMusic(music, meta):
	for beat in music.iter("beat"):
		for note in beat.iter("note"):
			n = Note()
			n.letter = note.get("letter")
			if not FILTERS["letter"].match(n.letter):
				raise InvalidValueError("Note letter must be from A-G inclusive, with optional # or b modifier.")
			n.duration = note.find("duration").text
			try:
				n.octave = note.find("octave").text
			except ParseError:
				n.octave = 4
			n.setFrequency()
			

def mainMenu(p):
	stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
	done = False
	while not done:
		filename = input("Enter path to file:\n")
		if os.path.isfile(filename):
			tree = ET.parse(filename)
			root = tree.getroot()

			meta = Meta(root.find("meta"))
			meta.title = meta.meta.find("title").text
			if not meta.title:
				raise MissingElementError("Title tag is missing from song metadata.")
			meta.tempo = meta.meta.find("tempo").text
			if not FILTERS["int"].match(meta.tempo):
				raise InvalidValueError("Tempo must be an integer.")

			music = root.find("music")

			print("Now playing: '%s'" % meta.title)
			playMusic(music, meta)

			done = True
		else:
			print("File '%s' does not exist." % filename)
	stream.stop_stream()
	stream.close()
	p.terminate()

mainMenu(p)