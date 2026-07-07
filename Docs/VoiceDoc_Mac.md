# Picoh text to speech on a Mac


picoh.setSynthesizer(synth,ID = "",region ='westeurope')
----------

Allows override of default OSX synthesizer. 

If you have an Azure account you can use:

use picoh.setSynthesizer("Azure", "<key>", "<region>") 
where <key> and <region> come from your Azure acccount

You can set up a free Azure account here:

<a href="https://azure.microsoft.com/en-gb/free/" target="_blank"></a>

picoh.setVoice(voice,language = "en-GB", gender = 'Female')
language and gender are only supported by Azure voices.  Gender is overridden by the selected voice
------

Use picoh.setVoice() to set the voice:

For Example:
```python

picoh.setVoice("Oliver")
picoh.say("Hello this is Oliver")
picoh.setVoice("Kate")
picoh.say("Hello this is Kate")
picoh.setVoice("ClaraNeural","en-CA")
picoh.say("This is Clara speaking with a canadian voice")
```
Available voices can be found in System Preferences -> Accessibility -> Speech in the System Voice Menu. Click customize to view voices in other languages. 

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.53.56.png" border="0" width = "50%"/></a>

<a href="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" target="_blank"><img src="https://github.com/ohbot/ohbotMac-python/blob/master/images/Screen%20Shot%202018-02-24%20at%2023.54.07.png" border="0" width = "50%"/></a>

A full list of voices can also be displayed by entering the following command in Terminal:

```say -v ?```

For Azure speech you can get a list of voices here:

<a href="https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech" target="_blank"></a>


picoh.setSpeechSpeed(params)
------

Use picoh.setSpeechSpeed() to set speech rate in words per minute:

Range: (int) 90+


For Example:
```python

picoh.setVoice("Oliver")
picoh.setSpeechSpeed(90)
picoh.say("Hello this is Oliver Slow")
picoh.setSpeechSpeed(400)
picoh.say("Hello this is Oliver Fast")
```

