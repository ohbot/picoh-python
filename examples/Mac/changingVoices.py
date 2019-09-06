from picoh import picoh 

import random

# Run 'say -v?' in Terminal to list options for voices. speechSpeed is 90 +.

picoh.reset()

picoh.say("Hi it is great to be here, i am finally running on a mac, wow")

picoh.wait(2)

picoh.setVoice("Karen")

picoh.speechSpeed(150)

picoh.move(picoh.HEADTURN,random.randint(3,6))

picoh.say("hello i am Karen")

picoh.setVoice(name = "Alex")

picoh.speechSpeed(90)

picoh.move(picoh.HEADTURN,random.randint(2,6))

picoh.say("hello i am Alex slow")

picoh.setVoice("Oliver")

picoh.move(picoh.HEADTURN,random.randint(1,6))

picoh.speechSpeed(200)

picoh.say("hello i am Oliver fast")

picoh.setVoice("Kate")

picoh.speechSpeed(90)

picoh.say("Hey I am Kate slow")

picoh.speechSpeed(500)

picoh.say("Hey I am Kate fast")

picoh.wait(2)

picoh.close()
