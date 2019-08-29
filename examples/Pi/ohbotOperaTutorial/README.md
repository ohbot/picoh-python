
# Ohbot Opera

This project shows one out of many potential ways to make the Ohbot Pi lip sync to any song. Examples can be found here:

https://www.youtube.com/watch?v=cJJtYiWifbY<br/>
https://www.youtube.com/watch?v=LoCSa6Hx0VE

## Author

Emmanuel Ferragne  
http://w3.univ-paris-diderot.fr/EtudesAnglophones/pg.php?bc=CHVEENG&page=FICHECHERC&g=sm&uid=eferragn

## Prerequisites
This presupposes that you already know how to run simple Python scripts for the Ohbot. 

* Hardware
	* Ohbot Pi
	* Raspberry Pi (mine is a 3 B)
	* PC (should work with any mainstream OS)
	* Amplified speakers or headphones
* Software
	* Praat (free software for speech analysis - intalled in a few seconds) on your PC
	* a Python IDE on the Raspberry Pi (like Thonny, which is bundled with Raspbian)
	* Ohbot software libraries for Python

## General workflow
The vowels you identified in your manual segmentation of the soundtrack with Praat (this is the tedious bit) will be automatically converted to lip positions and corresponding durations. The script textgrid2Ohbot.praat writes the final Python script for you and adds random head and eye movements and blinks. More info can be found in the comments inside textgrid2Ohbot.praat. The Python script is run on the Raspberry Pi; it controls the Ohbot's movements and plays back the sound track. 

## Step by step procedure
* Install the required programs; if you already have a Raspberry Pi with e.g. NOOBS, you just need to install Praat on your PC
* Put the files phonemeMapping.txt, textgrid2Ohbot.praat, and your soundtrack (preferrably a very short one to start with) in the same folder on your PC
* Open the soundtrack with Praat and create a TextGrid object with one interval tier
* Perform phonetic segmentation and annotation: here's a useful tutorial: https://www.youtube.com/watch?v=TuuJfr0tdzw
* Double-check that all the vowel symbols you put in your TextGrid also appear in the first column of phonemeMapping.txt, with corresponding lip position values in the other two columns. You can of course edit this file to add your own symbols and lip positions
* Save your TextGrid Object with Save as text file..., make sure it has the same name as the corresponding sound file, i.e., if your sound file is called demoOpera.wav, your TextGrid file should be demoOpera.TextGrid
* Open the script textgrid2Ohbot.praat in Praat. Run it. You will be prompted to choose the relevant TextGrid file, and then a new file will be created, with the same name as your TextGrid followed by a ".py" extension. 
* Export the sound file and the .py file to the same folder on the Raspberry Pi. 
* Make sure the Ohbot is connect and ready, connect speakers to the Pi's output jack, open the .py file in your Python IDE, and run it. 



