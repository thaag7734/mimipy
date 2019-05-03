import audiere
import time
import threading

AUD_DEV = audiere.open_device()

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
		hz = a*2**((n-9)/12)
		self.t = AUD_DEV.create_tone(hz)
		self.t.play()
		time.sleep(60/tempo*self.duration)
		self.stop()
	
	def stop(self):
		self.t.stop()
		
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
		hz = a*2**((n-9)/12)
		self.t = AUD_DEV.create_tone(hz)
		self.t.play()
		stopThread = threading.Thread(target=self.stop, args=(tempo))
		stopThread.run()
	
	def stop(self, tempo):
		time.sleep(60/tempo*self.duration)
		self.stop()

class Rest:
	def __init__(self, letter="b", duration=1):
		self.letter = letter
		self.duration = float(duration)
		
class ChRest:
	def __init__(self, letter="f", duration=1):
		self.letter = letter
		self.duration = float(duration)
		
class ChStep:
	def __init__(self):
		pass

class Properties:
	def __init__(self, tempo=80, key="c", tstop=4, tsbtm=4, a=440):
		self.tempo = int(tempo)
		self.key = key
		self.timesig = (int(tstop),int(tsbtm))
		self.a = int(a)

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
