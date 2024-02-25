# Datei: asr.py
from openai import OpenAI


class ASR:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcript = self.client.audio.transcriptions.create(model="whisper-1",
                                                                 file=audio_file, language="en")
            # print(transcript)
        transcription = transcript.text
        return transcription
