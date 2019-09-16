# Example of how to use the play sound function and change the base colour of Picoh.

from picoh import picoh
import random

picoh.reset()
picoh.wait(1)
picoh.move(picoh.LIDBLINK,0)

picoh.setEyeShape('Heart')
picoh.setEyeBrightness(0)
picoh.playSound('fanfare',untilDone = False)
picoh.wait(1.5)

picoh.move(picoh.LIDBLINK,5)
picoh.setEyeBrightness(5)

picoh.wait(1)

picoh.move(picoh.LIDBLINK,10)
picoh.setEyeBrightness(10)
picoh.wait(2)
picoh.setEyeBrightness(7)
picoh.wait(4)

picoh.playSound('ohbot',untilDone = False)

picoh.setEyeShape('Glasses')
for x in range(0,40):
    picoh.baseColour(random.randrange(0,10),random.randrange(0,10),random.randrange(0,10))
    picoh.wait(0.05)
    
picoh.baseColour(0,0,0)
picoh.wait(0.5)

picoh.setEyeShape('Angry')
picoh.playSound('smash',untilDone = False)
picoh.baseColour(10,0,0)

for x in range(0,14):
    picoh.move(picoh.EYETILT,3)
    picoh.wait(x/100)
    picoh.move(picoh.EYETILT,6)
    picoh.wait(x/100)
    
# Spring, play on a sepereate thread using untilDone = False.  
picoh.playSound('spring',untilDone = False)

picoh.setEyeShape('BoxRight','BoxLeft')
for x in range(0,14):
    picoh.move(picoh.EYETURN,3)
    picoh.wait(x/100)
    picoh.move(picoh.EYETURN,7)
    picoh.wait(x/100)
    picoh.baseColour(x,10-x,0)

picoh.move(picoh.EYETURN,5)

picoh.playSound('loop', untilDone = False)
picoh.setEyeShape('SunGlasses')

# The length of a beat in seconds
lengthOfBeat = 0.565

for x in range(0,8):

    picoh.move(picoh.HEADNOD,6)
    picoh.baseColour(x,10-x,0)

    picoh.wait(lengthOfBeat/2)
    
    picoh.move(picoh.HEADTURN,7)
    picoh.move(picoh.HEADNOD,4)
    picoh.baseColour(0,x,10-x)

    picoh.wait(lengthOfBeat/2)
    picoh.baseColour(10-x,x,0)

    picoh.move(picoh.HEADNOD,6)

    picoh.wait(lengthOfBeat/2)

    picoh.move(picoh.HEADTURN,3)
    picoh.move(picoh.HEADNOD,4)
    picoh.baseColour(0,10-x,x)

    picoh.wait(lengthOfBeat/2)
    
picoh.reset()
picoh.wait(1)
picoh.close()
