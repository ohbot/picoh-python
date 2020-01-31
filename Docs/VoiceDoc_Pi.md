Picoh supports both online and offline text to speech. 

Offline: <br>
Festival (Default) <br>
espeak <br>
pico2wave <br>

Online: <br>
gTTS <br>

Additonal voices can be used by installing the ```espeak``` or ```pico2wave``` synthesizers.

Offline:

 ```
 sudo apt-get install espeak
 sudo apt-get install libttspico-utils
 ```

Online :

 ```
 apt-get install libav-tools libavcodec-extra
 ```
 
 gTTS library is included as part of sudo pip3 install picoh.
 
 Ensure you you are running the latest version of the picoh library by running:
 
 ```
sudo pip3 install picoh --upgrade
 ```
 
picoh.setSynthesizer(synth)
----------

| synth | Full Name |
|----|-------- |
| “festival” | festival speech |
| “espeak” | espeak speech |
| “pico2wave” | pico2wave speech |
| “gTTS” | Google web based text to speech |


For Example:
```python
picoh.setSynthesizer("espeak")
```

or 

```python
picoh.setSynthesizer("pico2wave")
```

or 

```python
picoh.setSynthesizer("gTTS")
```

picoh.setVoice(voice)
------

Use picoh.setVoice() to set the voice synthesizer:

<b>Using ESPEAK</b>

http://espeak.sourceforge.net/commands.html<br>

| Name| Description|
| --- |------|
| -v followed by a letter code| execute 'espeak --voices' in terminal to see what's available |
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

More examples can be found in our [espeakVoices example program](https://github.com/ohbot/picoh-python/raw/master/examples/Pi/espeakVoices.py)  and  [pico2wave example program.](https://github.com/ohbot/picoh-python/raw/master/examples/Pi/pico2waveSpeech.py)


# Web Speech

Picoh supports Google Web speech using [gTTS](https://github.com/pndurette/gTTS). This provides a more realistic voice and support for multiple languages on the Raspberry Pi. Please note that using this speech means the text Picoh says is processed online on Google's servers. 

The language can be changed by setting picoh.language to a string containing a [google language code](https://cloud.google.com/speech-to-text/docs/languages).

For example:

```python
picoh.language = "da-DK"
```
or
```python
picoh.language = "en-GB"
```
or
```python
picoh.language = "en-US"
```

