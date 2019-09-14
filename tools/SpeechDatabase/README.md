# Speech Databse Tool.

Use the Speech Database Editor to edit the phrases in your speech database.  Each phrase can be assigned a Set and and Variable to help use them inside your Picoh programs. 

<a href="https://github.com/ohbot/picoh-python/blob/master/.images/speechdbscreenshot.png?raw=true" target="_blank"><img src="https://github.com/ohbot/picoh-python/blob/master/.images/speechdbscreenshot.png?raw=true" border="0" width = "100%"/></a>

* Tested on Python 3.7.  on macOS and Windows 10 and Python 3.4 on Raspberry Pi.
Right click and save file as:

How to run
----------
1) Right click and save in your working directory: [SpeechDatabase.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/tools/SpeechDatabase/SpeechDatabase.py)  

2) Run in IDLE or a Python editor/launcher of your choice. 




Using Phrases from your database. 
----------
The speech database program will read and write from PicohSpeech.csv found within the picohData/ in your working directory. 


To use a phrase in a program for example:

|Set |Variable |Phrase|
|--|--|--|
|1 |2 |Hello |

```python

picoh.setEyeShape("TestEyeShape")

```
or

```python

picoh.setEyeShape("TestEyeShapeRight","TestEyeShapeLeft")

```
Please ensure you save your program inside the same folder as the eye shape designer so they can both access the same copy of the picohData folder. See the picohData Folder section on the main [README](https://github.com/ohbot/picoh-python/blob/master/README.md) for more information.


Auto Mirror
----------

Many eye shapes work well when the left eye is a mirror of the right eye, check the automirror box in the eye shape designer to toggle this setting for your eye shapes. For shapes where automirror is turned on, the image in the right eye will be mirrored automatically. 

<a href="https://github.com/ohbot/picoh-python/blob/master/.images/angryeye.png?raw=true" target="_blank"><img src="https://github.com/ohbot/picoh-python/blob/master/.images/angryeye.png?raw=true" border="0" width = "10%"/></a>
