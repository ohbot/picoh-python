picoh.setSynthesizer(synth)
----------

| synth | Full Name |
|----|-------- |
| “festival” | festival speech |
| “espeak” | espeak speech |
| “pico2wave” | pico2wave speech |


For Example:
```python
picoh.setSynthesizer("espeak")
```

picoh.setVoice(voice)
------

Use picoh.setVoice() to set the voice synthesizer:

<b>Using ESPEAK</b>

http://espeak.sourceforge.net/commands.html<br>

| Name| Description|
| --- |------|
| -v followed by a letter code| enter 'espeak --voices' in terminal to see what's available|
|   +m1 to m7   | male voices |
|   +f1 to f4   | female voices |
|   +croak or whisper   | tone |
|   -a0 to a200   | amplitude |
|   -s80 to s500   | speed |
|   -p0 to p99   | pitch |


Examples:<br>

| Command | Result |
| ------ | ------- |
| ``picoh.setVoice("-ven+croak")`` | English croaky voice |
| ``picoh.setVoice("-vzh+m2 -s26")`` | Chinese male voice, Fast |
| ``picoh.setVoice("-vfr+f1 -p99 -s180")`` | French female whisper voice, medium speed and high pitched |

More examples can be found in our [espeakVoices example program](https://github.com/ohbot/picoh-python/blob/master/examples/Pi/espeakVoices.py)  and  [pico2wave example program.](https://github.com/ohbot/picoh-python/blob/master/examples/Pi/pico2waveSpeech.py)


**_Press fn + f5 to run your program_**

