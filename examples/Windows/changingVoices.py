# Test of different voices for picoh using Windows Python library
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

# import the picoh module
from picoh import picoh

# Reset picoh
picoh.reset()

# Default synthesizer SAPI.  Default Voice as set in Control Panel
picoh.say("I.  I just took a ride")
# Quieter
picoh.setVoice("-a82")
picoh.say("In a silver machine.")
# Faster
picoh.setVoice("-r4")
picoh.say("And I'm still feeling mean.")
# Slower
picoh.setVoice("-r-4")
picoh.say("Do you wanna ride? See yourself going by.")
# American
picoh.setVoice("-vzira")
picoh.say("The other side of the sky.")
# Default voice
picoh.setVoice("")
picoh.say("I got a silver machine.")

# Switch to espeak-ng - some of the voice attributes aren't supported
picoh.setSynthesizer("espeak-ng")

# Female Portugese loud
picoh.setVoice("-vpt+m1 -a200")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Male US
picoh.setVoice("-ven-us+m2")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Female Spanish high pitch
picoh.setVoice("-ves-la+f3 -p90")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Male Chinese speed fast
picoh.setVoice("-vzh+m2 -s260")
picoh.say("I got a silver machine.")
picoh.wait(1)

# Switch to espeak
picoh.setSynthesizer("espeak")

# Default voice
picoh.setVoice("")
picoh.say("I.  I just took a ride")
# Female French
picoh.setVoice("-vfr+f4")
picoh.say("In a silver machine.")
# Male English
picoh.setVoice("-ven+m7")
picoh.say("And I'm still feeling mean.")
# Female German
picoh.setVoice("-vde+f1")
picoh.say("Do you wanna ride? See yourself going by.")
# Croak English
picoh.setVoice("-ven+croak")
picoh.say("The other side of the sky.")
# Whisper English
picoh.setVoice("-ven+whisper")
picoh.say("I got a silver machine.")

picoh.wait(2)

# Female Portugese loud
picoh.setVoice("-vpt+m1 -a200")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Male US
picoh.setVoice("-ven-us+m2")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Female Spanish high pitch
picoh.setVoice("-ves-la+f3 -p90")
picoh.say("I got a silver machine.")
picoh.wait(1)
# Male Chinese speed fast
picoh.setVoice("-vzh+m2 -s260")
picoh.say("I got a silver machine.")
picoh.wait(1)

picoh.close()
