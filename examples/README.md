# Examples

Hello, this directory contains some examples to help you get to grips with programming Picoh. 

***Don't forget if you are new to Python here is a short guide explaining some of the key concepts:*** [Programming Picoh in Python](https://docs.google.com/document/d/e/2PACX-1vTM9FmTBpGGJ4Ddvutpv3kxXkS0oyT4U9JPBV95UXdSJU10TD5JC1XWTf2cRGjHWApHOrTC6JLizD64/pub)

All the functions in the picoh library are also documented if you scroll down in the main [README](https://github.com/ohbot/picoh-python/blob/master/README.md).

Run an example
-

1) Right click and save as one of the files below.

2) Open and run in IDLE or whatever Python editor/launcher you prefer. 

[helloWorldPicoh.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/helloWorldPicoh.py)
-
A simple program that makes Picoh move and speak. 

 [threadingExample.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/threadingExample.py)
-
A more slightly more complicated program that uses threads to make Picoh do more than one thing at a time. 

 [Lights+Sounds.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/Lights%2BSounds.py)
-
A program that demonstrates how to play sounds using picoh.playSound()

 [ohClock.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/ohClock.py)
-
This program makes Picoh wake up every quarter of an hour and say the time. It also uses a second thread to blink Picoh's eyes.  

 [wolframAlphaPicoh](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/wolframAlphaPicoh.py)
-
This program uses the wolfram alpha and wikipedia web services to get definitions of words users type in. It builds upon the movements from the threadingExample. 

Requires:

Mac and Pi:

```sudo pip3 install wolframalpha```  

```sudo pip3 install wikipedia``` 

Windows:

```pip install wolframalpha```  

```pip install wikipedia``` 
