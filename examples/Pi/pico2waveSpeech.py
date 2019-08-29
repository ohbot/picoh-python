# Install pico2wave using sudo apt-get install libttspico-utils
# Ensure you are running the latest version of the library by running sudo pip3 install ohbot --upgrade

from ohbot import ohbot

ohbot.reset()

ohbot.setSynthesizer("pico2wave")

ohbot.say("now I can speak using pico2wave text to speech as well")

ohbot.wait(1)

ohbot.close()

