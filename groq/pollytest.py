import boto3
import os
import sounddevice as sd
import soundfile as sf
import subprocess

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()

# Initialiser le client Polly
client = boto3.client('polly')


def ReadText(text):

    # Synthétiser le discours
    response = client.synthesize_speech(
        Engine='neural',
        LanguageCode='fr-FR',
        OutputFormat='mp3',
        SampleRate='24000',
        Text=text,
        TextType='text',
        VoiceId='Remi'
    )

    # Sauvegarder le fichier MP3
    with open("output.mp3", "wb") as file:
        file.write(response['AudioStream'].read())

    play_mp3("output.mp3")


    # Nettoyer les fichiers audio temporaires
    os.remove("output.mp3")