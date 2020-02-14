# Ohbot text to speech on Windows

picoh.setSynthesizer(synth)
----------

| synth | Full Name |
|----|-------- |
| “sapi” | SAPI speech |
| “espeak-ng” | espeak-ng speech |
| “espeak” | espeak speech |


For Example:
```python
picoh.setSynthesizer("espeak")
```

Note that the SAPI speech uses the voices available in Control Panel:Text to Speech.   It can’t use Cortana voices.


picoh.setVoice(voice)
------

Use picoh.setVoice() to set the voice depending on the synthesizer:

<b>Using SAPI</b>

Use any of the following arguments:

| Name| Description|
| --- |------|
| -a0 to -a100   | amplitude |
| -r-10 to r10   | rate |
| -v any part of the name of a SAPI voice (eg. -vHazel or -vZira) | voice |

For Example:
```python
picoh.setVoice("-a82 -r12 -vzira")

```

<b>Using ESPEAK</b>

http://espeak.sourceforge.net/commands.html<br>

| Name| Description|
| --- |------|
| -v followed by a letter code|look in program files\espeak\espeak-data\voices to see what's available|
|   +m1 to m7   | male voices |
|   +f1 to f4   | remale voices |
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

More examples can be found in our [voices example program.](https://github.com/ohbot/picoh-python/blob/master/examples/Windows/changingVoices.py)

<b>Using ESPEAK-NG</b>

Supports some of the ESPEAK parameters but some are missing.



