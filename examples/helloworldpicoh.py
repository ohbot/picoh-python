from picoh import picoh

picoh.reset()

picoh.wait(1)

picoh.setEyeShape("Eyeball")

picoh.say("Hello my name is Picoh. Good to meet you")

picoh.move(picoh.HEADTURN,3)
picoh.move(picoh.EYETURN,3)

picoh.wait(1)

picoh.move(picoh.HEADTURN,6)
picoh.move(picoh.EYETURN,7)

picoh.baseColour(3,4,2)

picoh.wait(1)

# Change the base to orange
picoh.baseColour(10,3,0)

picoh.setEyeShape("SunGlasses")

# Slowly increase the brightness of Picoh's eyes.
for x in range(0,50):
    picoh.setEyeBrightness(x/10)
    picoh.wait(0.2)

# Get a random phrase from the speech database.
phrase = picoh.getPhrase()
picoh.say(phrase)

picoh.wait(3)
picoh.close()
