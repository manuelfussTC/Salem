from elevenlabs import generate, play


class ElevenLabsTTS:
    def __init__(self, api_key=None):
        if api_key:
            from elevenlabs import set_api_key
            set_api_key(api_key)

    def synthesize(self, text):
        audio = generate(
            text=text,
            voice="Chris",
            model="eleven_multilingual_v2",
        )
        play(audio)  # Übergeben des use_ffmpeg Parameters an die


