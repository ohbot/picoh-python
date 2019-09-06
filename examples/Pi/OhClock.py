#OhClock - a sample program for using picoh python library.  More information at picoh.co.uk

from picoh import picoh
import threading
from time import time, sleep, localtime, strftime
from random import randint

#module level variable for breaking out of the blinking thread
blinking = False
#module level variable to stop it going off twice
lastm = ""

#this is called on a separate thread to blink the eyes while running
def blinkLids():
    while (blinking):
        picoh.move (picoh.LIDBLINK, 0)
        sleep (0.2)
        picoh.move (picoh.LIDBLINK, 10)
        #wait for a random amount of time for realistic blinking
        sleep (randint(0,4))

#start up sequence resets to mid position, sets the eyes to blue then goes to sleep
picoh.reset()
picoh.baseColour (0, 0, 10)
sleep(1.0)
picoh.baseColour (0, 0, 0)
picoh.move (picoh.HEADNOD, 0)
picoh.move (picoh.LIDBLINK, 0)
sleep(2.0)
#close to turn the motors off
picoh.close()

while (True):
    #get seconds and minutes into strings
    s = strftime("%S", localtime())
    m = strftime("%M", localtime())
    #set this to False for testing to make picoh speak continuously
    everyQuarterHour = True
    if ((everyQuarterHour == False) or ((everyQuarterHour == True) and (m == "00" or m == "15" or m == "30" or m == "45") and m != lastm)):
        lastm = m
        h = strftime("%H", localtime())
        hi = int (h)
        say = "Wow the time is "
        if (m == "15"):
            say = say + "a quarter past "
        if (m == "30"):
            say = say + "half past "
        if (m == "45"):
            say = say + "a quarter to "
            hi = hi + 1
            
        if hi == 0:
            say = say + "midnight"
        elif hi == 12:
            say = "mid day"
        elif (hi) > 12:
            say = say + str(hi-12) + " pea em"
        else:
            say = say + str(hi) + " a em"
            
        #for testing   
        if (m != "15" and m != "00" and m != "30" and m != "45"):
            say = say + " and " + m + " minutes"
            
        #set the eyes to pink, open eyes, lift head
        picoh.baseColour (10, 2, 2)
        picoh.move (picoh.LIDBLINK, 10)
        picoh.move (picoh.HEADNOD, 5)
        
        #now that eyes are open start blinking on a different thread
        blinking = True
        t = threading.Thread(target=blinkLids, args=())
        t.start()
        
        #turn the head to each side then back to centre
        sleep(0.5)
        picoh.move (picoh.HEADTURN, 10)
        sleep(0.5)
        picoh.move (picoh.HEADTURN, 0)
        sleep(0.5)
        picoh.move (picoh.HEADTURN, 5)

        #set hdmiAudio to True here if you are using hdmiAudio and speech is missing at beginning of each phrase
        picoh.say(say, untilDone=False, lipSync=True, hdmiAudio=False)

        #swivel eyes side to side 5 times
        for i in range (0, 5):
            picoh.move (picoh.EYETURN, 10, 10)
            sleep(0.1)
            picoh.move (picoh.EYETURN, 0, 10)
            sleep(0.1)
                
        #eye swivel back to centre
        picoh.move (picoh.EYETURN, 5, 10)

        #go to sleep position and turn eyes off
        sleep (3)
        blinking = False
        #wait a second for the thread to stop
        sleep (1)
        picoh.move (picoh.LIDBLINK, 0)
        picoh.baseColour (0, 0, 0)
        sleep(1)
        picoh.move (picoh.HEADNOD, 0)
        sleep(1)
        #turn motors off
        picoh.close()
        
        #sleep to stop it maxing out the CPU
        sleep(20)
