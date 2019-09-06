##Example of picoh intergrated with wolfram alpha and wikipedia web service

import wolframalpha
from picoh import picoh
from random import *
import threading

import wikipedia

wiki = False

## please replace ???? with your own wolframalpha client id.

wolfclient = wolframalpha.Client('??????-??????????')

connectingPhrases = ['Let me think', 'Just a second', 'give me a moment', 'thats an easy one','thats tricky','i know this one','let me get you an answer']

picoh.reset()

def handleInput():
    while True:

        text = input("Question:\n")
        picoh.say(text)
        picoh.baseColour(10,5,0,True)
        randIndex = randrange(0,len(connectingPhrases))
        
        choice = connectingPhrases[randIndex]
        picoh.move(picoh.HEADTURN,5)
        picoh.move(picoh.EYETILT,7)
        picoh.move(picoh.HEADNOD,9)
        picoh.say(choice)

        
        try:
            res = wolfclient.query(text)
            ans = next(res.results).text
            ans = ans.replace("|",".")
            picoh.say(ans)
            picoh.baseColour(0,10,0,True)

        except:

            print('Answer not available')
            picoh.say("Answer not available")
            picoh.baseColour(10,0,0,True)                
                
        picoh.move(picoh.HEADTURN,5)

def handleInputWiki():
    while True:

        text = input("Define:\n")
        picoh.say(text)
        picoh.baseColour(10,5,0,True)
        randIndex = randrange(0,len(connectingPhrases))
        
        choice = connectingPhrases[randIndex]
        picoh.move(picoh.HEADTURN,5)
        picoh.move(picoh.EYETILT,7)
        picoh.move(picoh.HEADNOD,9)
        picoh.say(choice)
        

  
        
        try:
            res = wikipedia.summary(text)
            picoh.say(res)
            picoh.baseColour(0,10,0,True)

        except:

            print('Answer not available')
            picoh.say("Answer not available")
            picoh.baseColour(10,0,0,True)
            picoh.move(picoh.HEADTURN,5)
        

def moveLoop():

    while True:
        
        picoh.move(randint(0,2),randint(0,9))

        picoh.wait(randint(0,3))

def blinking():

    while True:

        picoh.move(picoh.LIDBLINK,0,10)

        picoh.wait(random()/3)

        picoh.move(picoh.LIDBLINK,10,10)

        picoh.wait(randint(0,6))


t = threading.Thread(target=moveLoop, args=())

if wiki:
    t2 = threading.Thread(target=handleInputWiki, args=())
else:
    t2 = threading.Thread(target=handleInput, args=())
    
t3 = threading.Thread(target=blinking, args=())


t.start()
t2.start()
t3.start()

picoh.say("Hello picoh here, please type in a question")
