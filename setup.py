from distutils.core import setup

import platform

if platform.system() == "Darwin":
    includes =['pyserial','lxml','playsound','pyobjc','numpy','comtypes','requests']

if platform.system() == "Windows":
    includes =['pyserial','lxml','playsound','numpy','comtypes','requests']

if platform.system() == "Linux":
    includes =['pyserial','playsound','gTTS','pydub','requests']

setup(
    name = 'picoh',
    packages = ['picoh'],
      package_data={'': ['PicohSettings.xml','Silence1.wav','picohspeech.wav','PicohSpeech.csv','ohbot.obe','phonemes.txt','Images/movedown.gif','Images/moveright.gif','Images/off.gif','Images/offsmaller.gif','Images/on.gif','Images/onsmaller.gif','Images/picohlogo.gif','Images/picohlogoOn.gif','Images/picohlogoSmall.gif','Images/calibrate400.gif','Images/calibrate2400.gif','Images/plus.gif','Images/resetIcon.gif','Images/savebutton.gif','Images/logoPT.gif','MotorDefinitionsPicoh.omd','Images/pixel.gif','Sounds/fanfare.wav','Sounds/loop.wav','Sounds/ohbot.wav','Sounds/smash.wav','Sounds/spring.wav']},
    include_package_data=True,
    version = '1.272',
    description = 'Python library for controlling Picoh Robot',
    author = 'ohbot',
    author_email = 'info@ohbot.co.uk',
    url = 'https://github.com/ohbot/picoh',
    download_url = 'https://github.com/ohbot/picoh-python/archive/1.26.tar.gz',
    keywords = ['ohbot', 'robot','picoh'],
    classifiers = [],
    install_requires= includes,
)
