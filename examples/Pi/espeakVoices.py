#espeakVoices - a sample program for using picoh python library.  More information at ohbot.co.uk

# Setting voice with ESPEAK
# http://espeak.sourceforge.net/commands.html
# -v followed by a letter code - look in program files\espeak\espeak-data\voices to see what's available
# +m1 to +m7 for male voices
# +f1 to +f4 for female voices
# +croak or +whisper
# -a for amplitude (0 to 200)
# -s for speed 80 to 500
# -p for pitech 0 to 99

from picoh import picoh
import threading
from time import time, sleep, localtime, strftime
from random import randint

# Switch the speech synthesizer to epseak
picoh.setSynthesizer("espeak")

# Set the voice to english West Midlands accent medium speed.

picoh.setVoice("-ven-wm+m1 -s150")

#module level variable for breaking out of the blinking thread
blinking = False

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

# Start a thread for the blinking. 
blinking = True
t = threading.Thread(target=blinkLids, args=())
t.start()

sleep(2.0)

picoh.say("The picoh pi library now supports e speak meaning i can speak different languages and in different voices")

picoh.move(picoh.HEADTURN,4)
picoh.wait(0.2)
picoh.move(picoh.HEADTURN,6)
picoh.wait(0.2)

# Set the voice to English female medium speed.

picoh.setVoice("-ven+f2 -s150")
picoh.baseColour(3,10,2)
picoh.say("you can even change voice mid program")

# Set the voice to French female.

picoh.setVoice("-vfr+f2")
picoh.say("bonjour")

# Set the voice to Spanish female.

picoh.setVoice("-ves+f2")
picoh.say("hola")

# Set the voice to German male.

picoh.setVoice("-vde+m2")
picoh.say("Guten Tag")

picoh.move(picoh.HEADNOD,3)
picoh.move(picoh.HEADNOD,6)
picoh.baseColour(5,0,2)

# Set the voice to english whispering voice slower speed.

picoh.setVoice("-ven-wm+whisper -s120")
picoh.say("dont tell anyone but now i can whisper too")

picoh.wait(1)
picoh.close()
