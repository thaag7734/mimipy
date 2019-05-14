import pyaudio
from pyaudio import PyAudio
from musicutils import *
import time
import threading
import math
import numpy as np

#sine_tone() from here: https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python
def sine_tone(f, duration, stream):

	# generate samples, note conversion to float32 array
	samples = (np.sin(2*np.pi*np.arange(44100*duration)*f/44100)).astype(np.float32).tobytes()

	# play. May repeat with different volume values (if done interactively) 
	stream.write(samples)

	stream.write(b"0x80"*100)


class Note:
	def __init__(self, letter="c", octave=5, duration=1):
		self.letter = letter
		self.octave = int(octave)
		self.duration = float(duration)
	
	def play(self, a, tempo, key, p):
		sine_tone(hz, 60/tempo*self.duration, p)

	def setFrequency():
		if not self.letter[1]:
			letter = KEYS[key][self.letter]
		else:
			letter = self.letter
		n = SEMITONES[letter]
		octaveDiff = self.octave - 4
		hz = a*2**(((n+octaveDiff*12)-9)/12)

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

class MIMIError(Exception):
	pass

class InvalidValueError(MIMIError):
	pass

class MissingElementError(MIMIError):
	pass