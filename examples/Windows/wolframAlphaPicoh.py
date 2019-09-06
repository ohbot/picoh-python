##Example of ohbot intergrated with wolfram alpha and wikipedia web service

import wolframalpha
from ohbotWin import ohbot
from random import *
import threading

import wikipedia

wiki = False

## please replace ???? with your own wolframalpha client id.

wolfclient = wolframalpha.Client('??????-??????????')

connectingPhrases = ['Let me think', 'Just a second', 'give me a moment', 'thats an easy one','thats tricky','i know this one','let me get you an answer']

ohbot.reset()

def handleInput():
    while True:

        text = input("Question:\n")
        ohbot.say(text)
        ohbot.eyeColour(10,5,0,True)
        randIndex = randrange(0,len(connectingPhrases))
        
        choice = connectingPhrases[randIndex]
        ohbot.move(ohbot.HEADTURN,5)
        ohbot.move(ohbot.EYETILT,7)
        ohbot.move(ohbot.HEADNOD,9)
        ohbot.say(choice)

        
        try:
            res = wolfclient.query(text)
            ans = next(res.results).text
            ans = ans.replace("|",".")
            ohbot.say(ans)
            ohbot.eyeColour(0,10,0,True)

        except:

            print('Answer not available')
            ohbot.say("Answer not available")
            ohbot.eyeColour(10,0,0,True)                
                
        ohbot.move(ohbot.HEADTURN,5)

def handleInputWiki():
    while True:

        text = input("Define:\n")
        ohbot.say(text)
        ohbot.eyeColour(10,5,0,True)
        randIndex = randrange(0,len(connectingPhrases))
        
        choice = connectingPhrases[randIndex]
        ohbot.move(ohbot.HEADTURN,5)
        ohbot.move(ohbot.EYETILT,7)
        ohbot.move(ohbot.HEADNOD,9)
        ohbot.say(choice)
        

  
        
        try:
            res = wikipedia.summary(text)
            ohbot.say(res)
            ohbot.eyeColour(0,10,0,True)

        except:

            print('Answer not available')
            ohbot.say("Answer not available")
            ohbot.eyeColour(10,0,0,True)
            ohbot.move(ohbot.HEADTURN,5)
        

def moveLoop():

    while True:
        
        ohbot.move(randint(0,2),randint(0,9))

        ohbot.wait(randint(0,3))

def blinking():

    while True:

        ohbot.move(ohbot.LIDBLINK,0,10)

        ohbot.wait(random()/3)

        ohbot.move(ohbot.LIDBLINK,10,10)

        ohbot.wait(randint(0,6))


t = threading.Thread(target=moveLoop, args=())

if wiki:
    t2 = threading.Thread(target=handleInputWiki, args=())
else:
    t2 = threading.Thread(target=handleInput, args=())
    
t3 = threading.Thread(target=blinking, args=())


t.start()
t2.start()
t3.start()

ohbot.say("Hello ohbot here, please type in a question")
