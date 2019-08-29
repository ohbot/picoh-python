#espeakVoices - a sample program for using ohbot python library.  More information at ohbot.co.uk

# Setting voice with ESPEAK
# http://espeak.sourceforge.net/commands.html
# -v followed by a letter code - look in program files\espeak\espeak-data\voices to see what's available
# +m1 to +m7 for male voices
# +f1 to +f4 for female voices
# +croak or +whisper
# -a for amplitude (0 to 200)
# -s for speed 80 to 500
# -p for pitech 0 to 99

from ohbot import ohbot
import threading
from time import time, sleep, localtime, strftime
from random import randint

# Switch the speech synthesizer to epseak
ohbot.setSynthesizer("espeak")

# Set the voice to english West Midlands accent medium speed.

ohbot.setVoice("-ven-wm+m1 -s150")

#module level variable for breaking out of the blinking thread
blinking = False

#this is called on a separate thread to blink the eyes while running
def blinkLids():
    while (blinking):
        ohbot.move (ohbot.LIDBLINK, 0)
        sleep (0.2)
        ohbot.move (ohbot.LIDBLINK, 10)
        #wait for a random amount of time for realistic blinking
        sleep (randint(0,4))

#start up sequence resets to mid position, sets the eyes to blue then goes to sleep
ohbot.reset()
ohbot.eyeColour (0, 0, 10)
sleep(1.0)
ohbot.eyeColour (0, 0, 0)

# Start a thread for the blinking. 
blinking = True
t = threading.Thread(target=blinkLids, args=())
t.start()

sleep(2.0)

ohbot.say("The ohbot pi library now supports e speak meaning i can speak different languages and in different voices")

ohbot.move(ohbot.HEADTURN,4)
ohbot.wait(0.2)
ohbot.move(ohbot.HEADTURN,6)
ohbot.wait(0.2)

# Set the voice to English female medium speed.

ohbot.setVoice("-ven+f2 -s150")
ohbot.eyeColour(3,10,2)
ohbot.say("you can even change voice mid program")

# Set the voice to French female.

ohbot.setVoice("-vfr+f2")
ohbot.say("bonjour")

# Set the voice to Spanish female.

ohbot.setVoice("-ves+f2")
ohbot.say("hola")

# Set the voice to German male.

ohbot.setVoice("-vde+m2")
ohbot.say("Guten Tag")

ohbot.move(ohbot.HEADNOD,3)
ohbot.move(ohbot.HEADNOD,6)
ohbot.eyeColour(5,0,2)

# Set the voice to english whispering voice slower speed.

ohbot.setVoice("-ven-wm+whisper -s120")
ohbot.say("dont tell anyone but now i can whisper too")

ohbot.wait(1)
ohbot.close()
