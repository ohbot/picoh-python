# This is a script to help control a Picoh Robot. www.ohbot.co.uk

import platform
import serial
import serial.tools.list_ports
import time
import threading
import os
import os.path
from os import path
import shutil
import sys
import wave
import subprocess
from lxml import etree
import random
import re
import csv

# Import the correct sound library depending on platform.
if platform.system() == "Windows":
    import winsound
    # For SAPI speech
    from comtypes.client import CreateObject
    from comtypes.gen import SpeechLib
if platform.system() == "Darwin":
    from playsound import playsound
if platform.system() == "Linux":
    from playsound import playsound
    from gtts import gTTS
    from pydub import AudioSegment
  
# Variables to hold name of settings

speechDatabaseFile = ''
defaultEyeShape = ''
eyeShapeFile = ''
speechAudioFile = 'picohData/picohspeech.wav'
picohMotorDefFile = 'picohData/MotorDefinitonsPicoh.omd'
soundFolder = 'picohData/Sounds'
synthesizer = ''
voice = ''
language = 'en-GB' # Language/Accent for GTTS web text to speech.
settingsFile = 'picohData/PicohSettings.xml' # String to hold location of settings file

# Variable to hold the location of the picoh library folder.
directory = os.path.dirname(os.path.abspath(__file__))

# name of directory that holds eye shape, motor definition and speech db files.
dirName = 'picohData'

# Global variable to turn on and off printing debug info.
debug = False

# define constants for motors
HEADNOD = 0
HEADTURN = 1
EYETURN = 2
LIDBLINK = 3
TOPLIP = 4
BOTTOMLIP = 5
EYETILT = 6

# array to hold sensor values.
sensors = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Put motor ranges into lists
motorPos = [11, 11, 11, 11, 11, 11, 11, 11]
motorMins = [0, 0, 0, 0, 0, 0, 0, 0]
motorMaxs = [0, 0, 0, 0, 0, 0, 0, 0]
motorRev = [False, False, False, False, False, False, False, False]
restPos = [0, 0, 0, 0, 0, 0, 0, 0]
isAttached = [False, False, False, False, False, False, False, False]
motorType = ["", "", "", "", "", "", "", ""]

# empty lists to hold eye shapes and phrases from speech databa se.
shapeList = []
phraseList = []

# define a module level variable for the serial port
port = ""

# define library version
version = "1.252"

# flag to stop writing when writing for threading
writing = False

# flag to allow the library to run when not connected
connected = False

# flag to track if top lip is below centre.
topLipFree = False

# If the picohData folder does not exist, create it.
try:
    # Create target Directory
    os.mkdir(dirName)
except FileExistsError:
    pass

# Copy settings file
if not path.exists('picohData/PicohSettings.xml'):
    shutil.copyfile(os.path.join(directory, "PicohSettings.xml"), settingsFile)
    if debug:
        print("Copied Picoh Settings from :" + directory + " to picohData/")

# Load settings from XML file.
def _loadSettings():
    global eyeShapeFile,defaultEyeShape,synthesizer,voice,speechDatabaseFile,eyeShapeFile,picohMotorDefFile
    
    tree = etree.parse(settingsFile)

    
    root = tree.getroot()

    for element in tree.iter():

        name = element.get("Name")
        val = element.get("Value")

        if name == "DefaultEyeShape":
            defaultEyeShape = val
            
        if name == "DefaultSpeechSynth":
            synthesizer = val

        if name == "DefaultVoice":
            voice = val

        if name == "DefaultLang":
            language = val

        if name == "SpeechDBFile":
            speechDatabaseFile = val

        if name == "EyeShapeList":
            eyeShapeFile = val

        if name == "MotorDefFile":
            picohMotorDefFile = val

_loadSettings()

# Copy over files
if not path.exists(speechDatabaseFile):
    shutil.copyfile(os.path.join(directory, 'PicohSpeech.csv'),speechDatabaseFile)
    if debug:
        print("Copied PicohSpeech.csv from :" + directory + " to picohData/")

if not path.exists(eyeShapeFile):
    shutil.copyfile(os.path.join(directory, 'ohbot.obe'), eyeShapeFile)
    if debug:
        print("Copied ohbot.obe from :" + directory + " to picohData/")

if not path.exists(picohMotorDefFile):
    shutil.copyfile(os.path.join(directory, 'MotorDefinitionsPicoh.omd'), picohMotorDefFile)
    if debug:
        print("Copied MotorDefinitionsPicoh.omd from :" + directory + " to picohData/")

if not path.exists(soundFolder):

    shutil.copytree(os.path.join(directory, 'Sounds'),soundFolder)

    if debug:
        print("Copied Sounds from :" + directory + " to PicohData/")

