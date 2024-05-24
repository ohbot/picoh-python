# This is sample code to move Picoh's lips in time with speech
# It needs a loopback audio device to do this
# It also needs to use the modified library pyaudiowpatch 
from picoh import picoh
# pip install pyaudiowpatch to install this
import pyaudiowpatch as pyaudio
# pip install numpy to install this
import numpy as np

# Constants
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio

# Function to get RMS value
def get_rms(audio_data):
    # Convert audio data to numpy array
    samples = np.frombuffer(audio_data, dtype=np.int16)
    # Calculate RMS
    rms = np.sqrt(np.mean(samples**2))
    return rms

# Initialize PyAudio.  Using with will dispose of pyaudio on finish
with pyaudio.PyAudio() as p:
    device_index = -1
    sample_rate = -1
    device_name = ""

    print ("Loopback Devices:\r")

    # This will take the last loopback device in the list
    # so you may need to change this if you have more than one
    # loopback audio device
    for loopback in p.get_loopback_device_info_generator():
        print(f"{loopback}\r")
        device_index = loopback.get('index')
        sample_rate = (int)(loopback.get('defaultSampleRate'))
        device_name = loopback.get('name')

    if (device_index < 0):
        print ("Sorry, no loopback device was found")
        p.terminate()
        exit()
        
    print (f"Moving lips in time with device {device_name}\r")
        
    # Open audio stream
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

    print("Monitoring audio... press ctrl C to stop")

    try:
        while True:
            # Read a chunk of data from the stream
            data = stream.read(CHUNK)
            # Get the RMS value
            rms = get_rms(data)
            # Print the audio level.  Uncomment this to see the audio levels
            # print(f"Audio Level: {rms:.2f}")
            # Move Picoh's lips.  You may need to adjust this if the lips
            # are moving too much or too little
            if (not np.isnan(rms)):
                picoh.move(picoh.BOTTOMLIP, 5 + int(rms / 15))

    except KeyboardInterrupt:
        print("Stopped monitoring")

    # Close the stream and clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
