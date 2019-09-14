# Speech Databse Tool.

Use the Speech Database Editor to edit the phrases in your speech database.  Each phrase can be assigned a Set and and Variable to help use them inside your Picoh programs. 

<a href="https://github.com/ohbot/picoh-python/blob/master/.images/speechdbscreenshot.png?raw=true" target="_blank"><img src="https://github.com/ohbot/picoh-python/blob/master/.images/speechdbscreenshot.png?raw=true" border="0" width = "100%"/></a>

* Tested on Python 3.7.  on macOS and Windows 10 and Python 3.4 on Raspberry Pi.
Right click and save file as:

How to run
----------
1) Right click and save in your working directory: [SpeechDatabase.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/tools/SpeechDatabase/SpeechDatabase.py)  

2) Run in IDLE or a Python editor/launcher of your choice. 


Using phrases from your database. 
----------
The speech database tool will read and write from PicohSpeech.csv found within the picohData/ in your working directory. 


To use a phrase in a Picoh program select it using its set and/or variable for example:


```python

picoh.getPhrase(1,2)

```
This command would make Picoh say "how can I help?" if you are using the default speech database as this is the only phrase where set = 1 and variable = 2.   

or

```python

picoh.say(picoh.getPhrase(set=1)))
# Picoh will say a random phrase from set 1.

picoh.say(picoh.getPhrase(variable=2))
# Picoh will say a random phrase with variable = 2.

picoh.say(picoh.getPhrase())
# Picoh will say a random phrase from the whole database. 

```
Please ensure you save your program inside the same folder as the speech database tool so they can both access the same copy of the picohData folder. See the picohData Folder section on the main [README](https://github.com/ohbot/picoh-python/blob/master/README.md) for more information.
