# Example of picoh intergrated with wolfram alpha and wikipedia web service

from picoh import picoh

# pip3 install wolframalpha
import wolframalpha

# pip3 install wikipedia
import wikipedia
from random import *
import threading


# Create global variables to enable movement and blinking to be turned on and off. 
global moving, blinking

# Set these global variables to False for the time being. 
moving = False
blinking = False

# Set wiki to False to use wolframalpha instead of wikipedia. 
wiki = True

# Please replace ???? with your own wolframalpha client id.
# Sign up free here to get a client id: https://products.wolframalpha.com/simple-api/documentation/

wolfclient = wolframalpha.Client('??????-??????????')

picoh.reset()

def handleInput():
    global moving
    while True:

        picoh.say("Hello picoh here, what shall I look up on wolfram alpha?")

        text = input("Question:\n")
        picoh.say(text)
        picoh.setBaseColour(10,5,0)

        # Stop the random movement. 
        moving = False
        
        # Look forward and up. 
        picoh.move(picoh.HEADTURN,5)
        picoh.move(picoh.EYETILT,7)
        picoh.move(picoh.HEADNOD,9)
        
        # get a random phrase from set 2 in the speech database. 
        picoh.say(picoh.getPhrase(set = 2))

        # Try the call to a webservice to get a response from WolframAlpha. 
        try:
            # Start random movement again
            moving = True
            res = wolfclient.query(text)
            ans = next(res.results).text
            
            # replace response text | with .
            ans = ans.replace("|",".")
            picoh.say(ans)
            
            # set base to green. 
            picoh.setBaseColour(0,10,0)
            
        # If no answer can be found then say answer not available and set base to red. 
        except:
            print('Answer not available')
            picoh.say("Answer not available")
            picoh.setBaseColour(10,0,0)
                
        picoh.move(picoh.HEADTURN,5)

def handleInputWiki():
    global moving
    while True:

        picoh.say("Hello picoh here, what would you like the wiki definition for?")

        # Put up a text box and wait for user to type the word they want to define. 
        text = input("Define:\n")
        
        # Say the word they have typed.
        picoh.say(text)
        picoh.setBaseColour(10,5,0)

        # Stop the random movement
        moving = False
        
        # Look forward and up. 
        picoh.move(picoh.HEADTURN,5)
        picoh.move(picoh.EYETILT,7)
        picoh.move(picoh.HEADNOD,9)
        
        # get a random phrase from set 2 in the speech database. 
        picoh.say(picoh.getPhrase(set = 2))
        
        # Try the call to a webservice to get a response from Wikipedia.
        # Request the first sentence of the definition.  
        try:
            # Start random movement again
            moving = True
            res = wikipedia.summary(text,sentences=1)
            picoh.say(res)
            picoh.setBaseColour(0,10,0)

        except:
            # If no answer can be found then say answer not available and set base to red. 
            print('Answer not available')
            picoh.say("Answer not available")
            picoh.setBaseColour(10,0,0)
            picoh.move(picoh.HEADTURN,5)
        
def blinkLids():
    global blinking
    
    # While True - Loop forever.
    while True:
        # if blinking is True.
        if blinking:
            # for the numbers 10 to 0 set the lidblink position. 
            for x in range(10, 0, -1):
                picoh.move(picoh.LIDBLINK,x)
                picoh.wait(0.01)
                
            # for the numbers 0 to 10 set the lidblink position.
            for x in range(0, 10):
                picoh.move(picoh.LIDBLINK,x)
                picoh.wait(0.01)

            # wait for a random amount of time for realistic blinking
            picoh.wait(random() * 6)

def randomLook():
    global moving 
    while True:
        # if moving is True. 
        if moving:
            # Look in a random direction.
            picoh.move(picoh.EYETILT, randint(2, 8))
            picoh.move(picoh.EYETURN, randint(2, 8))

            # Wait for between 0 and 5 seconds. 
            picoh.wait(random() * 5)

def randomTurn():
    global moving
    while True:
        if moving:
            # Move Picoh's HEADTURN motor to a random position between 3 and 7.
            picoh.move(picoh.HEADTURN, randint(3, 7))

            # wait for a random amount of time before moving again. 
            picoh.wait(random() * 4)

def randomNod():
    global moving
    while True:
        if moving:

            # Move Picoh's HEADNOD motor to a random position between 4 and 7.
            picoh.move(picoh.HEADNOD, randint(4, 7))

            # wait for a random amount of time before moving again. 
            picoh.wait(random() * 4)

# Create a thread for blinking.
t1 = threading.Thread(target=blinkLids, args=())

# Create a thread to make eyes look around randomly.
t2 = threading.Thread(target=randomLook, args=())

# Create a thread for random head nod positions.
t3 = threading.Thread(target=randomNod, args=())

# Create a thread for random head turn positions. 
t4 = threading.Thread(target=randomTurn, args=())

# If wiki = True then use t5 call hangleInputWiki otherwise call handleInput 
if wiki:
    t5 = threading.Thread(target=handleInputWiki, args=())
else:
    t5 = threading.Thread(target=handleInput, args=())

# Set moving and blinking global variables to True. 
moving = True
blinking = True

# Start the movement threads. 
t1.start()
t2.start()
t3.start()
t4.start()

# Start the handle input thread. 
t5.start()


