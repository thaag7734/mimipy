class Note:
	def __init__(self, letter="c", mod="", octave=5, duration=1):
		self.letter = letter
		self.mod = mod
		self.octave = int(octave)
		self.duration = float(duration)
		
class ChNote:
	def __init__(self, letter="c", mod="", octave=5, duration=1):
		self.letter = letter
		self.mod = mod
		self.octave = int(octave)
		self.duration = float(duration)

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
