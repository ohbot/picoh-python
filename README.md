# Picoh for Python

<a href=".images/PicohLogoPixels.png" target="_blank"><img src=".images/PicohLogoPixels.png" border="0" width = "30%"/></a>

Choose your platform and click the links to get started!

|||||
|-------|-------|---------|-------|
|macOS|[Getting Started](https://github.com/ohbot/picoh-python/blob/master/Docs/Setup_Mac.md)|[Examples](https://github.com/ohbot/picoh-python/tree/master/examples/Mac)|[Text to speech documentation](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Mac.md)|
|Windows|[Getting Started](https://github.com/ohbot/picoh-python/blob/master/Docs/Setup_Windows.md)|[Examples](https://github.com/ohbot/picoh-python/tree/master/examples/Windows)|[Text to speech documentation](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Windows.md)|
|Pi|[Getting Started](https://github.com/ohbot/picoh-python/blob/master/Docs/Setup_Pi.md)|[Examples](https://github.com/ohbot/picoh-python/tree/master/examples/Pi)|[Text to speech documentation](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Pi.md)|


If you are new to Python here is a short guide explaining some of the key concepts: [Programming Picoh in Python](https://docs.google.com/document/d/e/2PACX-1vTM9FmTBpGGJ4Ddvutpv3kxXkS0oyT4U9JPBV95UXdSJU10TD5JC1XWTf2cRGjHWApHOrTC6JLizD64/pub)

To be expanded soon!

picohData Folder
-------
The fist time you run a Picoh program a new folder called picohData is created in your working directory. This folder is used to store various files that you can read from within your Picoh programs, these include SpeechDatabase file, a Motor Definitions file and an EyeShapes file. 


There are a various tools you can use to help edit these data files. When using a tool please download it and save it in the same folder as the your Picoh program file, this will ensure it is reading and writing to the correct folder. 


The data files include: 

Ohbot.obe - Containing eye shape patterns for Picoh's matrix display edited with the [Eyeshape Designer Tool](https://github.com/ohbot/picoh-python/tree/master/tools/EyeShapeDesigner). Eye shapes are accessed in Picoh programs using picoh.setEyeShape(), see below for examples. 

picohspeech.csv - Holds phrases for Picoh to say. Edit using the  [Speech Database Tool.](https://github.com/ohbot/picoh-python/tree/master/tools/SpeechDatabase) Phrases are accessed using picoh.getPhrase(), see below for more information. 

MotorDefinitionsPicoh.omd - Holds motor minimums, maximums and ranges. Modified using the [Calibrate Tool.](https://github.com/ohbot/picoh-python/tree/master/tools/Calibrate) Just calibrates the lip for now but will soon be able to calibrate all motors. 


If you delete a file in picohData (or the whole folder) the default files will be copied back over from the picoh library folder.  


You can share the picohData between multiple programs by saving them in the same folder. 

For example:
```
picohProgramsFolder
│   picohTest1.py
|   picohTest2.py
│   EyeShapeDesigner.py 
|   SpeechDatabse.py 
│   Calibrate.py   
|
└───picohData (Created Automatically)
        Ohbot.obe
        MotorDefinitionsPicoh.omd
        picohspeech.csv
```
Alternatively you can have seperate picohData folders by saving your programs in different folders, you will need a copy of the tools you want to use in the folder as well:
```
picohProgramsFolder
└───folderOne
│   │   picohTest1.py
│   │   Calibrate.py 
│   │   EyeShapeDesigner.py
|   |   SpeechDatabase.py
|   |   
│   └───picohData (Created Automatically)
│           Ohbot.obe
│           MotorDefinitionsPicoh.omd
│           picohspeech.csv
│   
└───folderTwo
    │   picohTest2.py
    │   Calibrate.py 
    │   EyeShapeDesigner.py
    |   SpeechDatabase.py
    |   
    └───picohData (Created Automatically)
            Ohbot.obe
            MotorDefinitionsPicoh.omd
            picohspeech.csv


```


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

picoh.setEyeShape(shapeNameRight,shapeNameLeft)
------

shapeNameRight: String - Eyeshape name. 
shapeNameLeft: String - Eyeshape name. 

Use picoh.setEyeShape() to change the shape of pixels displayed on Picoh's matrix display. 
To see available eye shapes and design your own have a look at the [EyeShape designer tool](https://github.com/ohbot/picoh-python/tree/master/tools/EyeShapeDesigner).

For Example:
```python

picoh.setEyeShape("Glasses")

```
or set pupils to different shapes using:
```python

picoh.setEyeShape("Sad","Angry")
picoh.wait(1)
picoh.setEyeShape("Large","Heart")
```

Default options for eye shapes: 

"Angry","BoxLeft","BoxRight", "Crying", "Eyeball", "Glasses", "Heart", "Large", "Sad", "SmallBall", "Square","SunGlasses", "VerySad"


picoh.setEyeBrightness(val)
------

| Name| Range| Description |
| --- |------|-------------|
| val | 0-10 (int or float)  | Desired Brightness| 

Use picoh.setEyeBrightness() to change the brightness of the pixels on Picoh's matrix display. 

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

To see available phrases and write your own see the [Speech Database Tool](https://github.com/ohbot/picoh-python/tree/master/tools/SpeechDatabase). 

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

| Name| Range| Description  |
| --- |------|-------------|
| sensorNumber   | 0-6 (int) | the pin the sensor is connected to |

returns the value as a float 0 - 10.

For Example:
```python
reading = picoh.readSensor(3)

picoh.move(picoh.HEADTURN, reading)

```

picoh.playSound(sound,untilDone = True)
----------

sound - string name of sound.
untilDone - wait till sound has finished before moving to next line in  your program. Defaults to True. This is useful if you want to move Picoh while a sound is playing. 

sounds are read from picohData/Sounds/ add new sound files to this folder to access them. .wav files only for the moment. When writing the file name in your program please do not include the .wav file extension. 

Some demo sounds will be pre installed:

* fanfare
* loop
* ohbot
* smash
* spring

For Example:
```python
picoh.playSound('fanfare')

```
or

```python
picoh.playSound('spring',False)

```

picoh.setSynthesizer(synth)
----------
Use picoh.speechSpeed() to set text to speech engine used by Picoh.

picoh.setVoice(voice)
------
Use picoh.speechSpeed() to set the voice used by Pioch. 


picoh.speechSpeed(params)
------
Use picoh.speechSpeed() to set speech rate in words per minute.

More info on speech
---

Platform specific documentation for setting voices and languages:


* [macOS](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Mac.md)

* [Windows](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Windows.md)

* [Pi](https://github.com/ohbot/picoh-python/blob/master/Docs/VoiceDoc_Pi.md)
