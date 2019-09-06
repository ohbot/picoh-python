# Picoh for Python (Mac Setup)


Background
-----

These instructions allow you to program your Picoh using Python on a Mac.

More information about Picoh can be found on [ohbot.co.uk.](http://www.ohbot.co.uk)


Setup
--------

Install the latest version of Python from [here.](https://www.python.org/downloads/)

Open the Terminal app and type the folloing:

``sudo pip3 install picoh``

You can find the Terminal app by searching for it in spotlight.

<a href="https://github.com/picoh/ohbotMac-python/blob/master/images/ss.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/ss.png" border="0" width = "60%"/></a>

Dependencies
----------

The ``pip3 install picoh`` command will install the following libraries:


| Library    | Use         | Terminal command to install  |Link |
| ---------- |-------------| -----------------------------|-----|
| picoh   | Interface with Picoh          | ```pip3 install picoh```  |[picoh](https://github.com/ohbot/picoh/) 
| serial    | Communicate with serial port| ```pip3 install pyserial```  |[pyserial](https://github.com/pyserial/pyserial/) |
| lxml    | Import settings file          | ```pip3 install lxml```  |[lxml](https://github.com/lxml/lxml) |
| playsound    | Play sound files       | ```pip3 install playsound```  |[playsound](https://github.com/TaylorSMarks/playsound) |
| pyobjc    | Python Objective C library       | ```pip3 install objc```  |[pyobjc](https://pypi.org/project/pyobjc/) |



To upgrade to the latest version of the library run the following in the console:
<br>
```sudo pip3 install picoh --upgrade```



Picoh library files (these will be installed with the `sudo pip3 install picoh` command above):

| File    | Use         |
| ---------- |------------|
| picoh.py   | Picoh package |
| picohdefinitions.omd    | Motor settings file |

_Note: The text to speech module will generate an audio file, ‘picohspeech.wav’ and a text file ‘phonemes.txt’ inside your working folder._


Hardware
-----

Required:


* Mac running OSX
* Picoh
* USB Cable

Setup:


Connect Picoh to your mac using the USB cable. 

---

Starting Python Programs
--------

Open <b>IDLE</b> from <b>Applications</b>.

Select <b>New</b> from the <b>File menu.</b>

Go to the [hellworldohbot](https://github.com/ohbot/ohbotMac-python/blob/master/examples/helloworldohbot.py) example on Github, copy the code and paste it into the new Python window.

Select <b>Run Module</b> from the <b>Run</b> menu.

Ohbot should speak and move.

More example programs can be found [here.](https://github.com/ohbot/ohbotMac-python/tree/master/examples)
