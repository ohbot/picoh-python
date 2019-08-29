# This is a script to help control an Ohbot Robot. www.ohbot.co.uk
# Modified for use on Windows 19/2/18

import serial
import serial.tools.list_ports
import time
import threading
import os
import sys
import wave
import subprocess
from lxml import etree
import re
from playsound import playsound



# define constants for motors
HEADNOD = 0
HEADTURN = 1
EYETURN = 2
LIDBLINK = 3
TOPLIP = 4
BOTTOMLIP = 5
EYETILT = 6

# array to hold 
sensors = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

# define a module level variable for the serial port
port=""

# define library version
version ="1.0"

global voice, synthesizer, speechRate
# global to set the params to speech synthesizer which control the voice
voice = "Alex"

#global to set the speech speed. 
speechRate = 170

# Global flag to use a synthesizer other than sapi.
# If it's not sapi then it needs to support -w parameter to write to file e.g. espeak or espeak-NG
synthesizer = "say -o "


ser = None

# Function to check if a number is a digit including negative numbers
def is_digit(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False
    
# speak depending on synthesizer
def speak(text):
   
        # Remove any characters that are unsafe for a subprocess call
        safetext = re.sub(r'[^ .a-zA-Z0-9?\']+', '', text)

        bashcommand = synthesizer + 'ohbotspeech.wav --file-format=RF64 --data-format=LEI16@22050 -r' + str(speechRate) + ' -v ' + voice + ' "' + safetext + '"'  

        # Execute bash command.
        ret = subprocess.Popen(bashcommand,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

        #for line in ret.stdout.readlines():
            #print (line)
            
        retval = ret.wait()
        #print(retval)
        
def init(portName):
    # pickup global instances of port, ser and sapi variables   
    global port,ser,sapivoice,sapistream
    
    dir = os.path.dirname(os.path.abspath(__file__))
    silenceFile = os.path.join(dir, 'Silence1.wav')
    
    playsound(silenceFile)
    # Search for the Ohbot serial port 
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        
        # If port has Ohbot connected save the location
        if portName in p[1]:
            port = p[0]
            print ("Ohbot found on port:" + port)
        elif portName in p[0]:
            port = p[0]
            print ("Ohbot found on port:" + port)

    # If not found then try the first port
    if port == "":
        for p in ports:
            port = p[0]
            print ("Ohbot probably found on port:" + port)
            break
            
    if port == "":
        print ("Ohbot port " + portName + " not found")
        return False

    # Open the serial port
    ser = serial.Serial(port, 19200)

    # Set read timeout and write timeouts to blocking
    ser.timeout = None
    ser.write_timeout = None

    # Make an initial call to Festival without playing the sound to check it's all okay
    text = "Hi"
        
    # Create a bash command with the desired text. The command writes two files, a .wav with the speech audio and a .txt file containing the phonemes and the times.
    speak (text)

    return True

# Startup Code
# xml file for motor definitions
dir = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(dir, 'MotorDefinitionsv21.omd')
tree = etree.parse(file)
root = tree.getroot()

# Put motor ranges into lists
motorPos = [11,11,11,11,11,11,11,11]
motorMins = [0,0,0,0,0,0,0,0]
motorMaxs = [0,0,0,0,0,0,0,0]
motorRev = [False,False,False,False,False,False,False,False]
restPos = [0,0,0,0,0,0,0,0]
isAttached = [False,False,False,False,False,False,False,False]

# For each line in motor defs file
for child in root:
    indexStr = child.get("Motor")
    index = int(indexStr)
    motorMins[index] = int(int(child.get("Min"))/1000*180)
    motorMaxs[index] = int(int(child.get("Max"))/1000*180)
    motorPos[index] = int(child.get("RestPosition"))
    restPos[index] = int(child.get("RestPosition"))

    if child.get("Reverse") == "True":
        rev = True
        motorRev[index] = rev
    else:
        rev = False
        motorRev[index] = rev
        
# initialise with any port that has USB Serial Device in the name
init("usbmodem")

# Function to move Ohbot's motors. Arguments | m (motor) → int (0-6) | pos (position) → int (0-10) | spd (speed) → int (0-10) **eg move(4,3,9) or move(0,9,3)**
def move(m, pos, spd=3):
    
    # Limit values to keep then within range
    pos = limit(pos)
    spd = limit(spd)

    # Reverse the motor if necessary   
    if motorRev[m]:
        pos = 10 - pos

    # Attach motor       
    attach(m)
    
    # Ensure the lips do not crash into each other. 
    if m == TOPLIP and pos + motorPos[BOTTOMLIP] > 10:
        pos = 10 - motorPos[BOTTOMLIP]

    if m == BOTTOMLIP and pos + motorPos[TOPLIP] > 10:
        pos = 10 - motorPos[TOPLIP]
        
    # Convert position (0-10) to a motor position in degrees
    absPos = int(getPos(m,pos))

    # Scale range of speed
    spd = (250/10)*spd

    # Construct message from values
    msg = "m0"+str(m)+","+str(absPos)+","+str(spd)+"\n"

    # Write message to serial port
    serwrite(msg)

    # Update motor positions list
    motorPos[m] = pos  
 
# Function to write to serial port
def serwrite(s):
    ser.write(s.encode('latin-1')) 
    

# Function to attach Ohbot's motors. Argument | m (motor) int (0-6)
def attach(m):
    if isAttached[m] == False:
        # Construct message
        msg = "a0"+str(m)+"\n"

        # Write message to serial port
        serwrite(msg)

        # Update flag
        isAttached[m] = True
    

# Function to detach Ohbot's motors.  Argument | m (motor) int (0-6)
def detach(m):
    msg = "d0"+str(m)+"\n"    
    serwrite(msg)
    isAttached[m] = False
    
# Function to find the scaled position of a given motor. Arguments | m (motor) → int (0-6) | pos (position) → int (0-10) | Returns a position
def getPos(m, pos):
    mRange = motorMaxs[m]-motorMins[m]
    scaledPos = (mRange/10)*pos
    return scaledPos + motorMins[m]

# Function to set the voice used by the synthesiser
# name - run 'say -v ?' in terminal to find available names.
# speed - speech rate in words per min.
# This override will stay in use until it's next called
def setVoice(name = voice):
    global voice
    voice = name
    
    
# Function to set a different speech synthesizer - defaults to sapi
def setSynthesizer(params):
    global synthesizer
    synthesizer = params
    
# Set the speed of the speech in words per min.
def speechSpeed(params):
    global speechRate
    speechRate = params

# Function to make Ohbot Speak. Arguments | text String "Hello World" **eg say("Hello my name is Ohbot") or
# untilDone - wait in function until speech is complete, lipSync - move lips in time with speech, hdmiAudio - adds a delay to give hdmi channel time to activate.
# soundDelay - positive if lip movement is lagging behind sound, negative if sound is lagging behind lip movement.
def say(text, untilDone = True, lipSync=True, hdmiAudio = False, soundDelay = 0):

    if hdmiAudio:
        soundDelay = soundDelay - 1

    # Create a bash command with the desired text. espeak.exe or another synthesizer must be in the current folder.  the -w parameter forces the speech to a file
    speak (text)
    
    # open the file to calculate visemes. Festival on RPi has this built in but for espeak need to do it manually
    waveFile = wave.open('ohbotspeech.wav', 'r')

    length = waveFile.getnframes()
    framerate = waveFile.getframerate()
    channels = waveFile.getnchannels()
    bytespersample = waveFile.getsampwidth()

    # How many samples per second for mouth position
    VISEMESPERSEC = 10

    # How many samples in 1/20th second
    # print ('framerate:', framerate, ' channels:', channels, ' length:', length, ' bytespersample:', bytespersample)

    chunk = int(waveFile.getframerate() / VISEMESPERSEC)
    # print ('chunk:', chunk)

    # Empty the lists that contain phoneme data and reset count
    phonemes = []
    times = []

    ms = 0

    for i in range (0, length - chunk, chunk):
        vol = 0
        buffer = waveFile.readframes(chunk)
        # frame is 1 sample for mono or 2 for stereo
        bytesread = chunk * channels * bytespersample
        # print ('bytesread:', bytesread)
        index = 0;
        for sample in range (0, int(bytesread / (channels * bytespersample))):
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
    for i in range (0, len(phonemes)-1):
        if (phonemes[i] > max):
            max = phonemes[i]

    for i in range (0, len(phonemes)-1):
        phonemes[i] = phonemes[i] * 10 / max
        # print ('visnorm', i, ":", times[i], ':', phonemes[i])
    
    if lipSync:
        if soundDelay > 0:
            # Set up a thread for the speech sound synthesis, delay start by soundDelay
            t = threading.Timer(soundDelay, saySpeech, args=(hdmiAudio,), kwargs=None)
            # Set up a thread for the speech movement
            t2 = threading.Thread(target=moveSpeech, args=(phonemes,times))
        else:
            # Set up a thread for the speech sound synthesis
            t = threading.Thread(target=saySpeech, args=(hdmiAudio,))
            # Set up a thread for the speech movement, delay start by - soundDelay
            t2 = threading.Timer(-soundDelay, moveSpeech, args=(phonemes,times), kwargs=None)
        t2.start() 
    else:
        # Set up a thread for the speech sound synthesis
        t = threading.Thread(target=saySpeech, args=(hdmiAudio,))      
    t.start()

    # if untilDone, keep running until speech has finished    
    if untilDone:
        totalTime = times[len(times)-1]
        startTime = time.time()
        while time.time()-startTime < totalTime:
            continue
        
# Function to limit values so they are between 0 - 10
def limit(val):
     if val > 10:
       return 10
     elif val < 0: 
        return 0
     else:
        return val

# Function to play back the speech wav file, if hmdi audio is being used play silence before speech sound
def saySpeech(addSilence):
    
    if addSilence:            
        dir = os.path.dirname(os.path.abspath(__file__))
        silenceFile = os.path.join(dir, 'Silence1.wav')       
        playsound(silenceFile)
        
    playsound('ohbotspeech.wav')
   
# Function to move Ohbot's lips in time with speech. Arguments | phonemes → list of phonemes[] | waits → list of waits[]
def moveSpeech(phonemes, times):
    startTime = time.time()
    timeNow = 0
    totalTime = times[len(times)-1]
    currentX = -1
    while timeNow < totalTime:     
        timeNow = time.time() - startTime
        for x in range (0,len(times)):
            if timeNow > times[x] and x > currentX:                
                posTop = phonememapTop(phonemes[x])
                posBottom = phonememapBottom(phonemes[x])
                move(TOPLIP,posTop,10)
                move(BOTTOMLIP,posBottom,10)
                currentX = x
    move(TOPLIP,5)
    move(BOTTOMLIP,5)
            
# Function mapping phonemes to top lip positions.
def phonememapTop(val):
    return 5 + val / 2;

# Function mapping phonemes to top lip positions.
# Bottom lip is 2/3 the movement of top lip
def phonememapBottom(val):
    return 5 + val / 3;
        
# Function to set the color of the LEDs in Ohbot's eyes.Arguments | r (red) → int (0-10) | g (green) → int (0-10) | b (blue) → int (0-10) 
# swapRandG is used to swap the red and green values on older Ohbots
def eyeColour(r, g, b, swapRandG = False):

    # Limit the values to keep them within range.
    r = limit(r)
    g = limit(g)
    b = limit(b)

    # Scale the values so they are between 0 - 255.
    r = int((255/10)*r)

    g = int((255/10)*g)

    b = int((255/10)*b)

    # Construct a message with the values.
    if swapRandG:
        msg1 = "l00,"+str(g)+","+str(r)+","+str(b)+"\n"
        msg2 = "l01,"+str(g)+","+str(r)+","+str(b)+"\n"
    else:       
        msg1 = "l00,"+str(r)+","+str(g)+","+str(b)+"\n"
        msg2 = "l01,"+str(r)+","+str(g)+","+str(b)+"\n"

    # Write message to serial port.
    serwrite(msg1)    
    serwrite(msg2)    

def wait(seconds):
    time.sleep(float(seconds))
    return

def close():       
    for x in range(0, len(motorMins)-1):
        detach(x)   

# Reset Ohbot back to start position
def reset():
    eyeColour(0,0,0)
    for x in range(0,len(restPos)-1):
        move(x,restPos[x])

# Return the sensor value between 0-10 for a given sensor number. Values stored in sensors[] array.
def readSensor(index):
    ser.flushInput()
    
    msg = "i0"+str(index)+"\n"
    serwrite(msg)

    line = ser.readline()
    lineStr = line.decode("utf-8")
    lines = lineStr.split(",")

    if len(lines) > 1:

        indexIn = lines[0]
        indexIn = indexIn[1]

        intdex = int(indexIn)
        
        newVal = int(lines[1])/1024
        newVal = newVal *10
        sensors[intdex] = limit(newVal)

    return sensors[index]
 
 


