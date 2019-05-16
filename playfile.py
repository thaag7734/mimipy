import re
from objects import *
#import pyaudio
#from pyaudio import PyAudio
import os
import threading
import defusedxml.ElementTree as ET
from defusedxml.ElementTree import ParseError

#p = PyAudio()

chrestEvent = threading.Event()
				
def playMusic(music, meta):
	for beat in music.iter("beat"):
		for note in beat.iter("note"):
			n = Note()

			n.letter = note.get("letter")
			letterMatch = FILTERS["letter"].match(n.letter)
			if not letterMatch:
				raise InvalidValueError("Note letter must be from A-G inclusive, with optional # or b modifier/octave number.")
			letterGroups = letterMatch.groups()

			duration = note.find("duration")
			try:
				if FILTERS["float"].match(duration.text):
					n.duration = float(duration)
				else:
					raise InvalidValueError("Note duration values must be a decimal or integer number.")
			except AttributeError:
				raise MissingElementError("Notes must have a defined duration using the <duration> tag.")

			if len(letterGroups) == 3:
				n.octave = int(letterGroups[2])
			else:
				octaveText = None
				try:
					octaveText = note.find("octave").text
				except AttributeError:
					pass
				if octaveText:
					if FILTERS["int"].match(octaveText):
						n.octave = int(note.find("octave").text)
				else:
					n.octave = 4

			n.setFrequency(meta.tuning, meta.key)

def mainMenu():
	#stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
	done = False
	while not done:
		filename = input("Enter path to file:\n")
		if os.path.isfile(filename):
			tree = ET.parse(filename)
			root = tree.getroot()

			meta = Meta(root.find("meta"))
			title = meta.meta.find("title")
			try:
				meta.title = title.text
			except AttributeError:
				raise MissingElementError("Title tag is missing from song metadata.")

			tempo = meta.meta.find("tempo")
			try:
				if not FILTERS["int"].match(tempo.text):
					raise InvalidValueError("Tempo must be an integer.")
				meta.tempo = tempo.text
			except AttributeError:
				raise MissingElementError("Tempo element is missing from song metadata.")

			key = meta.meta.find("key")
			try:
				if not FILTERS["keyletter"].match(key.text):
					raise InvalidValueError("Invalid value supplied for key element.")
				meta.key = key.text
			except AttributeError:
					raise MissingElementError("Key element is missing from song metadata.")
				
			tuning = meta.meta.find("tuning")
			try:
				if not FILTERS["float"].match(tuning.text):
					raise InvalidValueError("Tuning value must be a decimal or integer number.")
				meta.tuning = tuning.text
			except AttributeError:
				meta.tuning = 440

			music = root.find("music")

			print("Now playing: '%s'" % meta.title)
			playMusic(music, meta)

			done = True
		else:
			print("File '%s' does not exist." % filename)
	#stream.stop_stream()
	#stream.close()
	#p.terminate()

mainMenu()
