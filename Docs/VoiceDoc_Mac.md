picoh.setSynthesizer(synth)
----------

Allows override of default OSX say command. 


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
picoh.setSpeechSpeed(90)
picoh.say("Hello this is Oliver Slow")
picoh.setSpeechSpeed(400)
picoh.say("Hello this is Oliver Fast")
```

