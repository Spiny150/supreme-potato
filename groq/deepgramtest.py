DEEPGRAM_API_KEY = '4df94167314481bca1d1651ac6d504398f655efa'

import logging
from time import sleep
import groqandpolly

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)


def RepetitivStreamConcatenate(liste):
    a = ""
    for i in range(len(liste)):
        if i == 0:
            a += liste[i]
            continue
        if liste[i] == liste[i-1]:
            continue
        last5precedant = liste[i-1][-5:]
        for j in range(len(liste[i]), 4, -1):
            last5 = liste[i][j-5:j]
            if last5 == last5precedant:
                a += liste[i][j:]
                break
            if j == 5:
                a += " " + liste[i] + " "
    return a

# example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
# config = DeepgramClientOptions(
#     verbose=logging.DEBUG, options={"keepalive": "true"}
# )
# deepgram: DeepgramClient = DeepgramClient("", config)
# otherwise, use default config
deepgram: DeepgramClient = DeepgramClient("f59bd783f9b005d806f402687bcca67b178ccf5c")

dg_connection = deepgram.listen.live.v("1")

global total
total = []

# def on_open(self, open, **kwargs):
#     print(f"\n\n{open}\n\n")

def on_message(self, result, **kwargs):
    # print("-",end="")
    global total
    sentence = result.channel.alternatives[0].transcript
    if len(sentence) == 0:
        return
    total.append(sentence)
    print(f"speaker: {sentence}")

# def on_metadata(self, metadata, **kwargs):
#     print(f"\n\n{metadata}\n\n")

# def on_speech_started(self, speech_started, **kwargs):
#     print(f"\n\n{speech_startedgroqandpolly}\n\n")

def on_utterance_end(self, utterance_end, **kwargs):
    global total
    # print(f"\n\n{total}\n\n")
    a = RepetitivStreamConcatenate(total)
    print(f"\n\n{a}")
    microphone.mute()
    groqandpolly.DoLLM(a)
    microphone.unmute()
    total = []

# def on_error(self, error, **kwargs):
#     print(f"\n\n{error}\n\n")

# def on_close(self, close, **kwargs):
#     print(f"\n\n{close}\n\n")

# dg_connection.on(LiveTranscriptionEvents.Open, on_open)
dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
# dg_connection.on(LiveTranscriptionEvents.Metadata, on_metadata)
# dg_connection.on(LiveTranscriptionEvents.SpeechStarted, on_speech_started)
dg_connection.on(LiveTranscriptionEvents.UtteranceEnd, on_utterance_end)
# dg_connection.on(LiveTranscriptionEvents.Error, on_error)
# dg_connection.on(LiveTranscriptionEvents.Close, on_close)

options: LiveOptions = LiveOptions(
    model="nova-2",
    punctuate=True,
    language="fr-FR",
    encoding="linear16",
    channels=1,
    sample_rate=16000,
    # To get UtteranceEnd, the following must be set:
    interim_results=True,
    utterance_end_ms="1000",
    vad_events=True,
)
dg_connection.start(options)

# Open a microphone stream on the default input device
microphone = Microphone(dg_connection.send)

input("START ? ")
# start microphone
microphone.start()

# wait until finished
# while True:
#     print(test)
input("Press Enter to stop recording...\n\n")

# Wait for the microphone to close
microphone.finish()

# Indicate that we've finished
dg_connection.finish()

print("Finished")
# sleep(30)  # wait 30 seconds to see if there is any additional socket activity
# print("Really done!")