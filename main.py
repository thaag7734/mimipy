import re
from objects import *

done = False
music = Music()

while not done:
	origLine = input("Enter line:\n")
	line = origLine.lower()
	if re.search(r"^<[a-z0-9 =\"]+/>$", line):
		if re.search(r"^<note [a-z0-9 =\"]+/>$", line):
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
			music.add(note)
		elif re.search(r"^<chnote [a-z0-9 =\"]+/>$", line):
			chnote = ChNote()
			letterMatch = re.search(r"^.+ letter=\"([a-g])\"", line)
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
			music.add(chnote)
		elif re.search(r"^<rest [a-z0-9 =\"]+/>$", line):
			rest = Rest()
			letterMatch = re.search(r"^.+ letter=\"([a-g])\"", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d|\d)", line)
			if letterMatch:
				rest.letter = letterMatch[1]
			if durationMatch:
				rest.duration = durationMatch[1]
			music.add(rest)
		elif re.search(r"^<chrest [a-z0-9 =\"]+/>$", line):
			chrest = ChRest()
			letterMatch = re.search(r"^.+ letter=\"([a-g])\"", line)
			durationMatch = re.search(r"^.+ duration=((?:\d)\.\d|\d)", line)
			if letterMatch:
				chrest.letter = letterMatch[1]
			if durationMatch:
				chrest.duration = durationMatch[1]
			music.add(chrest)
		elif re.search(r"^<prop [a-z0-9 =\"]+/>$", line):
			prop = Properties()
			tempoMatch = re.search(r"^.+ tempo=(\d)", line)
			keyMatch = re.search(r"^.+ key=\"([a-g](?:[sfn])?)\"", line)
			tstopMatch = re.search(r"^.+ tstop=(\d)", line)
			tsbtmMatch = re.search(r"^.+ tsbtm=(\d)", line)
			tuningMatch = re.search(r"^.+ a=((?:\d)\.\d+|\d)", line)
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
			if tuningMatch:
				prop.a = tuningMatch[1]
			music.add(prop)
		elif re.search(r"^<chstep(?: )?/>$", line):
			chstep = ChStep()
			music.add(chstep)
		else:
			raise LineError("No supported tag found at line '%s'" % origLine)
	elif line == "done":
		done = True
		music.display()
	else:
		raise LineError("Malformed input at line '%s'" % origLine)
