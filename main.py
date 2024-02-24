import json
from python.OpenAIHelper import OpenAIHelper
from python.CommandParser import CommandParser
import time
from pathlib import Path



# Importiere TextInputHandler, wenn du es in deinem Kontext benötigst

def main():
    # Lade Konfigurationsdatei
    with open('config/config.json', 'r') as config_file:
        config = json.load(config_file)
    api_key = config.get('openai_api_key')

    # Initialisiere Helper mit API-Key
    helper = OpenAIHelper(api_key)

    # Erstelle oder hole existierenden Assistant
    assistant = helper.ensure_assistant_exists()

    # Erstelle einen neuen Thread (oder lade einen bestehenden, falls deine Logik dies unterstützt)
    thread_response = helper.create_empty_thread()
    thread_id = thread_response.get('id')

    # Erstelle einen Run mit dem Assistant und dem Thread
    run = helper.create_run(thread_id, assistant.id)

    # Hier würde deine Interaktionsschleife oder weitere Logik folgen, die den Assistant, den Thread und den Run verwendet
    while True:
        input_text = input("Bitte geben Sie Ihre Anweisung ein oder tippen Sie 'exit', um das Programm zu beenden: ")
        if input_text.lower() == 'exit':
            print("Programm wird beendet.")

            # Hole alle Nachrichten des Threads
            messages = helper.list_thread_messages(thread_id)
            print(messages)

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

        # Hier würde die Logik zur Verarbeitung der Anweisung folgen
        print(command)


if __name__ == "__main__":
    main()
