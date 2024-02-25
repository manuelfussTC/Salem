import json
from python.OpenAIHelper import OpenAIHelper
from python.CommandParser import CommandParser
from python.FileSearcher import FileSearcher
import time
from pathlib import Path
from python.asr import ASR
from python.elevenlabstts import ElevenLabsTTS  # Änderung hier
from python.recorder import Recorder


# Importiere TextInputHandler, wenn du es in deinem Kontext benötigst

def main():
    # Lade Konfigurationsdatei
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)
    api_key = config.get('openai_api_key')
    root_path = config.get('root_path')
    elevenlabs_api_key = config.get('elevenlabs_api_key')

    # Initialisiere Helper mit API-Key
    helper = OpenAIHelper(api_key)

    # Erstelle oder hole existierenden Assistant
    assistant = helper.ensure_assistant_exists()

    # Erstelle einen neuen Thread (oder lade einen bestehenden, falls deine Logik dies unterstützt)
    thread_response = helper.create_empty_thread()
    thread_id = thread_response.get('id')

    filesearcher = FileSearcher()
    initialCodeCollection = filesearcher.mergeAllFileContentWithPath()
    initialCodeCollectionPrompt = ("your name is Max. this are the files, the paths and their content in the website "
                                   "folder you monitor and manage. this website is hosted on a MacOS system in the "
                                   f"folder '{root_path}'. When there is a question regarding "
                                   "my website, always look here for the answer:"
                                   "'''\n" + initialCodeCollection + "\n'''")

    helper.create_thread_message(thread_id, "user", initialCodeCollectionPrompt)
    initialCodingPrompt = (f"Always, when there is a read instruction or a get or find instruction, skip the "
                           f"following. Always when there is styling affected, add styling within the style.css file. "
                           f"Always when there is javascript or js affected, add styling within the sript.js file. "
                           f"Always when I ask for a concrete change on my website, this includes change or add or "
                           f"remove or delete, write the shell code snippet directly into the response."
                           f"You work on a webserver in the project root. The root "
                           f"folder of the website is always 'website' within the project root so you have all rights "
                           f"to manipulate the files within the website folder. Always prefer awk over sed and grep "
                           f"over awk. ")
    helper.create_thread_message(thread_id, "user", initialCodingPrompt)

    # Erstelle einen Run mit dem Assistant und dem Thread
    run = helper.create_run(thread_id, assistant.id)

    recorder = Recorder()
    asr = ASR(api_key)
    tts = ElevenLabsTTS(elevenlabs_api_key)

    # Hier würde deine Interaktionsschleife oder weitere Logik folgen, die den Assistant, den Thread und den Run verwendet
    while True:
        recorder.record('audio.wav')
        transcription = asr.transcribe('audio.wav')
        input_text = transcription
        if input_text.lower() == 'exit':
            print("Programm wird beendet.")

            # Hole alle Nachrichten des Threads
            messages = helper.list_thread_messages(thread_id)

            # Erstelle den Ordner 'messages', falls er noch nicht existiert
            Path("messages").mkdir(parents=True, exist_ok=True)

            # Generiere einen Dateinamen mit dem aktuellen Timestamp
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"messages/messages_list_{timestamp}.json"

            # Speichere die Nachrichtenliste in der Datei
            with open(filename, 'w', encoding='utf-8') as file:
                # Verwende repr() für jede Nachricht in der Liste und schreibe jede Nachricht in eine neue Zeile
                for message in messages:
                    file.write(repr(message) + "\n")

            print(f"Nachrichten wurden in '{filename}' gespeichert.")
            break

        command_parser = CommandParser()

        command = command_parser.handle_generic_request(input_text, thread_id, run.id, assistant.id)

        tts.synthesize(command)
        # Hier würde die Logik zur Verarbeitung der Anweisung folgen
        print(command)


if __name__ == "__main__":
    main()
