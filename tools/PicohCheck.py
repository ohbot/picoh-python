from picohLocal import picoh
import random

picoh.reset()

picoh.wait(0.2)

picoh.say("Commencing hardware tests")

picoh.say("Base to red")
picoh.setBaseColour(10,0,0)

picoh.say("Base to green")
picoh.setBaseColour(0,10,0)

picoh.say("Base to blue")
picoh.setBaseColour(0,0,10)

picoh.say("Matrix off")
picoh.move(picoh.LIDBLINK,0)
picoh.setEyeShape("Full")

picoh.say("Matrix on")
picoh.move(picoh.LIDBLINK,10)

picoh.say("Eyes to angry")
picoh.setEyeShape("Angry")

picoh.say("Reset Eyes")
picoh.setEyeShape("Eyeball")

picoh.say("HeadTurn motor 0 to 10")

for x in range(0,10):

    picoh.move(picoh.HEADTURN,x)
    picoh.wait(0.2)
    
picoh.move(picoh.HEADTURN,5)

picoh.say("HeadNod motor 0 to 10")

for x in range(0,10):

    picoh.move(picoh.HEADNOD,x)
    picoh.wait(0.2)

picoh.move(picoh.HEADNOD,5)

picoh.say("Commencing random movement")

count = 0

while count < 10:
    picoh.move(picoh.HEADTURN,random.randint(2, 8))
    picoh.move(picoh.HEADNOD,random.randint(2, 8))
    picoh.move(picoh.EYETILT,random.randint(2, 8))
    picoh.move(picoh.EYETURN,random.randint(2, 8))
    count = count + 1
    picoh.wait(random.random()*2)

picoh.reset()

picoh.say("playing sound")

picoh.playSound('spring')

picoh.say("Random phrase from speech database")

picoh.say(picoh.getPhrase())

picoh.reset()
picoh.say("Goodbye")
picoh.close()

