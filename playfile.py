import re
from objects import Note, ChNote, Rest, ChRest, Properties, ChStep
import os
import threading

chrestEvent = threading.Event()

FILTERS = {
	"comment": re.compile(r"^<!--.+-->$"),
	"line": re.compile(r"^<[a-z0-9 =\"]+/>$"),
	"note": re.compile(r"^<note [a-z0-9 =\"]+/>$"),
	"chnote": re.compile(r"^<chnote [a-z0-9 =\"]+/>$"),
	"rest": re.compile(r"^<rest [a-z0-9 =\"]+/>$"),
	"chrest": re.compile(r"^<chrest [a-z0-9 =\"]+/>$"),
	"prop": re.compile(r"^<prop [a-z0-9 =\"]+/>$"),
	"chstep": re.compile(r"<chstep(?: )?/>"),
	
	"letter": re.compile(r"^.+ letter=\"([a-z])\""),
	"mod": re.compile(r"^.+ mod=\"([sfn])\""),
	"octave": re.compile(r"^.+ octave=(\d)"),
	"duration": re.compile(r"^.+ duration=((?:\d)\.\d+|\d)"),
	"tempo": re.compile(r"^.+ tempo=(\d)"),
	"key": re.compile(r"^.+ key=\"([a-g](?:[sfn])?)\""),
	"tstop": re.compile(r"^.+ tstop=(\d)"),
	"tsbtm": re.compile(r"^.+ tsbtm=(\d)"),
	"tuning": re.compile(r"^.+ a=((?:\d)\.\d+|\d)"),
	
}

def readToList(f):
	fileContent = []
	for line in f:
		if not (FILTERS["comment"].fullmatch(line.rstrip("\n")) or line.rstrip("\n") == ""):
			fileContent.append(line)
	f.close()
	return fileContent

def getLineObject(line, origLine):
	if FILTERS["line"].fullmatch(line):
		if FILTERS["note"].fullmatch(line):
			note = Note()
			letterMatch = FILTERS["letter"].search(line)
			modMatch = FILTERS["mod"].search(line)
			octaveMatch = FILTERS["octave"].search(line)
			durationMatch = FILTERS["duration"].search(line)
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
			letterMatch = FILTERS["letter"].search(line)
			modMatch = FILTERS["mod"].search(line)
			octaveMatch = FILTERS["octave"].search(line)
			durationMatch = FILTERS["duration"].search(line)
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
			letterMatch = FILTERS["letter"].search(line)
			durationMatch = FILTERS["duration"].search(line)
			if letterMatch:
				rest.letter = letterMatch[1]
			if durationMatch:
				rest.duration = durationMatch[1]
			return rest
		elif FILTERS["chrest"].fullmatch(line):
			chrest = ChRest()
			letterMatch = FILTERS["letter"].search(line)
			durationMatch = FILTERS["duration"].search(line)
			if letterMatch:
				chrest.letter = letterMatch[1]
			if durationMatch:
				chrest.duration = durationMatch[1]
			return chrest
		elif FILTERS["prop"].fullmatch(line):
			prop = Properties()
			tempoMatch = FILTERS["tempo"].search(line)
			keyMatch = FILTERS["key"].search(line)
			tstopMatch = FILTERS["tstop"].search(line)
			tsbtmMatch = FILTERS["tsbtm"].search(line)
			tuningMatch = FILTERS["tuning"].search(line)
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
			if tuningMatch:
				prop.a = tuningMatch[1]
			return prop
		elif FILTERS["chstep"].fullmatch(line):
			chstep = ChStep()
			return chstep
		else:
			raise LineError("No supported tag found at line '%s'" % origLine)
	elif not FILTERS["comment"].fullmatch(line):
		if line != "":
			raise LineError("Malformed input at line '%s'" % origLine)
				
def playList(content):
	global chrestEvent
	tempo = 0
	key = None
	timesig = (None, None)
	chQueue = []
	for line in content:
		obj = getObject(line.lower(), line)
		if type(obj) == Properties:
			tempo = obj.tempo
			key = obj.key
			timesig = obj.timesig
			a = obj.a
		elif type(obj) == Note:
			obj.play(a, tempo, key)
		elif type(obj) == ChNote:
			if not chrestEvent.isSet():
				obj.play(a, tempo, key)
		elif type(obj) == Rest:
			obj.rest(a, tempo)
		elif type(obj) == ChRest:
			obj.rest(a, tempo, e)

def mainMenu():
	done = False
	while not done:
		filename = input("Enter path to file:\n")
		if os.path.isfile(filename):
			playList(readToList(filename))
			done = True
		else:
			print("File '%s' does not exist." % filename)

mainMenu()
