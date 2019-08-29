from distutils.core import setup

setup(
    name = 'ohbotMac',
    packages = ['ohbotMac'],
    package_data={'': ['MotorDefinitionsv21.omd','Silence1.wav']},
    include_package_data=True,
    version = '1.15',  
    description = 'Python library for controlling Ohbot on a Mac',
    author = 'ohbot',
    author_email = 'info@ohbot.co.uk',
    url = 'https://github.com/ohbot/ohbotWin-python',
    download_url = 'https://github.com/ohbot/ohbotMac-python/archive/1.15.tar.gz',
    keywords = ['ohbot', 'robot'],
    classifiers = [],
    install_requires=[
          'pyserial','lxml','playsound','pyobjc',
      ],
)
