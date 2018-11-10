import pyaudio
import numpy as np
p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 440.0        # sine frequency, Hz, may be float
# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
               channels=1,
               rate=fs,
               output=True)
# play. May repeat with different volume values (if done interactively)
stream.write(volume*samples)
stream.stop_stream()
stream.close()
p.terminate()

'''
Install it using pip: 
pip install pyaudio 
Notes:
pip will download the PyAudio source and build it for your system. Be sure to install the portaudio library development package (
portaudio19-dev) and the python development package (python-all-dev) beforehand.

andere Variante 
sudo apt-get install python-pyaudio python3-pyaudio

https://forum-raspberrypi.de/forum/thread/32391-sinuswelle-ueber-die-klinke-ausgeben/?pageNo=1#codeLine_3_b3b499
'''
