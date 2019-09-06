# import the picoh module

from picoh import picoh

# Reset picoh

picoh.reset()

# Move turn picoh's head and eyes.
picoh.move(1,2)
picoh.move(3,1)

# Wait a few seconds for the motors to move

picoh.wait(2)

# Move head back to the centre and say "Hello World"
picoh.move(1,5,1)
picoh.say("Hello World")

# Slowly increase the brightness of the eyes.

for x in range(0,10):

    picoh.eyeColour(x,x,x)
    picoh.wait(0.1)

    picoh.eyeColour(0,0,0)
    picoh.wait(0.2)

    

picoh.move(1,5,1)
picoh.wait(1)

picoh.say("Now I am running in python you know",False)

for x in range (0,10):
    picoh.move(3,x)
    picoh.eyeColour(x,10-x,x)
    picoh.wait(0.3)

picoh.say("I can do the robot")


for y in range(0,4):
    for x in range(0,10):
        picoh.move(y,x)
        picoh.eyeColour(y,x,10-x)
        picoh.wait(0.2)
        
picoh.reset()
picoh.say("and ventriloquism",True,False)
picoh.eyeColour(0,0,10)
picoh.wait(1)

# close picoh at the end.

picoh.close()
