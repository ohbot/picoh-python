# Eye Shape Designer. 

Use the EyeShapeDesigner to draw your own eye shapes to use in your Picoh programs. Design the eye shape, pupil shape and the 4 stages of blink animation. 

<a href="https://github.com/ohbot/picoh-python/blob/master/.images/eyedesignerscreenshot2.png?raw=true" target="_blank"><img src="https://github.com/ohbot/picoh-python/blob/master/.images/eyedesignerscreenshot2.png?raw=true" border="0" width = "100%"/></a>

Tested on Python 3.7.  on macOS and Windows 10 and Python 3.4 on Raspberry Pi. 

How to run
----------

1) Right click and save in your working directory: [EyeShapeDesigner.py](https://raw.githubusercontent.com/ohbot/picoh-python/master/tools/EyeShapeDesigner/EyeShapeDesigner.py)  

2) Run in IDLE or a Python editor of your choice. 

Features
----------
-Draw, modify and rename and delete eyeshapes.

-See your drawing on Picoh's matrix in real time. 

-Enable and disable an eyeshape's auto mirror setting.

-Animate Picoh's pupil using the mouse position to test your eye shape. 

-Test the blink animation you have draw using a button click. 


Using Eye Shapes
----------
The Eye Shape Designer will read and write eyeshapes from the Ohbot.obe file found within the picohData folder in your working directory.


If you want to use a shape you have designed in a program eg:

```python

picoh.setEyeShape("TestEyeShape")
```
Please ensure you save your program inside the same folder as the eye shape designer so they can both access the same copy of the picohData folder. See the Picoh Data folder section on the main [readme](https://github.com/ohbot/picoh-python/blob/master/README.md) for more information.

Set the left and right eyes to different shapes like this:

```python

picoh.setEyeShape("TestEyeShapeRight","TestEyeShapeLeft")
```

Auto Mirror
----------

Many eye shapes work well when the left eye is a mirror of the right eye, check the automirror box in the eye shape designer to toggle this setting for your eye shapes.For shapes where automirror is on the image in the right eye will be mirrored automatically. 


Picoh Button
----------

Press the Picoh button to disable/enable your drawings being previewed on Picoh. 
