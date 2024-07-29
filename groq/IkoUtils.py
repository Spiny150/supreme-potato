import sounddevice as sd
import soundfile as sf
import librosa
import numpy as np
import silero_vad
CHANNELS = 1
SAMPLERATE = 16000
BLOCKSIZE = 160


def recordAudioForTime(duration: float) -> list:
    audioArray = []
    stream = sd.Stream(
        callback=lambda indata,outdata, frames, time, status :
            audioArray.extend(indata[:, 0]),
        channels=CHANNELS,
        samplerate=SAMPLERATE,
        blocksize=BLOCKSIZE,
        )
    stream.start()
    sd.sleep(duration)
    stream.stop()
    stream.close()
    return np.array(audioArray)



def GetAudioStream() -> tuple[sd.Stream, list]:
    audioArray = []

    stream = sd.Stream(
    callback=lambda indata,outdata, frames, time, status :
        audioArray.extend(indata[:, 0]),
    channels=CHANNELS,
    samplerate=SAMPLERATE,
    blocksize=BLOCKSIZE,
    )
    return stream, audioArray

def saveAudio(filename, audioArray) -> None:
    sf.write(filename, audioArray, SAMPLERATE)

