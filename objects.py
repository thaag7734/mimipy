from pyaudio import PyAudio
from musicutils import *
import time
import threading
import math

#sine_tone() from here: https://stackoverflow.com/a/974291
def sine_tone(frequency, duration, volume=1, sample_rate=22050):
	n_samples = int(sample_rate * duration)
	restframes = n_samples % sample_rate
	
	stream = p.open(format=p.get_format_from_width(1), # 8bit
		channels=1, # mono
		rate=sample_rate,
		output=True)
	s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
	samples = (int(s(t) * 0x7f + 0x80) for t in range(n_samples))
	for buf in zip(*[samples]*sample_rate): # write several samples at a time
		stream.write(bytes(bytearray(buf)))

	# fill remainder of frameset with silence
	stream.write(b'\x80' * restframes)

	stream.stop_stream()
	stream.close()
	p.terminate()

class Note:
	def __init__(self, letter="c", mod="", octave=5, duration=1):
		self.letter = letter
		self.mod = mod
		self.octave = int(octave)
		self.duration = float(duration)
	
	def play(self, a, tempo, key):
		keyMod = self.mod
		if keyMod == "":
			keyMod = KEYS[key][self.letter]
		n = SEMITONES[self.letter + keyMod]
		octaveDiff = self.octave - 4
		hz = a*2**(((n+octaveDiff*12)-9)/12)
		sine_tone(hz, 60/tempo*self.duration)
		time.sleep(60/tempo*self.duration)
		
class ChNote:
	def __init__(self, letter="c", mod="", octave=5, duration=1):
		self.letter = letter
		self.mod = mod
		self.octave = int(octave)
		self.duration = float(duration)
	
	def play(self, a, tempo, key):
		keyMod = self.mod
		if keyMod == "":
			keyMod = KEYS[key][self.letter]
		n = SEMITONES[self.letter + keyMod]
		octaveDiff = self.octave - 4
		hz = a*2**(((n+octaveDiff*12)-9)/12)
		sine_tone(hz, 60/tempo*self.duration)

class Rest:
	def __init__(self, letter="b", duration=1):
		self.letter = letter
		self.duration = float(duration)
	
	def rest(self, tempo):
		time.sleep(60/tempo*self.duration)
		
class ChRest:
	def __init__(self, letter="f", duration=1):
		self.letter = letter
		self.duration = float(duration)
	
	def rest(self, tempo, e):
		restThread = threading.Thread(target=self.chrest, args=(tempo, e))
		
	def chrest(self, tempo, e):
		e.set()
		time.sleep(60/tempo*self.duration)
		e.clear()
		
class ChStep:
	def __init__(self):
		pass

class Properties:
	def __init__(self, tempo=80, key="c", tstop=4, tsbtm=4, a=440):
		self.tempo = int(tempo)
		self.key = key
		self.timesig = (int(tstop),int(tsbtm))
		self.a = float(a)

class Music:
	def __init__(self, prop=Properties()):
		self.musicList = []
		self.add(prop)

	def add(self, item):
		self.musicList.append(item)
		
	def display(self):
		print(self.musicList)
		for item in self.musicList:
			if type(item) is Note:
				print("Note: %s%s%s;%s" % (item.letter, item.mod, str(item.octave), str(item.duration)))
			elif type(item) is ChNote:
				print("ChNote: %s%s%s;%s" % (item.letter, item.mod, str(item.octave), str(item.duration)))
			elif type(item) is Rest:
				print("Rest: %s;%s" % (item.letter, str(item.duration)))
			elif type(item) is ChRest:
				print("Rest: %s;%s" % (item.letter, str(item.duration)))
			elif type(item) is Properties:
				print("Prop: %sbpm;%s;%s/%s" % (str(item.tempo), item.key, str(item.timesig[0]), str(item.timesig[1])))
			elif type(item) is ChStep:
				print("ChStep")

class LineError(Exception):
	pass