# global to set the params to speech synthesizer which control the voice
# Global flag to use a synthesizer other than sapi.
# If it's not sapi then it needs to support -w parameter to write to file e.g. espeak or espeak-NG

if platform.system() == "Windows":
    if synthesizer == "":
        synthesizer = "sapi"
if platform.system() == "Darwin":
    if synthesizer == "":
        synthesizer = "say -o "
if platform.system() == "Linux":
    if synthesizer == "":
        synthesizer = "festival"
    # un-comment to make google webspeech default
    # synthesizer = "gTTS" 

# global to set the speech speed.
speechRate = 170

print("Speech Synthesizer: " + synthesizer)

try:
    # Display logo on Pi-Top[4]
    from ptoled import PTOLEDDisplay
    oled_screen = PTOLEDDisplay()
    logoImagePath = os.path.join(directory, 'Images/logoPT.gif')
    oled_screen.draw_image_file(logoImagePath)
except:
    pass

if debug:
    print("Picoh Library Directory " + directory)


# Cache of pupil positions
global lastfex, lastfey
lastfex = 5
lastfey = 5

ser = None

# A class that defines eye shape objects.

class EyeShape(object):

    def __init__(self, name_value, hexString_value, autoMirror_value, pupilRangeX_value, pupilRangeY_value):
        self.name = name_value
        self.hexString = hexString_value
        self.autoMirror = autoMirror_value
        self.pupilRangeX = pupilRangeX_value
        self.pupilRangeY = pupilRangeY_value

# A class that defines speech phrase objects.

class Phrase(object):

    def __init__(self, set, variable, text):
        self.set = set
        self.variable = variable
        self.text = text
            
# Used during calibration.
def _revertMotorDefsFile():
    shutil.copyfile(os.path.join(directory, 'MotorDefinitionsPicoh.omd'), os.path.join('picohData',picohMotorDefFile))
    _loadMotorDefs()

# Read motor definitions file.
def _loadMotorDefs():
    tree = etree.parse(picohMotorDefFile)
    root = tree.getroot()
    # For each line in motor defs file
    for child in root:
        indexStr = child.get("Motor")
        index = int(indexStr)
        motorMins[index] = int(int(child.get("Min")) / 1000 * 180)
        motorMaxs[index] = int(int(child.get("Max")) / 1000 * 180)
        motorPos[index] = int(child.get("RestPosition"))
        restPos[index] = int(child.get("RestPosition"))
        motorType[index] = child.get("MotorType")

        if child.get("Reverse") == "True":
            rev = True
            motorRev[index] = rev
        else:
            rev = False
            motorRev[index] = rev

            
# Read eyeshape file into eyeshape list.
def _loadEyeShapes():
    global shapeList

    # Clear the shapeList
    shapeList = []
    tree = etree.parse(eyeShapeFile)
    index = 0

    for element in tree.iter():

        if element.tag == "Name":
            shapeList.append(EyeShape(str(element.text), "", False, 5, 5))

        if element.tag == "PupilRangeX":
            shapeList[index].pupilRangeX = int(element.text)

        if element.tag == "PupilRangeY":
            shapeList[index].pupilRangeY = int(element.text)

        if element.tag == "Hex":
            shapeList[index].hexString = element.text

        if element.tag == "AutoMirror":
            if element.text == "true":
                shapeList[index].autoMirror = True

            else:
                shapeList[index].autoMirror = False

            index = index + 1
       
# Read speech database file into phraseList.
def _loadSpeechDatabase():
    global phraseList

    # Clear the phrase list.

    phraseList = []

    file = speechDatabaseFile

    with open(file, 'rt')as f:
        data = csv.reader(f)

        for row in data:
            if row[2] != '' and row[0] != 'Set':
                if row[0] == '' and row[1] == '':
                    newPhrase = Phrase('', '', row[2])
                    phraseList.append(newPhrase)

                elif row[0] == '' and row[1] != '':
                    newPhrase = Phrase('', int(row[1]), row[2])
                    phraseList.append(newPhrase)

                elif row[0] != '' and row[1] == '':
                    newPhrase = Phrase(row[0], '', row[2])
                    phraseList.append(newPhrase)

                else:
                    newPhrase = Phrase(row[0], row[1], row[2])
                    phraseList.append(newPhrase)

                    
# Function to check if a number is a digit including negative numbers
def _is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


# Function to parse SAPI settings from voice override
# -a0 to -a100 for amplitude
# -r-10 to r10 for rate
# -v any part of the name of a SAPI voice e.g. -vHazel, -vZira
# e.g. "-a82 -r12 -vzira"
def _parseSAPIVoice(flag):
    pos = voice.find("-" + flag)
    val = ""
    if ((pos != None) and (pos >= 0)):
        val = voice[pos + 2:]
        pos = val.find(" ")
        if ((pos != None) and (pos > 0)):
            val = val[:pos]
    return val

