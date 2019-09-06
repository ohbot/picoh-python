# Picoh for Python

<a href=".images/PicohLogoPixels.png" target="_blank"><img src=".images/PicohLogoPixels.png" border="0" width = "30%"/></a>

Setup
-------

 [macOS](https://github.com/ohbot/picoh)

Functions
-------

picoh.init(portName)
----------

Called internally looking for a port with name containing "USB Serial Device" but if your port is different you can call it and override this port name. It returns True if the port is found and opened successfully, otherwise it returns false. This is likely with Operating Systems in languages other than English.

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

picoh.setEyeShape(shapeNameLeft,shapeNameRight)
------

shapeNameLeft: String - Eyeshape name. 
shapeNameRight: String - Eyeshape name. 

Use picoh.setEyeShape() to change the shape of pixels displayed on Picoh's matrix display. 
To see available eye shapes and design your own have a look at the EyeShape designer tool.

For Example:
```python

picoh.setEyeShape("Happy")

```
or set pupils to different shapes using:
```python

picoh.setEyeShape("Sad","Angry")
picoh.wait(1)
picoh.setEyeShape("Large","Heart")
```

Default options for eye shapes: "Angry", "Crying", "Eyeball", "Glasses", "Heart", "Large", "Sad", "SmallBall", "Square","Sungalsses", "VerySad"


picoh.setEyeBrightness(val)
------

| Name| Range| Description |
| --- |------|-------------|
| val | 0-10 (int or float)  | Desired Brightness| 

Use picoh.setEyeShape() to change the brightness of the pixels on Picoh's matrix display. 

For Example:
```python

picoh.setEyeBrightness(3)
picoh.wait(1)

```
or loop set in a loop:
```python

for x in range(0,10):
    picoh.setEyeBrightness(x)
    picoh.wait(0.2)
```


picoh.getPhrase(set,variable)
------

set: Int - The desired set for phrase. 
variable: Int - The desired variable for phrase. 

Use picoh.getPhrase() to retrieve a phrase from Picoh's speech database. 

You can view and edit the speech database using the Speech Databse tool. Each entry in the speech database has a set and a variable associated with it. When you use getPhrase() you can choose to get phrases with specific values for set and/or variable.  

If more than one phrase matches the set and variable provided a random match is returned. 

To see available eye shapes and design your own have a look at the EyeShape designer tool.

For Example:
```python

picoh.say(picoh.getPhrase(1,2))

```
or get a random phrase from a specific set:
```python

picoh.say(picoh.getPhrase(set=1)))
# Picoh will say a random phrase from set 1.

picoh.say(picoh.getPhrase(variable=2))
# Picoh will say a random phrase with variable = 2.
```

or get a random phrase from the whole database:
```python

picoh.say(picoh.getPhrase())

```


picoh.baseColour(r, g, b)
----------

Set the colour of Picoh’s eyes. 

| Name| Range| Description  | Default |
| ---      |------|-------------| ------- |
| r        | 0-10 (int)  | Red| - |
| g        | 0-10 (int)  | Green| - |
| b        | 0-10 (int)  | Blue| - |


For Example:
```python
picoh.baseColour(2,3,8)
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




