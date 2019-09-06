# Test of different voices for Ohbot using Windows Python library
# SAPI (Default)
# -a0 to -a100 for amplitude
# -r-10 to r10 for rate
# -v any part of the name of a SAPI voice e.g. -vHazel, -vZira
# e.g. "-a82 -r12 -vzira"

# ESPEAK
# http://espeak.sourceforge.net/commands.html
# -v followed by a letter code - look in program files\espeak\espeak-data\voices to see what's available
# +m1 to +m7 for male voices
# +f1 to +f4 for female voices
# +croak or +whisper
# -a for amplitude (0 to 200)
# -s for speed 80 to 500
# -p for pitech 0 to 99

# ESPEAK-NG
# supports some of the ESPEAK but some is missing

# import the ohbot module
from ohbotWin import ohbot

# Reset Ohbot
ohbot.reset()

# Default synthesizer SAPI.  Default Voice as set in Control Panel
ohbot.say("I.  I just took a ride")
# Quieter
ohbot.setVoice("-a82")
ohbot.say("In a silver machine.")
# Faster
ohbot.setVoice("-r4")
ohbot.say("And I'm still feeling mean.")
# Slower
ohbot.setVoice("-r-4")
ohbot.say("Do you wanna ride? See yourself going by.")
# American
ohbot.setVoice("-vzira")
ohbot.say("The other side of the sky.")
# Default voice
ohbot.setVoice("")
ohbot.say("I got a silver machine.")

# Switch to espeak-ng - some of the voice attributes aren't supported
ohbot.setSynthesizer("espeak-ng")

# Female Portugese loud
ohbot.setVoice("-vpt+m1 -a200")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Male US
ohbot.setVoice("-ven-us+m2")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Female Spanish high pitch
ohbot.setVoice("-ves-la+f3 -p90")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Male Chinese speed fast
ohbot.setVoice("-vzh+m2 -s260")
ohbot.say("I got a silver machine.")
ohbot.wait(1)

# Switch to espeak
ohbot.setSynthesizer("espeak")

# Default voice
ohbot.setVoice("")
ohbot.say("I.  I just took a ride")
# Female French
ohbot.setVoice("-vfr+f4")
ohbot.say("In a silver machine.")
# Male English
ohbot.setVoice("-ven+m7")
ohbot.say("And I'm still feeling mean.")
# Female German
ohbot.setVoice("-vde+f1")
ohbot.say("Do you wanna ride? See yourself going by.")
# Croak English
ohbot.setVoice("-ven+croak")
ohbot.say("The other side of the sky.")
# Whisper English
ohbot.setVoice("-ven+whisper")
ohbot.say("I got a silver machine.")

ohbot.wait(2)

# Female Portugese loud
ohbot.setVoice("-vpt+m1 -a200")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Male US
ohbot.setVoice("-ven-us+m2")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Female Spanish high pitch
ohbot.setVoice("-ves-la+f3 -p90")
ohbot.say("I got a silver machine.")
ohbot.wait(1)
# Male Chinese speed fast
ohbot.setVoice("-vzh+m2 -s260")
ohbot.say("I got a silver machine.")
ohbot.wait(1)

ohbot.close()
