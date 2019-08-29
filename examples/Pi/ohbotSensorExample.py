from ohbot import ohbot

## Example program for using sensors with ohbot.
## Tilt sensor - a3
## Light sensor - a4
 
ohbot.reset()
while True:    

    val1 = ohbot.readSensor(4)
    
    val2 = ohbot.readSensor(3)
    
    ohbot.eyeColour(val2,10-val2,0,True)
    ohbot.move(ohbot.HEADTURN, val2)
    print(val2)
    if val1 > 2:
        ohbot.say("put me down")
    
    if val2 < 2:
        ohbot.say("who turned out the lights")

    ohbot.wait(0.1)

