# Datei: ASR.py
import openai


class ASR:
    def __init__(self, api_key):
        openai.api_key = api_key

    def transcribe(self, audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file,  language="de")
            print(transcript)
        transcription = transcript['text']
        return transcription
