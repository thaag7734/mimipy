import re

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
	def __init__(self, tempo=80, key="c", tstop=4, tsbtm=4):
		self.tempo = int(tempo)
		self.key = key
		self.timesig = (int(tstop),int(tsbtm))

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

done = False
music = Music()

while not done:
	lineError = False
	line = input("Enter line:\n").lower()
	if not re.search(r"^<[a-z0-9 =\"]+/>$", line):
		lineError = True
	if not lineError:
		if re.search("^<note[a-z0-9 =\"]+/>$", line):
			note = Note()
			letterMatch = re.search("^.+letter=\"([a-z])\"", line)
			modMatch = re.search("^.+mod=\"([sfn])\"", line)
			octaveMatch = re.search("^.+octave=(\d)", line)
			durationMatch = re.search("^.+duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				note.letter = letterMatch[1]
			if modMatch:
				if modMatch[1] == "n":
					note.mod = ""
				else:
					note.mod = modMatch[1]
			if octaveMatch:
				note.octave = octaveMatch[1]
			if durationMatch:
				note.duration = durationMatch[1]
			music.add(note)
		elif re.search("^<chnote[a-z0-9 =\"]+/>$", line):
			chnote = ChNote()
			letterMatch = re.search("^.+letter=\"([a-g])\"", line)
			modMatch = re.search("^.+mod=\"([sfn])\"", line)
			octaveMatch = re.search("^.+octave=(\d)", line)
			durationMatch = re.search("^.+duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				chnote.letter = letterMatch[1]
			if modMatch:
				if modMatch[1] == "n":
					chnote.mod = ""
				else:
					chnote.mod = modMatch[1]
			if octaveMatch:
				chnote.octave = octaveMatch[1]
			if durationMatch:
				chnote.duration = durationMatch[1]
			music.add(chnote)
		elif re.search("^<rest[a-z0-9 =\"]+/>$", line):
			rest = Rest()
			letterMatch = re.search("^.+letter=\"([a-g])\"", line)
			durationMatch = re.search("^.+duration=((?:\d)\.\d|\d)", line)
			if letterMatch:
				rest.letter = letterMatch[1]
			if durationMatch:
				rest.duration = durationMatch[1]
			music.add(rest)
		elif re.search("^<chrest[a-z0-9 =\"]+/>$", line):
			chrest = ChRest()
			letterMatch = re.search("^.+letter=\"([a-g])\"", line)
			durationMatch = re.search("^.+duration=((?:\d)\.\d|\d)", line)
			if letterMatch:
				chrest.letter = letterMatch[1]
			if durationMatch:
				chrest.duration = durationMatch[1]
			music.add(chrest)
		elif re.search("^<prop[a-z0-9 =\"]+/>$", line):
			prop = Properties()
			tempoMatch = re.search("^.+tempo=(\d)", line)
			keyMatch = re.search("^.+key=\"([a-g](?:[sfn])?)\"", line)
			tstopMatch = re.search("^.+tstop=(\d)", line)
			tsbtmMatch = re.search("^.+tsbtm=(\d)", line)
			if tempoMatch:
				prop.tempo = tempoMatch[1]
			if keyMatch:
				if len(keyMatch[1]) > 1 and keyMatch[1][1] == "n":
					prop.key = keyMatch[1][0]
				else:
					prop.key = keyMatch[1]
			if tstopMatch:
				prop.tstop = tstopMatch[1]
			if tsbtmMatch:
				prop.tsbtm = tsbtmMatch[1]
			music.add(prop)
		elif re.search("^<chstep(?: )?/>", line):
			chstep = ChStep()
			music.add(chstep)
		else:
			lineError = True
	elif line == "done":
		done = True
		music.display()
	elif lineError:
		print("lineError")
