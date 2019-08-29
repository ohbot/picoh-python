# import the ohbot module

from ohbot import ohbot

# Reset Ohbot

ohbot.reset()

# Move turn ohbot's head and eyes. 
ohbot.move(1,2)
ohbot.move(3,1)

# Wait a few seconds for the motors to move

ohbot.wait(2)

# Move head back to the centre and say "Hello World"
ohbot.move(1,5,1)
ohbot.say("Hello World")

# Slowly increase the brightness of the eyes.

for x in range(0,10):

    ohbot.eyeColour(x,x,x)
    ohbot.wait(0.1)

    ohbot.eyeColour(0,0,0)
    ohbot.wait(0.2)

    

ohbot.move(1,5,1)
ohbot.wait(1)

ohbot.say("Now I am running in python you know",False)

for x in range (0,10):
    ohbot.move(3,x)
    ohbot.eyeColour(x,10-x,x)
    ohbot.wait(0.3)

ohbot.say("I can do the robot")


for y in range(0,4):
    for x in range(0,10):
        ohbot.move(y,x)
        ohbot.eyeColour(y,x,10-x)
        ohbot.wait(0.2)
        
ohbot.reset()      
ohbot.say("and ventriloquism",True,False)
ohbot.eyeColour(0,0,10)
ohbot.wait(1)

# close ohbot at the end.

ohbot.close()