# generate speech file depending on platform and sythensizer.
def _generateSpeechFile(text):
    # Pick up the global variable that defines the language. This is only used in GTTS speech.
    global language
    file = speechAudioFile
    if platform.system() == "Windows":
        if ("sapi" in synthesizer.lower()):
            #from comtypes.gen import SpeechLib
            global sapivoice, sapistream

            sapistream.Open(file, SpeechLib.SSFMCreateForWrite)
            sapivoice.AudioOutputStream = sapistream

            # set any parameters
            sa = _parseSAPIVoice("a");
            if _is_digit(sa):
                sapivoice.Volume = int(sa)
            else:
                sapivoice.Volume = 100
            sr = _parseSAPIVoice("r")
            if _is_digit(sr):
                sapivoice.Rate = int(sr)
            else:
                sapivoice.Rate = 0
            sv = _parseSAPIVoice("v");
            # Default voice is always first in the list
            if (sv == ''):
                sapivoice.voice = sapivoice.GetVoices()[0]
            else:
                for v in sapivoice.GetVoices():
                    if (sv.lower() in v.GetDescription().lower()):
                        sapivoice.voice = v

            sapivoice.Speak(text)
            sapistream.Close()
        else:
            # Remove any characters that are unsafe for a subprocess call
            safetext = re.sub(r'[^ .a-zA-Z0-9?\']+', '', text)

            bashcommand = synthesizer + ' -w ' + file + ' ' + voice + ' "' + safetext + '"'
            # Execute bash command.
            subprocess.call(bashcommand, shell=True)
            if debug:
                print("Speech Bash Command")
                print(bashcommand)

    if platform.system() == "Darwin":
        # Remove any characters that are unsafe for a subprocess call
        safetext = re.sub(r'[^ .a-zA-Z0-9?\']+', '', text)

        file = speechAudioFile

        if voice:
            bashcommand = synthesizer + file + ' --file-format=RF64 --data-format=LEI16@22050 -r' + str(
                speechRate) + ' -v ' + voice + ' "' + safetext + '"'
        else:
            bashcommand = synthesizer + file + ' --file-format=RF64 --data-format=LEI16@22050 -r' + str(
                speechRate) + ' "' + safetext + '"'

        if debug:
            print("Speech Bash Command:")
            print(bashcommand)

        # Execute bash command.
        ret = subprocess.Popen(bashcommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        retval = ret.wait()
        # print(retval)

    if platform.system() == "Linux":

        #if we are using gTTS web speech.
        if synthesizer.upper() == "GTTS":
            # Passing the text and language to the engine
            tts = gTTS(text=text, lang=language, slow=False)

            # Saving the converted audio in a wav file named sample
            tts.save('picohData/picohspeech.mp3')
            sound = AudioSegment.from_mp3('picohData/picohspeech.mp3')
            sound.export('picohData/picohspeech.wav', format="wav")
        else:
            # Remove any characters that are unsafe for a subprocess call
            safetext = re.sub(r'[^ .a-zA-Z0-9?\']+', '', text)
                      
            if synthesizer.upper() == "FESTIVAL":
                bashcommand = "festival -b '(set! mytext (Utterance Text " + '"' + safetext + '"))' + "' '(utt.synth mytext)' '(utt.save.wave mytext " + '"picohData/picohspeech.wav")' + "' '(utt.save.segs mytext " + '"picohData/phonemes"' + ")'"
            else:
                bashcommand = synthesizer + ' -w picohData/picohspeech.wav ' + voice + ' "' + safetext + '"'
                
            # Execute bash command.
            subprocess.call(bashcommand, shell=True)

            if debug:
                print("Speech Bash Command:")
                print(bashcommand)

def init(portName):
    # pickup global instances of port, ser and sapi variables
    global port, ser, sapivoice, sapistream, connected, directory

    _loadEyeShapes()
    _loadMotorDefs()

    silenceFile = os.path.join(directory, 'Silence1.wav')

    # get the sapi objects ready on Windows
    if platform.system() == "Windows":
        sapivoice = CreateObject("SAPI.SpVoice")
        sapistream = CreateObject("SAPI.SpFileStream")
        winsound.PlaySound(silenceFile, winsound.SND_FILENAME)

    # get the audio system warmed up on Mac
    if platform.system() == "Darwin":
        playsound(silenceFile)

    # get the audio system warmed up on linux
    if platform.system() == "Linux":
        os.system('aplay ' + silenceFile)

    # Search for the Picoh serial port
    ports = list(serial.tools.list_ports.comports())
    for p in ports:

        # If port has Picoh connected save the location
        if portName in p[1]:
            port = p[0]
            print("Picoh found on port:" + port)
            connected = True
        elif portName in p[0]:
            port = p[0]
            print("Picoh found on port:" + port)
            connected = True

    # If not found then try the first port
    if port == "":
        for p in ports:
            port = p[0]
            print("Picoh not found")
            connected = False
            break

    if port == "":
        print("Picoh port " + portName + " not found")
        return False

    # Open the serial port
    if connected:
        ser = serial.Serial(port, 19200)
        ser.timeout = None
        ser.write_timeout = None

    # Set read timeout and write timeouts to blocking

    # Make an initial call to Festival without playing the sound to check it's all okay
    text = "Hi"

    # Create a bash command with the desired text. The command writes two files, a .wav with the speech audio and a
    # .txt file containing the phonemes and the times.

    if synthesizer.lower() != "festival":
        _generateSpeechFile(text)
        
    _loadSpeechDatabase()

    return True

# initialise with any port that has USB Serial Device in the name

if platform.system() == "Windows":
    init("USB Serial Device")
if platform.system() == "Darwin":
    init("usbmodem")
if platform.system() == "Linux":
    init("Arduino")

def getDirectory():
    global directory
    return directory

# Function to move Picoh's motors. Arguments | m (motor) → int (0-6) | pos (position) → int (0-10) | spd (speed) →
# int (0-10) **eg move(4,3,9) or move(0,9,3)**
def move(m, pos, spd=5, eye=0):
    global lastfex, lastfey, topLipFree

    # Limit values to keep then within range
    pos = _limit(pos)
    spd = _limit(spd)

    # Keeping track of whether the top lip is pushed below the centre stop.

    if pos > 9 and m == BOTTOMLIP:
        topLipFree = True

    if pos <= 5 and m == BOTTOMLIP:
        topLipFree = False

    if pos < 5 and m == BOTTOMLIP:
        pos = 5 - ((5 - pos) / 2)

    # Reverse the motor if necessary
    if motorRev[m]:
        pos = 10 - pos

    if debug:
        print("Moved motor number " + str(m) + " to position " + str(pos))

    # Eyeturn
    if (motorType[m] == "Matrix X"):
        pos = (pos - 5) * 0.4 + 5  # Bodge to reduce the scale
        msg = "FE," + str(eye) + "," + "{:0.0f}".format(pos * 255 / 10) + "," + "{:0.0f}".format(lastfey * 255 / 10) + "\n"

        # print ("fex:" + msg)
        # Write message to serial port
        _serwrite(msg)
        lastfex = pos
        return

    # Eyetilt
    if (motorType[m] == "Matrix Y"):
        pos = (pos - 5) * 0.4 + 5  # Bodge to reduce the scale
        msg = "FE," + str(eye) + "," + "{:0.0f}".format(lastfex * 255 / 10) + "," + "{:0.0f}".format(pos * 255 / 10) + "\n"
        # print ("fey:" + msg)
        # Write message to serial port
        _serwrite(msg)
        lastfey = pos
        return

    # Blink
    if (motorType[m] == "Matrix Lid"):
        msg = "FL,+" + str(eye) + "," + "{:0.0f}".format((10 - pos) * 255 / 10) + "\n"
        # print ("fl:" + msg)
        # Write message to serial port
        _serwrite(msg)
        return

    # Attach motor
    attach(m)

    # Convert position (0-10) to a motor position in degrees
    absPos = int(_getPos(m, pos))

    # Scale range of speed
    spd = (250 / 10) * spd

    # Construct message from values
    msg = "m0" + str(m) + "," + str(absPos) + "," + str(spd) + "\n"

    # Write message to serial port
    _serwrite(msg)

    # Update motor positions list
    motorPos[m] = pos


# Function to write to serial port
def _serwrite(s):
    global connected, writing

    if debug:
        print("Serial command sent to Picoh:")
        print(s)
    if platform.system() == "Windows" or platform.system() == "Linux":
        # wait until previous write is finished
        while (writing):
            pass
        # print ('waiting on write')

    if connected:
        writing = True
        ser.write(s.encode('latin-1'))
        writing = False

    # Function to attach Picoh's motors. Argument | m (motor) int (0-6)


def attach(m):
    if isAttached[m] == False:
        # Construct message
        msg = "a0" + str(m) + "\n"

        # Write message to serial port
        _serwrite(msg)

        # Update flag
        isAttached[m] = True


# Function to detach Picoh's motors.  Argument | m (motor) int (0-6)
def detach(m):
    msg = "d0" + str(m) + "\n"
    _serwrite(msg)
    isAttached[m] = False


# Function to find the scaled position of a given motor. Arguments | m (motor) → int (0-6) | pos (position) → int (0-10) | Returns a position
def _getPos(m, pos):
    mRange = motorMaxs[m] - motorMins[m]
    scaledPos = (mRange / 10) * pos
    return scaledPos + motorMins[m]


# Function to set the language used by gTTS web speech synthesizer
# name - run 'say -v ?' in terminal to find available names.
def setLanguage(params=language):
    global language
    language = params

# Function to set the voice used by the synthesiser
# name - run 'say -v ?' in terminal to find available names.
# speed - speech rate in words per min.
# This override will stay in use until it's next called
def setVoice(params=voice):
    global voice
    voice = params

# Function to set a different speech synthesizer - defaults to sapi
def setSynthesizer(params=synthesizer):
    global synthesizer
    synthesizer = params

# Set the speed of the speech in words per min.
def speechSpeed(params=speechRate):
    global speechRate
    speechRate = params
    
# Set the speed of the speech in words per min mirrors speechSpeed for consistency.
def setSpeechSpeed(params=speechRate):
    global speechRate
    speechRate = params

# Function to make Picoh Speak. Arguments | text String "Hello World" **eg say("Hello my name is Picoh")
# untilDone - wait in function until speech is complete, lipSync - move lips in time with speech, hdmiAudio - adds a delay to give hdmi channel time to activate.
# soundDelay - positive if lip movement is lagging behind sound, negative if sound is lagging behind lip movement.
def say(text, untilDone=True, lipSync=True, hdmiAudio=False, soundDelay=0):
    global topLipFree

    if topLipFree:
        move(BOTTOMLIP, 4)
        wait(0.25)
    
    if text.isspace() or text == '':
        return
    text = text.replace("picoh", "peek oh")
    text = text.replace("Picoh", "peek oh")
    
    if hdmiAudio:
        soundDelay = soundDelay - 1

    # Create a bash command with the desired text. espeak.exe or another synthesizer must be in the current folder.  the -w parameter forces the speech to a file
    _generateSpeechFile(text)
    
    if synthesizer.upper() == "FESTIVAL":
        
        # Open the text file containing the phonemes

        f = open("picohData/phonemes", 'r')

        # Empty the lists that contain phoneme data and reset count
        phonemes = []
        times = []
        vals = []

        # Read a line to move past the first line
        line = f.readline()

        # While there are more lines to read.
        while line:

            # Read the line
            line = f.readline()

            # Split the line into values
            vals = line.split()

            # If values exist add the phoneme to the phonemes list and the timecode to the times list.
            if vals:
                phonemes.append(vals[2])
                times.append(float(vals[0]))
    else:
        
        # open the file to calculate visemes. Festival on RPi has this built in but for espeak need to do it manually

        waveFile = wave.open(speechAudioFile, 'r')

        length = waveFile.getnframes()
        framerate = waveFile.getframerate()
        channels = waveFile.getnchannels()
        bytespersample = waveFile.getsampwidth()

        # How many samples per second for mouth position
        if platform.system() == "Windows":
            VISEMESPERSEC = 10
        if platform.system() == "Darwin":
            VISEMESPERSEC = 10
        if platform.system() == "Linux":
            VISEMESPERSEC = 10

        # How many samples in 1/20th second
        # print ('framerate:', framerate, ' channels:', channels, ' length:', length, ' bytespersample:', bytespersample)

        chunk = int(waveFile.getframerate() / VISEMESPERSEC)
        # print ('chunk:', chunk)

        # Empty the lists that contain phoneme data and reset count
        phonemes = []
        times = []

        ms = 0

        for i in range(0, length - chunk, chunk):
            vol = 0
            buffer = waveFile.readframes(chunk)
            # frame is 1 sample for mono or 2 for stereo
            bytesread = chunk * channels * bytespersample
            # print ('bytesread:', bytesread)
            index = 0;
            for sample in range(0, int(bytesread / (channels * bytespersample))):
                vol += buffer[index]
                vol += buffer[index + 1] * 256
                index += bytespersample
                if channels > 1:
                    vol += buffer[index]
                    vol += buffer[index + 1] * 256
                    index += bytespersample

            # print ('viseme', i, ":", ms, ':', vol)
            ms += (1000 / VISEMESPERSEC);

            phonemes.append(float(vol))
            times.append(float(ms) / 1000)

        # Back to the beginning for next use
        waveFile.rewind()

        # Normalise the volume
        max = 0
        for i in range(0, len(phonemes) - 1):
            if phonemes[i] > max:
                max = phonemes[i]

        for i in range(0, len(phonemes) - 1):
            phonemes[i] = phonemes[i] * 10 / max
            # print ('visnorm', i, ":", times[i], ':', phonemes[i])
    
    # Use the bottom lip to push the top lip above the centre point if it is below
       
    if lipSync:
        if soundDelay > 0:
            # Set up a thread for the speech sound synthesis, delay start by soundDelay
            t = threading.Timer(soundDelay, _playSpeech, args=(hdmiAudio,), kwargs=None)
            # Set up a thread for the speech movement
            t2 = threading.Thread(target=_moveSpeech, args=(phonemes, times))
        else:
            # Set up a thread for the speech sound synthesis
            t = threading.Thread(target=_playSpeech, args=(hdmiAudio,))
            # Set up a thread for the speech movement, delay start by - soundDelay
            t2 = threading.Timer(-soundDelay, _moveSpeech, args=(phonemes, times), kwargs=None)
        t2.start()
    else:
        # Set up a thread for the speech sound synthesis
        t = threading.Thread(target=_playSpeech, args=(hdmiAudio,))
    t.start()

    # if untilDone, keep running until speech has finished
    if untilDone:
        totalTime = times[len(times) - 1]
        startTime = time.time()
        while time.time() - startTime < totalTime:
            continue
                
# Function to play back the speech wav file, if hmdi audio is being used play silence before speech sound
def _playSpeech(addSilence):
    dir = os.path.dirname(os.path.abspath(__file__))
    silenceFile = os.path.join(dir, 'Silence1.wav')

    speechFile = speechAudioFile
    if platform.system() == "Windows":

        if addSilence:
            winsound.PlaySound(silenceFile, winsound.SND_FILENAME)
        winsound.PlaySound(speechFile, winsound.SND_FILENAME)

    if platform.system() == "Darwin":
        if addSilence:
            playsound(silenceFile)
        playsound(speechFile)

    if platform.system() == "Linux":
        if addSilence:
            commandString = 'aplay -D plug:default ' + silenceFile + '\naplay picohData/picohspeech.wav'
            os.system(commandString)
        else:
            os.system('aplay -D plug:default picohData/picohspeech.wav')


# Function to move Picoh's lips in time with speech. Arguments | phonemes → list of phonemes[] | waits → list of waits[]
def _moveSpeech(phonemes, times):
    startTime = time.time()
    timeNow = 0
    totalTime = times[len(times) - 1]
    currentX = -1
    while timeNow < totalTime:
        timeNow = time.time() - startTime
        for x in range(0, len(times)):
            if timeNow > times[x] and x > currentX:
                if synthesizer.upper() == "FESTIVAL":
                    #posTop = _phonememapTopFest(phonemes[x])
                    posBottom = _phonememapBottomFest(phonemes[x])
                else:
                    posTop = _phonememapTop(phonemes[x])
                    posBottom = _phonememapBottom(phonemes[x])
                # move(TOPLIP, posTop, 10)
                posBottom = (((posBottom-5)/5)*3)+5
                move(BOTTOMLIP, posBottom, 10)
                currentX = x
    # move(TOPLIP, 5)
    move(BOTTOMLIP, 5)
    

# Function to limit values so they are between 0 - 10    
def _limit(val):
    if val > 10:
        return 10
    elif val < 0:
        return 0
    else:
        return val

# Function mapping phonemes to top lip positions. Argument | val → phoneme | returns a position as int
def _phonememapTopFest(val):
    return {
        'p': 5,
        'b': 5,
        'm': 5,
        'ae': 7,
        'ax': 7,
        'ah': 7,
        'aw': 10,
        'aa': 10,
        'ao': 10,
        'ow': 10,
        'ey': 7,
        'eh': 7,
        'uh': 7,
        'ay': 7,
        'h': 7,
        'er': 8,
        'r': 8,
        'l': 8,
        'y': 6,
        'iy': 6,
        'ih': 6,
        'ix': 6,
        'w': 6,
        'uw': 6,
        'oy': 6,
        's': 5,
        'z': 5,
        'sh': 5,
        'ch': 5,
        'jh': 5,
        'zh': 5,
        'th': 5,
        'dh': 5,
        'd': 5,
        't': 5,
        'n': 5,
        'k': 5,
        'g': 5,
        'ng': 5,
        'f': 6,
        'v': 6
    }.get(val, 5)


# Function mapping phonemes to lip positions. Argument | val → phoneme | returns a position as int
def _phonememapBottomFest(val):
    return {
        'p': 5,
        'b': 5,
        'm': 5,
        'ae': 8,
        'ax': 8,
        'ah': 8,
        'aw': 5,
        'aa': 10,
        'ao': 10,
        'ow': 10,
        'ey': 7,
        'eh': 7,
        'uh': 7,
        'ay': 7,
        'h': 7,
        'er': 8,
        'r': 8,
        'l': 8,
        'y': 6,
        'iy': 6,
        'ih': 6,
        'ix': 6,
        'w': 6,
        'uw': 6,
        'oy': 6,
        's': 6,
        'z': 6,
        'sh': 6,
        'ch': 6,
        'jh': 6,
        'zh': 6,
        'th': 6,
        'dh': 6,
        'd': 6,
        't': 6,
        'n': 6,
        'k': 6,
        'g': 6,
        'ng': 6,
        'f': 5,
        'v': 5
    }.get(val, 5)

# Function mapping phonemes to top lip positions.
def _phonememapTop(val):
    return 5 + (_limit(val) / 2)

# Function mapping phonemes to top lip positions.
# Bottom lip never goes over 9
def _phonememapBottom(val):
    return 5 + (_limit(val) * 3 / 10)

# Legacy function to support Ohbot programs with eyeColour. Passes onto baseColour.
def eyeColour(r, g, b, swapRandG=False):
    baseColour(r, g, b, swapRandG)

# Clone of base colour to keep consitency with set eyeShape etc.
def setBaseColour(r, g, b, swapRandG=False):
    baseColour(r, g, b, swapRandG)

# US Spelling
def setBaseColor(r, g, b, swapRandG=False):
    baseColour(r, g, b, swapRandG)

# Function to set the color of the LEDs in Picoh's base. Arguments | r (red) → int (0-10) | g (green) → int (0-10) | b (blue) → int (0-10)
# swapRandG is used to swap the red and green values as this is required for some LEDs
def baseColour(r, g, b, swapRandG=False):
    # Limit the values to keep them within range.
    r = _limit(r)
    g = _limit(g)
    b = _limit(b)

    # Scale the values so they are between 0 - 255.
    r = int((255 / 10) * r)

    g = int((255 / 10) * g)

    b = int((255 / 10) * b)

    # Construct a message with the values.
    if swapRandG:
        msg1 = "l00," + str(g) + "," + str(r) + "," + str(b) + "\n"
        msg2 = "l01," + str(g) + "," + str(r) + "," + str(b) + "\n"
    else:
        msg1 = "l00," + str(r) + "," + str(g) + "," + str(b) + "\n"
        msg2 = "l01," + str(r) + "," + str(g) + "," + str(b) + "\n"

    # Write message to serial port.
    _serwrite(msg1)
    _serwrite(msg2)

# Wait for a number of seconds. 
def wait(seconds):
    time.sleep(float(seconds))
    return

# Detach each of Picoh's motors.
def close():
    for x in range(0, len(motorMins) - 1):
        detach(x)

    # Reset Picoh back to start position
def reset():
    baseColour(0, 0, 0)
    setEyeShape(defaultEyeShape, defaultEyeShape)
    for x in range(len(restPos) - 1,-1,-1):
        move(x, restPos[x])
        wait(0.1)
    close()

# Return the sensor value between 0-10 for a given sensor number. Values stored in sensors[] array.
def readSensor(index):
    ser.flushInput()

    msg = "i0" + str(index) + "\n"
    _serwrite(msg)

    line = ser.readline()
    lineStr = line.decode("utf-8")
    lines = lineStr.split(",")

    if len(lines) > 1:
        indexIn = lines[0]
        indexIn = indexIn[1]

        intdex = int(indexIn)

        newVal = int(lines[1]) / 1024
        newVal = newVal * 10
        sensors[intdex] = _limit(newVal)

    return sensors[index]


# set the brightness of the eyes.  Value is 0 (off) to 10 (full brightness)
def setEyeBrightness(val):
    val = val / 10
    val = val * val
    msg = "{:0.0f}".format(val * 255)

    # print ("brightness:" + msg)

    _serwrite("FI," + msg + "\n")

# set the eye shape according to the passed in eyeshapedefinition
# eysshape definition is 6 sets of 9 hex pairs which set the bits of half of the screen
# the other half of the screen is a mirror copy
# the first 5 sets of pairs set the normal eye and 4 blink positions
# the last set of pairs set the pupil
# set the eye shape according to the passed in eyeshapedefinition
# eyeshape definition is 6 sets of 9 hex pairs which set the bits of half of the screen
# the other half of the screen is a mirror copy
# the first 5 sets of pairs set the normal eye and 4 blink positions
# the last set of pairs set the pupil
def _setEyes(leftDefinition, rightDefinition="", autoMirror=True):
    # TODO needs some work here to use both definitions for independent eye shapes
    # and to define the pupil range and offset
    definition = leftDefinition

    if rightDefinition == "":
        rightDefinition = definition

    _serwrite("FB,0," + _EyeShapeBytes(definition, rightDefinition, 0, autoMirror) + "\n")
    _serwrite("FB,1," + _EyeShapeBytes(definition, rightDefinition, 1, autoMirror) + "\n")
    _serwrite("FB,2," + _EyeShapeBytes(definition, rightDefinition, 2, autoMirror) + "\n")
    _serwrite("FB,3," + _EyeShapeBytes(definition, rightDefinition, 3, autoMirror) + "\n")
    _serwrite("FB,4," + _EyeShapeBytes(definition, rightDefinition, 4, autoMirror) + "\n")
    # Pupil is held in set 6 and has been implemented in the Arduino driver as FB 8
    _serwrite("FB,8," + _EyeShapeBytes(definition, rightDefinition, 5, autoMirror) + "\n")

# function for getting a string that defines the 16 x 9 matrix for a particular 8 x 9 eyeshapedefinition
# setNo is 0 for the normal eyeshape, 1 to 4 for blink shapes or 5 for the pupil
def _EyeShapeBytes(definitionR, definition, setNo, autoMirror):
    strRet = ""
    for x in range(0, 9):
        if (len(strRet) > 0):
            strRet += ","
        offset = setNo * 18 + x * 2

        if autoMirror:
            strRet += (definition[offset: offset + 2])
        else:
            strRet += _reverseBits(definition[offset: offset + 2])

        strRet += _reverseBits(definitionR[offset: offset + 2])
    if debug:
        print ("eyeshape set:" + str(set) + ": " + strRet)

    return strRet

# reverse the bits of a two byte hex number
def _reverseBits(str):
    # print ("str: " + str)
    x = int(str, 16)
    r = 0

    if (x & 0x80):
        r += 0x01
    if (x & 0x40):
        r += 0x02
    if (x & 0x20):
        r += 0x04
    if (x & 0x10):
        r += 0x08
    if (x & 0x08):
        r += 0x10
    if (x & 0x04):
        r += 0x20
    if (x & 0x02):
        r += 0x40
    if (x & 0x01):
        r += 0x80

    # https://stackoverflow.com/questions/2269827/how-to-convert-an-int-to-a-hex-string
    return "%0.2X" % r

def setEyeShape(shapeNameRight, shapeNameLeft=''):
    global shapeList

    if shapeNameLeft == '':
        shapeNameLeft = shapeNameRight

    leftHex = ''

    for index, shape in enumerate(shapeList):
        if shape.name.upper() == shapeNameRight.upper():
            rightHex = shape.hexString

    for index, shape in enumerate(shapeList):
        if shape.name.upper() == shapeNameLeft.upper():
            leftHex = shape.hexString
            if shape.autoMirror:
                autoMirrorVar = True
            else:
                autoMirrorVar = False

    # Send hex to Picoh.

    if leftHex == '':
        print(str(shapeNameLeft) + " Eyeshape Not Found")
        return
    if connected:
        _setEyes(rightHex, leftHex, autoMirrorVar)
        wait(0.05)
        move(EYETILT, motorPos[EYETILT])
        move(EYETURN, motorPos[EYETURN])


def getPhrase(set='None', variable='None'):
    global phraseList
    possiblePhrases = []
    for phrase in phraseList:
        if str(set) == str(phrase.set) or set == 'None':
            if str(variable) == phrase.variable or variable == 'None':
                possiblePhrases.append(phrase.text)
    length = len(possiblePhrases)
    if length == 0:
        print(
                "No matching phrase found for set: " + str(set) + " variable: " + str(variable) + " in: " + speechFile)
        return ""
    elif length == 1:
        return possiblePhrases[0]
    else:
        return possiblePhrases[random.randint(0, length - 1)]

# Function to play sounds located in the picohData/Sounds/ folder.
def playSound(name="", untilDone=True):
    if not name:
        return

    # Set up a thread to play the sound.
    soundThread = threading.Thread(target=_playSoundThread, args=(name,))

    # Start the thread.
    soundThread.start()

    # If untilDone is True join the main thread to soundThread.
    if untilDone:
        soundThread.join()

def _playSoundThread(name=""):
    if not name:
        return

    name = name + ".wav"
    soundFile = os.path.join(soundFolder, name)

    # play the sound on Windows
    if platform.system() == "Windows":
        winsound.PlaySound(soundFile, winsound.SND_FILENAME)

    # play the sound on Mac
    if platform.system() == "Darwin":
        playsound(soundFile)

    # play the sound on Linux
    if platform.system() == "Linux":
        os.system('aplay ' + soundFile)
