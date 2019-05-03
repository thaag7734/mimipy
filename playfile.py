import re
from objects import *

FILTERS = {
	"line": re.compile(r"^<[a-z0-9 =\"]+/>$"),
	"note": re.compile(r"^<note [a-z0-9 =\"]+/>$"),
	"chnote": re.compile(r"^<chnote [a-z0-9 =\"]+/>$"),
	"rest": re.compile(r"^<rest [a-z0-9 =\"]+/>$"),
	"chrest": re.compile(r"^<chrest [a-z0-9 =\"]+/>$"),
	"prop": re.compile(r"^<prop [a-z0-9 =\"]+/>$"),
	"chstep": re.compile(r"<chstep(?: )?/>")
}

def readToList(f):
	fileContent = [line.rstrip("\n") for line in f]
	f.close()
	return fileContent

def getLineObject(line, origLine):
	if FILTERS["line"].fullmatch(line):
		if FILTERS["note"].fullmatch(line):
			note = Note()
			letterMatch = re.search(r"^.+ letter=\"([a-z])\"", line)
			modMatch = re.search(r"^.+ mod=\"([sfn])\"", line)
			octaveMatch = re.search(r"^.+ octave=(\d)", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				note.letter = letterMatch[1]
			if modMatch:
				note.mod = modMatch[1]
			if octaveMatch:
				note.octave = octaveMatch[1]
			if durationMatch:
				note.duration = durationMatch[1]
			return note
		elif FILTERS["chnote"].fullmatch(line):
			chnote = ChNote()
			letterMatch = re.search(r"^.+ letter=\"([a-z])\"", line)
			modMatch = re.search(r"^.+ mod=\"([sfn])\"", line)
			octaveMatch = re.search(r"^.+ octave=(\d)", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				chnote.letter = letterMatch[1]
			if modMatch:
				chnote.mod = modMatch[1]
			if octaveMatch:
				chnote.octave = octaveMatch[1]
			if durationMatch:
				chnote.duration = durationMatch[1]
			return chnote
		elif FILTERS["rest"].fullmatch(line):
			rest = Rest()
			letterMatch = re.search(r"^.+ letter=\"([a-z])\"", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				rest.letter = letterMatch[1]
			if durationMatch:
				rest.duration = durationMatch[1]
			return rest
		elif FILTERS["chrest"].fullmatch(line):
			chrest = ChRest()
			letterMatch = re.search(r"^.+ letter=\"([a-z])\"", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d+|\d)", line)
			if letterMatch:
				chrest.letter = letterMatch[1]
			if durationMatch:
				chrest.duration = durationMatch[1]
			return chrest
		elif FILTERS["prop"].fullmatch(line):
			prop = Properties()
			tempoMatch = re.search(r"^.+ tempo=(\d)", line)
			keyMatch = re.search(r"^.+ key=\"([a-g](?:[sfn])?)\"", line)
			tstopMatch = re.search(r"^.+ tstop=(\d)", line)
			tsbtmMatch = re.search(r"^.+ tsbtm=(\d)", line)
			if tempoMatch:
				prop.tempo = tempoMatch[1]
			if keyMatch:
				prop.key = keyMatch[1]
			if keyMatch:
				if len(keyMatch[1]) > 1 and keyMatch[1][1] == "n":
					prop.key = keyMatch[1][0]
				else:
					prop.key = keyMatch[1]
			if tstopMatch:
				prop.tstop = tstopMatch[1]
			if tsbtmMatch:
				prop.tsbtm = tsbtmMatch[1]
			return prop
		elif FILTERS["chstep"].fullmatch(line):
			chstep = ChStep()
			return chstep
		else:
			raise LineError("No supported tag found at line '%s'" % origLine)
	else:
		if line != "":
			raise LineError("Malformed input at line '%s'" % origLine)
				
def playList(content):
	tempo = 0
	key = None
	timesig = (None, None)
	chList = []
	for line in content:
		obj = getObject(line.lower(), line)
		if type(obj) == Properties:
			tempo = obj.tempo
			key = obj.key
			timesig = obj.timesig
			a = obj.a
		elif type(obj) == Note:
			obj.play(a, tempo)
			
