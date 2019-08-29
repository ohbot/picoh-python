# Ohbot for Python (Mac Version)

<a href="http://whoosh.co.uk/ohbothelp/images/eyes.gif" target="_blank"><img src="http://whoosh.co.uk/ohbothelp/images/eyes.gif" border="0" width = "30%"/></a>


Background
-----

These instructions allow you to program your Ohbot using Python on a Mac.

More information about Ohbot can be found on [ohbot.co.uk.](http://www.ohbot.co.uk)


Setup
--------

Install the latest version of Python from [here.](https://www.python.org/downloads/release/python-364/)

Open the Terminal app and type the folloing:

``sudo pip3 install ohbotMac``

You can find the Terminal app by searching for it in spotlight.

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/ss.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/ss.png" border="0" width = "60%"/></a>

Dependencies
----------

The ``pip3 install ohbotMac`` command will install the following libraries:


| Library    | Use         | Terminal command to install  |Link |
| ---------- |-------------| -----------------------------|-----|
| ohbotMac   | Interface with Ohbot          | ```pip3 install ohbotMac```  |[ohbot](https://github.com/ohbot/ohbotWin-python/) 
| serial    | Communicate with serial port| ```pip3 install pyserial```  |[pyserial](https://github.com/pyserial/pyserial/) |
| lxml    | Import settings file          | ```pip3 install lxml```  |[lxml](https://github.com/lxml/lxml) |
| playsound    | Play sound files       | ```pip3 install playsound```  |[playsound](https://github.com/TaylorSMarks/playsound) |
| pyobjc    | Python Objective C library       | ```pip3 install objc```  |[pyobjc](https://pypi.org/project/pyobjc/) |



To upgrade to the latest version of the library run the following in the console:
<br>
```sudo pip3 install ohbotMac --upgrade```



Ohbot library files (these will be installed with the `sudo pip3 install ohbotMac` command above):

| File    | Use         |
| ---------- |------------|
| ohbot.py   | Ohbot package |
| MotorDefinionsv21.omd    | Motor settings file |

_Note: The text to speech module will generate an audio file, ‘ohbotspeech.wav’ and a text file ‘phonemes.txt’ inside your working folder._

---

Hardware
-----

Required:


* Mac running OSX
* Ohbot
* USB Y Cable
* A 5 volt 1 amp USB power supply (for Ohbot)
* Speakers/headphones.


Setup:


Plug the middle of USB Y cable into the PC and the other large USB plug into the power adaptor. Then plug the mini USB into Ohbot. (Note with newer devices the power adaptor may not be required.)

---

Starting Python Programs
--------

Open <b>IDLE</b> from <b>Applications</b>.

Select <b>New</b> from the <b>File menu.</b>

Go to the [hellworldohbot](https://github.com/ohbot/ohbotMac-python/blob/master/examples/helloworldohbot.py) example on Github, copy the code and paste it into the new Python window.

Select <b>Run Module</b> from the <b>Run</b> menu.

Ohbot should speak and move.

More example programs can be found [here.](https://github.com/ohbot/ohbotMac-python/tree/master/examples)


Functions
-------

ohbot.init(portName)
----------

Called internally looking for a port with name containing "USB Serial Device" but if your port is different you can call it and override this port name. It returns True if the port is found and opened successfully, otherwise it returns false. This is likely with a versions of OSX in languages other than English. 

ohbot.move(m, pos, speed=3)
----------


| Name| Range| Description | Default |
| --- |------|-------------|---------|
| m   | 0-6 (int)  | Motor Number| - |
| pos | 0-10 (int)  | Desired Position| - |
| speed | 0-10 (int) | Motor Speed| 3 |


For Example:
```python
ohbot.move(1,7)
```
or
```python
ohbot.move(2,3,1) 
```
or you can use a constant from the library to specify the motor:
```python
ohbot.move(ohbot.EYETURN,3,1) 
```
Motor index reference:

| m | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| ----| --- | --- |  --- |  --- |  --- |  --- |  --- |
| constant | HEADNOD | HEADTURN | EYETURN | LIDBLINK | TOPLIP | BOTTOMLIP | EYETILT | 
  

ohbot.say(text, untilDone=True, lipSync=True, hdmiAudio=False, soundDelay=0)
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
ohbot.say('Hello I am Ohbot')

ohbot.say('Goodbye',False,False)

ohbot.say('Goodbye',False,False,True)

ohbot.say('Goodbye',soundDelay = 0.3)
```
---

ohbot.wait(seconds)
----------

Seconds - float or int required wait time. ohbot.wait(1.5)

| Name| Range| Description  |
| --- |------|-------------|
| seconds   | float or int  | Length of wait in seconds|



For Example:
```python
ohbot.wait(2)

ohbot.wait(0.5)
```

*Note: It is important to use ohbot.wait() commands between motor sequential commands for the same motor.*

For Example:
```python
ohbot.move(1,7,2)

ohbot.wait(2)

ohbot.move(1,4,2)
```
---

ohbot.eyeColour(r, g, b, swapRandG=False)
----------

Set the colour of Ohbot’s eyes. 

| Name| Range| Description  | Default |
| ---      |------|-------------| ------- |
| r        | 0-10 (int)  | Red| - |
| g        | 0-10 (int)  | Green| - |
| b        | 0-10 (int)  | Blue| - |
| swapRandG| bool | swap r and g value for some older Ohbots | False |


For Example:
```python
ohbot.eyeColour(2,3,8)
```
or 
```python
ohbot.eyeColour(2,3,8,True)
```

---

ohbot.reset()
----------

Resets Ohbot’s motors back to rest positions and turns off Ohbot’s eyes. Useful to start programs with this. You may need an ohbot.wait() after this to give time for the motors to move. 

For Example:
```python
ohbot.reset()
ohbot.move(1,7,2)
ohbot.wait(1)
ohbot.move(1,1)
...
```
---

ohbot.close()
----------

Call to detach all Ohbot’s motors which stops them using power, you can call ohbot.attach(m) or ohbot.detach(m) for individual motors.

For Example:
```python
ohbot.move(1,7,2)
ohbot.wait(1)
ohbot.move(1,1)

ohbot.close()
```
---

ohbot.readSensor(sensorNumber)
----------

Seconds - float or int required wait time. ohbot.wait(1.5)

| Name| Range| Description  |
| --- |------|-------------|
| sensorNumber   | 0-6 (int) | the pin the sensor is connected to |

returns the value as a float 0 - 10.

For Example:
```python
reading = ohbot.readSensor(3)

ohbot.move(ohbot.HEADTURN, reading)

```
ohbot.setSynthesizer(synth)
----------

Allows override of default OSX say command. 


ohbot.setVoice(voice)
------

Use ohbot.setVoice() to set the voice:

For Example:
```python

ohbot.setVoice("Oliver")
ohbot.say("Hello this is Oliver")
ohbot.setVoice("Kate")
ohbot.say("Hello this is Kate")
```
Available voices can be found in System Preferences -> Accessibility -> Speech in the System Voice Menu. Click customize to view voices in other languages. 

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" border="0" width = "50%"/></a>

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" border="0" width = "50%"/></a>

A full list of voices can also be displayed by entering the following command in Terminal:

```say -v ?```

ohbot.speechSpeed(params)
------

Use ohbot.speechSpeed() to set speech rate in words per minute:

Range: (int) 90+


For Example:
```python

ohbot.setVoice("Oliver")
ohbot.speechSpeed(90)
ohbot.say("Hello this is Oliver Slow")
ohbot.speechSpeed(400)
ohbot.say("Hello this is Oliver Fast")
```




