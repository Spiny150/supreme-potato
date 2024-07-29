import pvporcupine
import sounddevice as sd
import numpy as np
import pyaudio
import struct
from pvrecorder import PvRecorder
import threading
import deepgramtest


# Remplacez par votre clé d'accès Porcupine
access_key = 'wsARPJnOFkfbWHFjHtoqJPcxzolCUncG07m0cM83qI05jX40PKVMWg=='

# Créez l'instance de Porcupine
porcupine = pvporcupine.create(
    access_key=access_key,
    #keywords=['alexa'],
    keyword_paths=['ok-echo_fr_linux_v3_0_0.ppn'],
    model_path='porcupine_params_fr.pv'
)

# Configuration de l'audio
SAMPLERATE = porcupine.sample_rate
FRAMES_PER_BUFFER = porcupine.frame_length

def get_next_audio_frame():
    """Capture les trames audio en temps réel."""
    audio_data = sd.rec(FRAMES_PER_BUFFER, samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()  # Attendre que l'enregistrement soit terminé
    return np.squeeze(audio_data)



try:
    
    # pa = pyaudio.PyAudio()

    # audio_stream = pa.open(
    #                 rate=porcupine.sample_rate,
    #                 channels=1,
    #                 format=pyaudio.paInt16,
    #                 input=True,
    #                 frames_per_buffer=porcupine.frame_length,
    #                 )
    recorder = PvRecorder(porcupine.frame_length)
    recorder.start()
    print("Listening for wake words...")

    while True:
        # audio_frame = audio_stream.read(porcupine.frame_length)
        # #print(audio_frame)
        # audio_frame = struct.unpack_from("h" * porcupine.frame_length, audio_frame)
        
        audio_frame = recorder.read()
        
        keyword_index = porcupine.process(audio_frame)
        #print(keyword_index)
        if keyword_index == 0:
            deepgramtest.conv()
            print("Listening for wake words...")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    porcupine.delete()
