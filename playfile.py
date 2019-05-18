import re
from objects import *
from audiolazy import AudioIO
import os
import numpy as np
import math
import threading
import defusedxml.ElementTree as ET
from defusedxml.ElementTree import ParseError
import pygame

pygame.mixer.pre_init(44100, -16, 1)
pygame.mixer.init()

#p = PyAudio()

chrestEvent = threading.Event()
				
def playMusic(music, meta):
	for beat in music.iter("beat"):
		sounds = []
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
					n.duration = float(duration.text)
				else:
					raise InvalidValueError("Note duration values must be a decimal or integer number.")
			except AttributeError:
				raise MissingElementError("Notes must have a defined duration using the <duration> tag.")

			if letterGroups[1]:
				n.octave = int(letterGroups[1])
			else:
				octaveText = None
				try:
					octaveText = note.find("octave").text
				except AttributeError:
					pass
				if octaveText:
					if FILTERS["int"].match(octaveText):
						n.octave = int(octaveText)
				else:
					n.octave = 4

			n.setFrequency(meta.tuning, meta.key)

			#sound = pygame.sndarray.make_sound(np.sin(2*np.pi*np.arange(22050*60/n.duration*meta.tempo)*n.hz/22050))

			n_samples = int(round(n.duration*60/meta.tempo*44100))
			buf = np.zeros((n_samples), dtype=np.int16)
			max_sample = 2**(16-1) - 1

			for s in range(n_samples):
				t = float(s)/44100

				buf[s] = int(round(max_sample*math.sin(2*math.pi*n.hz*t)))

			#t = threading.Thread(target=player.play, args=(samples), kwargs={'rate':11025})
			sound = pygame.sndarray.make_sound(buf)
			sound.set_volume(.4)
			sounds.append(sound)

		for s in sounds:
			s.play()
			#t = threading.Thread(target=s.play, args=())
			#t.run()
		time.sleep(60/meta.tempo)

		'''print("""Note:
	Letter: %s
	Duration: %s
	Octave: %s
	Frequency: %s
	Groups: %s
		%s
				""" % (n.letter, str(n.duration), str(n.octave), str(n.hz), str(letterGroups), str(letterGroups)))'''

def mainMenu():
	#stream = p.open(format=pyaudio.paFloat32, channels=1, rate=11025, output=True)
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
				meta.tempo = int(tempo.text)
				print(type(meta.tempo))
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
				meta.tuning = float(tuning.text)
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
