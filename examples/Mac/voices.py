from ohbotMac import ohbot

import random

# Run 'say -v?' in Terminal to list options for voices. speechSpeed is 90 +.

ohbot.reset()

ohbot.say("Hi it is great to be here, i am finally running on a mac, wow")

ohbot.wait(2)

ohbot.setVoice("Karen")

ohbot.speechSpeed(150)

ohbot.move(ohbot.HEADTURN,random.randint(3,6))

ohbot.say("hello i am Karen")

ohbot.setVoice(name = "Alex")

ohbot.speechSpeed(90)

ohbot.move(ohbot.HEADTURN,random.randint(2,6))

ohbot.say("hello i am Alex slow")

ohbot.setVoice("Oliver")

ohbot.move(ohbot.HEADTURN,random.randint(1,6))

ohbot.speechSpeed(200)

ohbot.say("hello i am Oliver fast")

ohbot.setVoice("Kate")

ohbot.speechSpeed(90)

ohbot.say("Hey I am Kate slow")

ohbot.speechSpeed(500)

ohbot.say("Hey I am Kate fast")

ohbot.wait(2)

ohbot.close()
