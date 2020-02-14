from picoh import picoh
# Reset picoh's motors and wait a second for them to move to rest positions.  
picoh.reset()
picoh.wait(1)

# Set Picoh's eye shape. 
picoh.setEyeShape("Eyeball")

# Say a phrase. 
picoh.say("Hello my name is Picoh. Good to meet you")

# Move the HEADTURN and EYETURN to position 3. 
picoh.move(picoh.HEADTURN,3)
picoh.move(picoh.EYETURN,3)

picoh.wait(1)

# Move the HEADTURN and EYETURN to position 7.
picoh.move(picoh.HEADTURN,7)
picoh.move(picoh.EYETURN,7)

# Set the base to red:3/10 green: 4/10 and blue 2/10. 
picoh.setBaseColour(3,4,2)

picoh.wait(1)

# Change the base to orange
picoh.setBaseColour(10,3,0)

# Set the eyeshape to SunGlasses
picoh.setEyeShape("SunGlasses")

# Slowly increase the brightness of Picoh's eyes.
for x in range(0,50):
    picoh.setEyeBrightness(x/10)
    picoh.wait(0.2)

# Get a random phrase from the speech database.
phrase = picoh.getPhrase()
picoh.say(phrase)

# Wait a few seconds and then close. This detaches Picoh's motors. 
picoh.wait(3)
picoh.close()
