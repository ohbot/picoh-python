# Install pico2wave using sudo apt-get install libttspico-utils
# Ensure you are running the latest version of the library by running sudo pip3 install picoh --upgrade

from picoh import picoh

picoh.reset()

picoh.setSynthesizer("pico2wave")

picoh.say("now I can speak using pico2wave text to speech as well")

picoh.wait(1)

picoh.close()

