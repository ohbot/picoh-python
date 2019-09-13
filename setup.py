from distutils.core import setup

import platform

if platform.system() == "Darwin":
    includes =['pyserial','lxml','playsound','pyobjc','numpy','comtypes']

if platform.system() == "Windows":
    includes =['pyserial','lxml','playsound','numpy','comtypes']

if platform.system() == "Linux":
    includes =['pyserial','playsound']

setup(
    name = 'picoh',
    packages = ['picoh'],
      package_data={'': ['picohdefinitions.omd','Silence1.wav','picohspeech.wav','PicohSpeech.csv','ohbot.obe','phonemes.txt','Images/movedown.gif','Images/moveright.gif','Images/off.gif','Images/offsmaller.gif','Images/on.gif','Images/onsmaller.gif','Images/picohlogo.gif','Images/picohlogoOn.gif','Images/picohlogoSmall.gif','Images/plus.gif','Images/resetIcon.gif','Images/savebutton.gif','MotorDefinitionsPicoh.omd','Images/pixel.gif']},
    include_package_data=True,
    version = '1.0236',
    description = 'Python library for controlling Picoh Robot',
    author = 'ohbot',
    author_email = 'info@ohbot.co.uk',
    url = 'https://github.com/ohbot/picoh',
    download_url = 'https://github.com/ohbot/picoh-python/archive/1.tar.gz',
    keywords = ['ohbot', 'robot','picoh'],
    classifiers = [],
    install_requires= includes,
)
