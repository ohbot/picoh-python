# Picoh for Python

<a href="http://whoosh.co.uk/ohbothelp/images/eyes.gif" target="_blank"><img src="http://whoosh.co.uk/ohbothelp/images/eyes.gif" border="0" width = "30%"/></a>


Background
-----

These instructions allow you to program your Picoh using Python.

More information about Picoh can be found on [ohbot.co.uk.](http://www.ohbot.co.uk/picoh)


Setup
--------

Install the latest version of Python from [here.](https://www.python.org/downloads/release/python-364/)

Open the Terminal app and type the folloing:

**TODO**

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

---

Hardware
-----

Required:

***TODO**

* Mac running OSX
* Picoh
* USB Y Cable
* A 5 volt 1 amp USB power supply (for Picoh)
* Speakers/headphones.


Setup:


Plug the middle of USB Y cable into the computer and the other large USB plug into the power adaptor. Then plug the micro USB into Picoh. (Note with newer devices the power adaptor may not be required.)

---

Starting Python Programs
--------

Open <b>IDLE</b> from <b>Applications</b>.

Select <b>New</b> from the <b>File menu.</b>
**TODO**
Go to the [hellworldohbot](https://github.com/ohbot/ohbotMac-python/blob/master/examples/helloworldohbot.py) example on Github, copy the code and paste it into the new Python window.

Select <b>Run Module</b> from the <b>Run</b> menu.

Picoh should speak and move.

More example programs can be found [here.](https://github.com/ohbot/ohbotMac-python/tree/master/examples)


Functions
-------

picoh.init(portName)
----------

Called internally looking for a port with name containing "USB Serial Device" but if your port is different you can call it and override this port name. It returns True if the port is found and opened successfully, otherwise it returns false. This is likely with a versions of OSX in languages other than English. 

picoh.move(m, pos, speed=3)
----------


| Name| Range| Description | Default |
| --- |------|-------------|---------|
| m   | 0-6 (int)  | Motor Number| - |
| pos | 0-10 (int)  | Desired Position| - |
| speed | 0-10 (int) | Motor Speed| 3 |


For Example:
```python
picoh.move(1,7)
```
or
```python
picoh.move(2,3,1) 
```
or you can use a constant from the library to specify the motor:
```python
picoh.move(picoh.EYETURN,3,1) 
```
Motor index reference:

| m | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| ----| --- | --- |  --- |  --- |  --- |  --- |  --- |
| constant | HEADNOD | HEADTURN | EYETURN | LIDBLINK | TOPLIP | BOTTOMLIP | EYETILT | 
  

picoh.say(text, untilDone=True, lipSync=True, hdmiAudio=False, soundDelay=0)
----------

| Name| Range| Description | Default |
| --- |------|-------------|---------|
| text   | 'A string with no punctuation'  | Words to say| - |
| untilDone | bool  | Return when finished speaking| True |
| lipSync | bool | Move lips in time with speech| True |
| hdmiAudio | bool | Fixes missing start of phrase when HDMI audio output is being used| False |
| soundDelay | float | Set to positive if lip movement is lagging behind sound and negative if sound is lagging behind lip movement| 0 |



For Example:
```python
picoh.say('Hello I am Picoh')

picoh.say('Goodbye',False,False)

picoh.say('Goodbye',False,False,True)

picoh.say('Goodbye',soundDelay = 0.3)
```
---

picoh.wait(seconds)
----------

Seconds - float or int required wait time. picoh.wait(1.5)

| Name| Range| Description  |
| --- |------|-------------|
| seconds   | float or int  | Length of wait in seconds|



For Example:
```python
picoh.wait(2)

picoh.wait(0.5)
```

*Note: It is important to use picoh.wait() commands between motor sequential commands for the same motor.*

For Example:
```python
picoh.move(1,7,2)

picoh.wait(2)

picoh.move(1,4,2)
```
---

picoh.eyeColour(r, g, b, swapRandG=False)
----------

Set the colour of Picoh’s eyes. 

| Name| Range| Description  | Default |
| ---      |------|-------------| ------- |
| r        | 0-10 (int)  | Red| - |
| g        | 0-10 (int)  | Green| - |
| b        | 0-10 (int)  | Blue| - |
| swapRandG| bool | swap r and g value (Unused - legacy from Ohbot library) | False |


For Example:
```python
picoh.eyeColour(2,3,8)
```
or 
```python
picoh.eyeColour(2,3,8,True)
```

---

picoh.reset()
----------

Resets Picoh's motors  and matrix back to rest positions and turns off Picoh's base LEDs. Useful to start programs with this. You may need an picoh.wait() after this to give time for the motors to move. 

For Example:
```python
picoh.reset()
picoh.move(1,7,2)
picoh.wait(1)
picoh.move(1,1)
...
```
---

picoh.close()
----------

Call to detach all Picoh's motors which stops them using power, you can call picoh.attach(m) or picoh.detach(m) for individual motors.

For Example:
```python
picoh.move(1,7,2)
picoh.wait(1)
picoh.move(1,1)

picoh.close()
```
---

picoh.readSensor(sensorNumber)
----------

Seconds - float or int required wait time. picoh.wait(1.5)

| Name| Range| Description  |
| --- |------|-------------|
| sensorNumber   | 0-6 (int) | the pin the sensor is connected to |

returns the value as a float 0 - 10.

For Example:
```python
reading = picoh.readSensor(3)

picoh.move(picoh.HEADTURN, reading)

```
picoh.setSynthesizer(synth)
----------

Allows override of default OSX say command. 


** TODO **

picoh.setVoice(voice)
------

Use picoh.setVoice() to set the voice:

For Example:
```python

picoh.setVoice("Oliver")
picoh.say("Hello this is Oliver")
picoh.setVoice("Kate")
picoh.say("Hello this is Kate")
```
Available voices can be found in System Preferences -> Accessibility -> Speech in the System Voice Menu. Click customize to view voices in other languages. 

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" border="0" width = "50%"/></a>

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" border="0" width = "50%"/></a>

A full list of voices can also be displayed by entering the following command in Terminal:

```say -v ?```

picoh.speechSpeed(params)
------

Use picoh.speechSpeed() to set speech rate in words per minute:

Range: (int) 90+


For Example:
```python

picoh.setVoice("Oliver")
picoh.speechSpeed(90)
picoh.say("Hello this is Oliver Slow")
picoh.speechSpeed(400)
picoh.say("Hello this is Oliver Fast")
```




