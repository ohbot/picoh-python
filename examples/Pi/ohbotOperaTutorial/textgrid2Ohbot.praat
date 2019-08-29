#textgrid2Ohbot v. 1 by Emmanuel Ferragne

#sound file must have the same name as textgrid file
#this script and all files (including phonemeMapping.txt)
#should be in the same directory

#converts a textgrid file to a Python script that requires
#4 simultaneous threads on the Raspberry Pi:
#1) sound track play back
#2) lip movements
#3) head nods
#4) random eye blinks and left to right movements, and head turns

myGrid$ = chooseReadFile$: "Load textgrid file"
Read from file: "phonemeMapping.txt"
Read from file: myGrid$
gridName$ = selected$("TextGrid")
fileDuration = Get total duration
pyName$ = gridName$ + ".py"

checkOld = fileReadable(pyName$)
if checkOld = 1
	pauseScript: "An older version of " + pyName$ + " has been found and will be deleted"
	deleteFile: pyName$
endif

#start writing Python script
writeFileLine: pyName$, "from ohbot import ohbot"
appendFileLine: pyName$, "from threading import Thread"
appendFileLine: pyName$, "import pygame"
appendFileLine: pyName$, ""
appendFileLine: pyName$, "ohbot.reset()"
appendFileLine: pyName$, "pygame.mixer.init()"
appendFileLine: pyName$, "s = pygame.mixer.Sound(""" + gridName$ + ".wav" + """)"
appendFileLine: pyName$, ""
appendFileLine: pyName$, "def doPlay():"
appendFileLine: pyName$, tab$, "s.play()"
appendFileLine: pyName$, ""
appendFileLine: pyName$, "def doLips():"
#modify wait duration here for better sync with music
appendFileLine: pyName$, tab$, "ohbot.wait(0.05)"

#this bloc for lip sync
nbInter = Get number of intervals: 1
for i from 1 to nbInter
	selectObject: "TextGrid " + gridName$
	currentLabel$ = Get label of interval: 1, i
	currentStart = Get starting point: 1, i
	currentEnd = Get end point: 1, i
	currentDuration = currentEnd - currentStart
	selectObject: "Table phonemeMapping"
	checkSearch = Search column: "phoneme", currentLabel$
	if checkSearch <> 0
		topLipPos = Get value: checkSearch, "topLip"
		botLipPos = Get value: checkSearch, "bottomLip"
		appendFileLine: pyName$, tab$, "ohbot.move(4," + string$(topLipPos) + ")"
		appendFileLine: pyName$, tab$, "ohbot.move(5," + string$(botLipPos) + ")"
		appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(currentDuration) + ")"
	else
		appendFileLine: pyName$, tab$, "ohbot.move(4,5)"
		appendFileLine: pyName$, tab$, "ohbot.move(5,5)"
		appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(currentDuration) + ")"
		
	endif
endfor
appendFileLine: pyName$, ""

#second pass implementing head nods
#if vowel is longer than 0.8 s and
#shorter than 2.5 s, nod at vowel start
#if vowel duration >= 2.5 head moves
#up and down quickly
appendFileLine: pyName$, "def doNod():"
for i from 1 to nbInter
	selectObject: "TextGrid " + gridName$
	currentLabel$ = Get label of interval: 1, i
	currentStart = Get starting point: 1, i
	currentEnd = Get end point: 1, i
	currentDuration = currentEnd - currentStart
	selectObject: "Table phonemeMapping"
	checkSearch = Search column: "phoneme", currentLabel$
	if checkSearch <> 0
		if currentDuration > 0.8 and currentDuration < 2.5
			rndPos = randomInteger(3,7)
			appendFileLine: pyName$, tab$, "ohbot.move(0," + string$(rndPos) + ")"
			appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(currentDuration) + ")"
		elsif currentDuration >= 2.5
			rndPos = randomInteger(3,7)
			appendFileLine: pyName$, tab$, "ohbot.move(0," + string$(rndPos) + ")"
			appendFileLine: pyName$, tab$, "ohbot.wait(2)"
			remTime = currentDuration - 2
			numIter = remTime div 0.2
			remIter = remTime mod 0.2
			for jVibrato from 1 to numIter
				appendFileLine: pyName$, tab$, "ohbot.move(0," + string$(rndPos+1) + ")"
				appendFileLine: pyName$, tab$, "ohbot.wait(0.1)"
				appendFileLine: pyName$, tab$, "ohbot.move(0," + string$(rndPos) + ")"
				appendFileLine: pyName$, tab$, "ohbot.wait(0.1)"
			endfor
			appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(remIter) + ")"
				
			
		else
			appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(currentDuration) + ")"
		endif
	else
		appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(currentDuration) + ")"
		
	endif
endfor
appendFileLine: pyName$, ""

#bloc for emotions
#blinks, eye movements and head turns
#are randomly generated
appendFileLine: pyName$, "def doEmo():"
timeEmo = 0
while timeEmo < fileDuration
	rndWait = randomUniform(0.5,1.5)
	rndProcess = randomInteger(1,3)
	if rndProcess = 1
		@doBlink: rndWait
		
	elsif rndProcess = 2
		@doEyes: rndWait

	elsif rndProcess = 3
		@doHead: rndWait
	endif
	timeEmo = timeEmo + rndWait * 2
endwhile


appendFileLine: pyName$, "threads = [Thread(target=doPlay), Thread(target=doLips), Thread(target=doNod), Thread(target=doEmo)]"
appendFileLine: pyName$, ""
appendFileLine: pyName$, "for t in threads:"
appendFileLine: pyName$, tab$, "t.start()"
appendFileLine: pyName$, ""
appendFileLine: pyName$, "for t in threads:"
appendFileLine: pyName$, tab$, "t.join()"
appendFileLine: pyName$, "ohbot.reset()"
appendFileLine: pyName$, "ohbot.wait(1)"
appendFileLine: pyName$, "ohbot.close()"

procedure doBlink: rndWait
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(3,1)"
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(3,9)"
endproc

procedure doEyes: rndWait
	rndMove = 5
	while rndMove = 5
		rndMove = randomInteger(1,9)
	endwhile
	rndSpeed = randomInteger(1,10)
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(2," + string$(rndMove) + "," + string$(rndSpeed) +")"
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(2,5," + string$(rndSpeed) +")"
endproc

procedure doHead: rndWait
	rndMove = 5
	while rndMove = 5
		rndMove = randomInteger(4,6)
	endwhile
	rndSpeed = randomInteger(1,3)
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(1," + string$(rndMove) + "," + string$(rndSpeed) +")"
	appendFileLine: pyName$, tab$, "ohbot.wait(" + string$(rndWait) + ")"
	appendFileLine: pyName$, tab$, "ohbot.move(1,5," + string$(rndSpeed) +")"
endproc
	