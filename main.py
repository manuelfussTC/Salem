import json
from python.OpenAIHelper import OpenAIHelper
from python.TextInputHandler import TextInputHandler


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
    get_latest_message = helper.get_latest_message_content(thread_id)

    # Hier würde deine Interaktionsschleife oder weitere Logik folgen, die den Assistant, den Thread und den Run verwendet
    while True:
        input_text = input("Bitte geben Sie Ihre Anweisung ein oder tippen Sie 'exit', um das Programm zu beenden: ")
        if input_text.lower() == 'exit':
            print("Programm wird beendet.")
            break

        text_handler = TextInputHandler()

        text_handler.handle_input(input_text, thread_id, run.id, assistant.id)

        # Hier würde die Logik zur Verarbeitung der Anweisung folgen


if __name__ == "__main__":
    main()
