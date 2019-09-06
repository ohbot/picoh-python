# Picoh for Python (Windows Setup)


Background
-----

These instructions allow you to program your Picoh using Python on a Windows PC.

More information about Picoh can be found on [ohbot.co.uk.](http://www.ohbot.co.uk)


Setup
--------

Install the latest version of Python from [here.](https://www.python.org/downloads/)

Tick the option to Add Python 3.6 to PATH then click on Install Now. 

Once install is complete type “Command” into the Windows search box.  Right click on <b>Command Prompt </b> and select <b>Run as administrator.</b>

<br>

<a href="https://github.com/ohbot/ohbotWin-python/blob/master/images/image2-24.tif" target="_blank"><img src="https://github.com/ohbot/ohbotWin-python/blob/master/images/image2-24.tif" border="0" width = "35%"/></a>

<br>

This will open a command prompt window. 

Type the folloing:

``pip install picoh``

To upgrade to the latest version of the library run the following in the console:
```sudo pip3 install picoh --upgrade```

Installing more voices (optional)
--------

The Picoh Python library will default to using SAPI voices which are the voices that are available through Windows Control Panel:Speech Propeties.

You can change this to espeak or espeak-ng by calling picoh.setSynthesiser (“espeak”) or picoh.setSynthesizer (“espeak-ng”).

Install the espeak library from [here.](http://espeak.sourceforge.net/download.html)


Install espeak and then copy the espeak.exe file in Windows File Explorer from 

C:\Program Files (x86)\eSpeak\command_line

To 

C:\Program Files\Python36

To use the espeak-ng library install it from [here.](https://github.com/espeak-ng/espeak-ng#binaries)

Install espeak-ng and then copy the espeak-ng.exe and espeak-ng.dll files in Windows File Explorer from 

C:\Program Files\eSpeak NG

To 

C:\Program Files\Python36

That should be it for the setup.

Dependencies
----------

The ``pip install picoh`` command will install the following libraries:


| Library    | Use         | Terminal command to install  |Link |
| ---------- |-------------| -----------------------------|-----|
| picoh   | Interface with Picoh          | ```pip install picoh```  |[picoh](https://github.com/picoh/picoh-python/) 
| serial    | Communicate with serial port| ```pip install pyserial```  |[pyserial](https://github.com/pyserial/pyserial/) |
| lxml    | Import settings file          | ```pip install lxml```  |[lxml](https://github.com/lxml/lxml) |
| comtypes    | Required for serial communication      | ```pip install comtypes```  | [comtypes](https://github.com/enthought/comtypes) |
| pyobjc    | Python Objective C library       | ```pip3 install objc```  |[pyobjc](https://pypi.org/project/pyobjc/) |


To upgrade to the latest version of the library run the following in the console:
```pip install picoh -- upgrade```


Picoh library files (these will be installed with the `pip install picoh` command above):

| File    | Use         |
| ---------- |------------|
| picoh.py   | picoh package |
| picohDefinitions.omd    | Motor settings file |
| PicohSpeech.csv | Speech Database File |
| Ohbot.obe | EyeShape Files|


_Note: The text to speech module will generate an audio file, ‘picohspeech.wav’ inside /picohData in your working folder._

---

Hardware
-----

Required:


* PC Running Windows.
* Picoh
* USB Cable


Setup:

Connect Picoh to your PC using the USB cable. 

---

Starting Python Programs
--------

Go to the Windows Menu and run IDLE from the Python folder:


<a href="https://github.com/ohbot/ohbotWin-python/blob/master/images/image3-26.tif" target="_blank"><img src="https://github.com/ohbot/ohbotWin-python/blob/master/images/image3-26.tif" border="0" width = "35%"/></a>


Select <b>New</b> from the <b>File menu.</b>

Go to the [hellworldohbot](https://github.com/ohbot/ohbotWin-python/blob/master/examples/helloworldohbot.py) example on Github, copy the code and paste it into the new Python window.

Select <b>Run Module</b> from the <b>Run</b> menu.

Picoh should speak and move.

More example programs can be found [here.](https://github.com/ohbot/ohbotWin-python/tree/master/examples)
