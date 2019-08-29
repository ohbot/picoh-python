from distutils.core import setup

setup(
    name = 'picoh',
    packages = ['picoh'],
    package_data={'': ['picohdefinitions.omd','Silence1.wav','PicohSpeech.csv','ohbot.obe']},
    include_package_data=True,
    version = '0.1',
    description = 'Python library for controlling Picoh Robot',
    author = 'ohbot',
    author_email = 'info@ohbot.co.uk',
    url = 'https://github.com/ohbot/picoh',
    download_url = 'https://github.com/ohbot/ohbotMac-python/archive/1.15.tar.gz',
    keywords = ['ohbot', 'robot','picoh'],
    classifiers = [],
    install_requires=[
          'pyserial','lxml','playsound','pyobjc',,
      ],
)
