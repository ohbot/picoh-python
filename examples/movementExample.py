from picoh import picoh

# Reset Picoh
picoh.reset()

'''
The picoh.move() function needs at least 2 arguments: movement name and desired position.

picoh.HEADTURN
picoh.HEADNOD
picoh.EYETURN
picoh.EYETILT
picoh.BOTTOMLIP
picoh.LIDBLINK

position can be any number 0-10.

'''
# Move the HEADTURN motor to 2. 
picoh.move(picoh.HEADTURN,2)
picoh.say("head turn to 2")
# Move the HEADTURN motor to 5.
picoh.move(picoh.HEADTURN,5)
picoh.say("head turn to 5")

# Move the HEADNOD motor to 9. 
picoh.move(picoh.HEADNOD,9)
picoh.say("head nod to 9")
# Move the HEADNOD motor to 5. 
picoh.move(picoh.HEADNOD,5)
picoh.say("head nod to 5")

'''
The picoh.move() function can also take an optional third arguement 'spd'
to change the speed of the movement. If unspecified speed defaults to 5. 
'''

# Move HEADTURN motor to position 0 at speed 1.
picoh.move(picoh.HEADTURN,0,spd=1)
picoh.say("Head turn to 0, speed 1")

# Wait for motor to move
picoh.wait(2)

# Move HEADTURN motor to position 10 at speed 1.
picoh.move(picoh.HEADTURN,10,spd=1)
picoh.say("Head turn to 10, speed 1")

# Wait for motor to move
picoh.wait(1)

# Move HEADTURN motor to position 0 at speed 10.
picoh.move(picoh.HEADTURN,0,spd=10)
picoh.say("Head turn to 0, speed 10")

# Wait for motor to move
picoh.wait(0.5)

picoh.move(picoh.HEADTURN,10,spd=10)
picoh.say("Head turn to 10, speed 10")

# Wait for motor to move
picoh.reset()
picoh.wait(1)

'''
Finally the move function supports another optional argument 'eye'.
This will only have an effect when moving, EYETURN, EYETILT or LIDBLINK.
The eye arguments allows the eyes to be move individually, 0 - Both, 1 - Right, 2 - Left
If unspecified, default value 0 (Both) is used. 
'''

# Wink Left

for x in range(10,0,-1):
    picoh.move(picoh.LIDBLINK,x,eye = 1)
    picoh.wait(0.04)

for x in range(0,10):
    picoh.move(picoh.LIDBLINK,x,eye = 1)
    picoh.wait(0.04)

# Wink Right

for x in range(10,0,-1):
    picoh.move(picoh.LIDBLINK,x,eye = 2)
    picoh.wait(0.04)

for x in range(0,10):
    picoh.move(picoh.LIDBLINK,x,eye = 2)
    picoh.wait(0.04)

# Blink

for x in range(10,0,-1):
    picoh.move(picoh.LIDBLINK,x,eye = 0)
    picoh.wait(0.04)

for x in range(0,10):
    picoh.move(picoh.LIDBLINK,x,eye = 0)
    picoh.wait(0.04)

# Move right eye

for x in range(0,10):
    picoh.move(picoh.EYETILT,x,eye = 1)
    picoh.wait(0.1)

# Move left eye

for x in range(0,10):
    picoh.move(picoh.EYETILT,x,eye = 2)
    picoh.wait(0.1)

# Set both eyes back to 5. 
picoh.move(picoh.EYETILT,5)

picoh.close()







