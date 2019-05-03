import audiere
import time
import threading

AUD_DEV = audiere.open_device()

SEMITONES = {
	"cs": 1,
	"df": 1,
	"dn": 2,
	"ds": 3,
	"ef": 3,
	"en": 4,
	"es": 5,
	"fn": 5,
	"fs": 6,
	"gf": 6,
	"gn": 7,
	"gs": 8,
	"af": 8,
	"an": 9,
	"as": 10,
	"bf": 10,
	"bn": 11,
	"bs": 12,
	"cf": 12
}

class Note:
	def __init__(self, letter="c", mod="", octave=5, duration=1):
		self.letter = letter
		self.mod = mod
		self.octave = int(octave)
		self.duration = float(duration)
	
	def play(self, a, tempo):
		n = SEMITONES[self.letter + self.mod]
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
	
	def play(self, a, tempo):
		n = SEMITONES[self.letter + self.mod]
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
