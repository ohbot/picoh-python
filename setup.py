from distutils.core import setup

import platform

if platform.system() == "Darwin":
    includes =['pyserial','lxml','playsound','pyobjc','comtypes',]

if platform.system() == "Windows":
    includes =['pyserial','lxml','playsound','comtypes',]

if platform.system() == "Linux":
    includes =['pyserial','playsound']

setup(
    name = 'picoh',
    packages = ['picoh'],
    package_data={'': ['picohdefinitions.omd','Silence1.wav','picohspeech.wav','PicohSpeech.csv','ohbot.obe']},
    include_package_data=True,
    version = '0.137',
    description = 'Python library for controlling Picoh Robot',
    author = 'ohbot',
    author_email = 'info@ohbot.co.uk',
    url = 'https://github.com/ohbot/picoh',
    download_url = 'https://github.com/ohbot/ohbotMac-python/archive/1.15.tar.gz',
    keywords = ['ohbot', 'robot','picoh'],
    classifiers = [],
    install_requires= includes,
)
