# Picoh for Pi

This package is a starting point for people wanting to use Python 3 on a raspberry Pi to control Picoh. 

More information about Picoh can be found on [ohbot.co.uk](http://www.ohbot.co.uk)

Dependencies
----------

If you don't have python or pip3 (the python 3 package manager) installed, open terminal and execute the following:

```
sudo apt-get install python3
sudo apt-get install python3-pip
```

Picoh requires some libraries to be installed. 

To install libraries execute the corresponding terminal commands in your Raspberry Pi terminal:

| Library    | Use         | Terminal command to install  |Link |
| ---------- |-------------| -----------------------------|-----|
| picoh   | Interface with Picoh          | ```sudo pip3 install picoh``` |[picoh](https://github.com/picoh/picoh-python/) |
| festival    | Generate text to speech  | ```sudo apt-get install festival```  |- |
| espeak (optional)    | Generate text to speech  | ```sudo apt-get install espeak```  |[espeak](http://espeak.sourceforge.net/) |
| pico2wave (optional)    | Generate text to speech  | ```sudo apt-get install libttspico-utils```  |-|
| lxml    | Import settings file          | ```sudo apt-get install python3-lxml``` |[lxml](https://github.com/lxml/lxml) |
| serial    | Communicate with serial port | Included with Picoh |[pyserial](https://github.com/pyserial/pyserial/) |
| threading    | Run multiple threads     | Included in Python 3  |- |
| os    | Send commands to festival       | Included in Python 3  |- |
| time    | Run timers                    | Included in Python 3  |- |


You only need to install ```picoh```, ```lxml``` and ```festival```, ```serial``` should be installed automatically during the install of picoh. 

Additonal voices can be used by installing ```espeak``` and ```pico2wave```

Picoh is tested with Python 3 running on a Raspberry Pi 3 Model B. 

To upgrade to the latest version of the library run the following in the console:
```sudo pip3 install picoh --upgrade```


|Picoh library files (these will be installed with the `sudo pip3 install picoh` command above):

| File    | Use         |
| ---------- |------------|
| picoh.py   | Picoh package |
| picohdefinitions.omd    | Motor settings file |
| PicohSpeech.csv | Speech Database File |
| Ohbot.obe | EyeShape Files|


---

Hardware
-----

Required:


* Raspberry Pi
* Picoh
* USB Cable


Setup:

Connect Picoh to your mac using the USB cable. 

---

Writing Programs
--------

1. Open Python 3 (IDLE)
2. Click File → New File
3. Save your file as a python script (.py) in a new folder called Ohbot somewhere on your Pi.

Import
-------

Make sure you import picoh library at the start of your program. 
```python
from picoh import picoh
```

Go to the [helloworldpicoh](https://raw.githubusercontent.com/ohbot/picoh-python/master/examples/Pi/helloworldpicoh.py) example, copy the code and paste it into the new Python window.

Select <b>Run Module</b> from the <b>Run</b> menu.

Picoh should speak and move.

More example programs can be found [here.](https://github.com/ohbot/picoh-python/tree/master/examples/Pi)

