from picoh import picoh

## Example program for using sensors with picoh.
## Tilt sensor - a3
## Light sensor - a4
 
picoh.reset()
while True:    

    val1 = picoh.readSensor(4)
    
    val2 = picoh.readSensor(3)
    
    picoh.eyeColour(val2,10-val2,0,True)
    picoh.move(picoh.HEADTURN, val2)
    print(val2)
    if val1 > 2:
        picoh.say("put me down")
    
    if val2 < 2:
        picoh.say("who turned out the lights")

    picoh.wait(0.1)

