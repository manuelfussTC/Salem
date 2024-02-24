import json
from openai import OpenAI
from python.OpenAIHelper import OpenAIHelper
import time  # Für die Wartezeit zwischen den Statusabfragen



class OpenAIGenerator:
    BASE_URL = 'https://api.openai.com/v1/'
    MODEL_1 = 'gpt-4-1106-preview'  # Special GPT-4 model
    MODEL_2 = 'gpt-4'  # Standard GPT-4 model
    MODEL_3 = 'gpt-3.5-turbo-16k'  # GPT-3.5-Turbo model
    FALLBACK_MODEL = 'gpt-4'  # Fallback-Modell, wenn die ursprüngliche Anfrage fehlschlägt

    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            self.api_key = config.get('openai_api_key')
            if not self.api_key:
                raise ValueError("API key not found in config.")
            self.helper = OpenAIHelper(self.api_key)
        except Exception as e:
            raise Exception('Failed to initialize OpenAIGenerator: {e}')

        self.client = OpenAI(api_key=self.api_key)
        # self.helper.delete_all_assistants()


    def _get_headers(self):
        """Hilfsmethode zur Generierung der Request-Header."""
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer {self.api_key}"
        }

    def generate_text(self, prompt, thread_id=None, run_id=None, assistant_id=None, model_version="gpt-4-1106-preview", max_tokens=4000):
        if model_version not in [self.MODEL_1, self.MODEL_2, self.MODEL_3]:
            return "Invalid model version specified."
        # Erstelle einen neuen Thread, wenn keine Thread-ID vorhanden ist
        # if thread_id is None:
        #     thread_response = self.helper.create_empty_thread()
        #     if thread_response and 'id' in thread_response:
        #         thread_id = thread_response.get('id')
        #     else:
        #         # Fehlerbehandlung, wenn keine Thread-ID erstellt werden konnte
        #         return "Failed to create thread or retrieve thread ID."
        # print('model version:', model_version)
        if model_version == self.MODEL_3:
            response = self._make_request_gpt_3_5(prompt, max_tokens)
        else:
            # Für GPT-4 Modelle, nutze die Thread-Logik
            response = self._make_request_gpt_4(prompt, thread_id, run_id, assistant_id)

        return response

    # def _make_request(self, prompt, model, max_tokens, thread_id=None, run_id=None):
    #     if model == self.MODEL_3:  # gpt-3.5-turbo-16k verwendet eine andere Endpunktstruktur
    #         return self._make_request_gpt_3_5(prompt, max_tokens)
    #     else:  # Für GPT-4 Modelle
    #         return self._make_request_gpt_4(prompt, thread_id, run_id)

    def _make_request_gpt_4(self, prompt, thread_id=None, run_id=None, assistant_id=None):
        # Füge die Anfrage als Nachricht zu einem existierenden Thread hinzu
        message_response = self.helper.create_thread_message(thread_id, "user", prompt)
        current_run = self.helper.create_run(thread_id, assistant_id)



        run_id = current_run.id

        # Warte, bis der Run-Status auf "completed" gesetzt ist
        while current_run.status != 'completed':
            # print("Warte auf Run-Abschluss. Aktueller Status:", current_run.status)
            time.sleep(1)  # Warte eine Sekunde vor der nächsten Statusabfrage
            current_run = self.helper.retrieve_run(thread_id, run_id)  # Aktualisiere den Run-Status

        # Hole die neueste Nachricht vom Assistant als Antwort, nachdem der Run abgeschlossen ist
        latest_message = self.helper.get_latest_message_content(thread_id)

        chat_history = self.helper.get_all_messages_content_as_a_chat_history(thread_id)
        # print('chat history:', chat_history)
        return latest_message


    def _make_request_gpt_3_5(self, prompt, max_tokens):
        try:
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )

            # Hier gehen wir davon aus, dass die Antwort mindestens eine Wahl enthält
            if completion.choices:
                return completion.choices[0].message
            else:
                return {"error": "No completion choices returned."}
        except Exception as e:
            print("An exception occurred: {e}")
            return {"error": f"An exception occurred: {e}"}

    def _is_response_valid(self, response):
        try:
            # Versuche zuerst, auf die Antwort als Dictionary zuzugreifen
            if 'choices' in response and response['choices']:
                message_content = response['choices'][0]['message']['content']
            elif response.content:
                # Überprüfe, ob 'content' existiert und die 'get'-Methode aufrufbar ist
                file_type_object = json.loads(response.content)
                file_type = file_type_object.get('file_type')
                return bool(file_type)  # Gültig, wenn 'file_type' vorhanden und nicht leer ist
            else:
                return False
        except (TypeError, AttributeError):
            # Wenn ein TypeError oder AttributeError auftritt, versuche, die Antwort als Objekt zu behandeln
            try:
                if hasattr(response, 'choices') and response.choices:
                    message_content = response.choices[0].message.content
                else:
                    return False
            except (TypeError, AttributeError):
                # Wenn erneut Fehler auftreten, ist die Antwort definitiv ungültig
                return False
        # Versuche, den 'content' zu parsen, falls er noch nicht als 'file_type' extrahiert wurde
        try:
            if 'message_content' in locals():  # Prüft, ob 'message_content' bereits definiert wurde
                content_data = json.loads(message_content)
                file_type = content_data.get('file_type')
                return bool(file_type)  # Gültig, wenn 'file_type' vorhanden und nicht leer ist
        except (ValueError, AttributeError):
            # Fange Fehler beim Parsen von JSON oder beim Zugriff auf nicht vorhandene Attribute
            return False

        # Die Antwort ist ungültig, wenn keine der obigen Bedingungen erfüllt ist
        return False

    def _extract_text(self, response, model_version):
        if model_version == self.MODEL_3:
            file_type_object = json.loads(response.content)
            file_type = file_type_object.get('file_type')
            return file_type.strip()
        else:
            return response['choices'][0]['text'].strip()
