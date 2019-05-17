#import pyaudio
#from pyaudio import PyAudio
from musicutils import *
import time
import threading
import math
import numpy as np
import re

FILTERS = {
	"float": re.compile(r"^(\d+|(?:\d+)?\.\d+)$"),
	"int": re.compile(r"^(\d+)$"),
	"letter": re.compile(r"^([A-G](?:[#b])?(\d)?)$"),
	"keyletter": re.compile(r"^([A-G](?:[#b])?)$")
	}

#sine_tone() from here: https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python
def sine_tone(f, duration, stream):

	# generate samples, note conversion to float32 array
	samples = (np.sin(2*np.pi*np.arange(44100*duration)*f/44100)).astype(np.float32).tobytes()

	# play. May repeat with different volume values (if done interactively) 
	stream.write(samples)

	stream.write(b"0x80"*100)


class Note:
	def __init__(self, octave=4):
		self.octave = int(octave)

	def setFrequency(self, a, key):
		letterGroups = FILTERS["letter"].match(self.letter).groups()
		letter = self.letter
		mod = ""
		if len(letterGroups) == 3:
			mod = KEYS[key][self.letter[:-1]]
		letter = "".join(char for char in self.letter if not char.isdigit())
		n = SEMITONES[letter]
		octaveDiff = self.octave - 3
		self.hz = a*2**(((n+octaveDiff*12)-9)/12)

class Rest:
	def __init__(self, letter="b", duration=1):
		self.letter = letter
		self.duration = float(duration)
	
	def rest(self, tempo):
		time.sleep(60/tempo*self.duration)

class Meta:
	def __init__(self, meta):
		self.meta = meta
		self.title = None
		self.tempo = None
		self.tuning = 440

class MIMIError(Exception):
	pass

class InvalidValueError(MIMIError):
	pass

class MissingElementError(MIMIError):
	pass