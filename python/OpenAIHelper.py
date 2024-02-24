import openai
from openai.types.beta.threads import MessageContentText


class OpenAIHelper:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def ensure_assistant_exists(self):
        name = "My Custom Assistant"
        instructions = "Please assist the user."
        tools = []
        model = "gpt-3.5-turbo-1106"
        new_assistant = self.create_assistant(instructions, name, tools, model)
        print("Neuer Assistent erstellt: ", new_assistant.id, "\r\n")
        return new_assistant

    def save_thread_id(self, thread_id, file_path='current_thread_id.txt'):
        """Speichert die Thread-ID in einer Datei."""
        with open(file_path, 'w') as file:
            file.write(thread_id)

    def load_thread_id(self, file_path='current_thread_id.txt'):
        """Lädt die Thread-ID aus einer Datei, falls vorhanden."""
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def save_run_id(self, run_id, file_path='current_run_id.txt'):
        """Speichert die Run-ID in einer Datei."""
        with open(file_path, 'w') as file:
            file.write(run_id)

    def load_run_id(self, file_path='current_run_id.txt'):
        """Lädt die Run-ID aus einer Datei, falls vorhanden."""
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return None

    def create_assistant(self, instructions, name, tools, model):
        my_assistant = self.client.beta.assistants.create(
            instructions=instructions,
            name=name,
            tools=[{"type": tool} for tool in tools],
            model=model,
        )
        return my_assistant

    def list_assistants(self):
        assistants = self.client.beta.assistants.list()
        return assistants.data

    def delete_all_assistants(self):
        assistants = self.list_assistants()
        for assistant in assistants:
            print(f"Deleting assistant {assistant.id}", "\r\n")
            self.client.beta.assistants.delete(assistant.id)

    def retrieve_assistant(self, assistant_id):
        my_assistant = self.client.beta.assistants.retrieve(assistant_id)
        return my_assistant

    def update_assistant(self, assistant_id, instructions, name, tools, model, file_ids=None):
        my_updated_assistant = self.client.beta.assistants.update(
            assistant_id,
            instructions=instructions,
            name=name,
            tools=[{"type": tool} for tool in tools],
            model=model,
            file_ids=file_ids or [],
        )
        return my_updated_assistant

    def create_empty_thread(self):
        response = self.client.beta.threads.create()

        # Überprüfe, ob die Antwort ein Thread-Objekt ist
        if isinstance(response, openai.types.beta.thread.Thread):
            # Extrahiere die 'id' direkt aus dem Thread-Objekt
            thread_id = response.id
            # Gebe ein Dictionary zurück, das der erwarteten Struktur entspricht
            return {'id': thread_id}
        else:
            # Falls die Antwort nicht das erwartete Format hat, logge den Fehler
            print("Die Antwort ist nicht vom erwarteten Typ 'Thread'.")
            return None

    def retrieve_thread(self, thread_id):
        my_thread = self.client.beta.threads.retrieve(thread_id)
        return my_thread

    def update_thread(self, thread_id, metadata):
        my_updated_thread = self.client.beta.threads.update(
            thread_id,
            metadata=metadata,
        )
        return my_updated_thread

    def delete_thread(self, thread_id):
        response = self.client.beta.threads.delete(thread_id)
        return response

    def create_thread_message(self, thread_id, role, content):
        # Stelle sicher, dass 'role' auf 'user' gesetzt ist, da dies der erlaubte Wert ist
        thread_message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,  # Korrigiere dies von 'system' zu 'user'
            content=content,
        )
        return thread_message

    def list_thread_messages(self, thread_id):
        thread_messages = self.client.beta.threads.messages.list(thread_id)
        return thread_messages.data

    def get_latest_message_content(self, thread_id):
        messages = self.list_thread_messages(thread_id)
        if not messages:
            return "Keine Nachrichten gefunden."

        # Die neueste Nachricht ist die letzte in der Liste
        latest_message = messages[0]

        # Überprüfe, ob die neueste Nachricht Inhalte vom Typ 'text' enthält
        if latest_message.content and isinstance(latest_message.content[0], MessageContentText):
            # Gibt den 'value' des Textinhalts der neuesten Nachricht zurück
            return latest_message.content[0].text.value
        else:
            return "Die neueste Nachricht enthält keinen Textinhalt."

    #format the message content to be a chat history with line wise messages
    def get_all_messages_content_as_a_chat_history(self, thread_id):
        messages = self.list_thread_messages(thread_id)
        chat_history = []
        for message in messages:
            if message.content and isinstance(message.content[0], MessageContentText):
                chat_history.append(message.content[0].text.value)
        return '\n'.join(chat_history)

    def retrieve_message(self, message_id, thread_id):
        message = self.client.beta.threads.messages.retrieve(
            message_id=message_id,
            thread_id=thread_id,
        )
        return message

    def update_message(self, message_id, thread_id, metadata):
        message = self.client.beta.threads.messages.update(
            message_id=message_id,
            thread_id=thread_id,
            metadata=metadata,
        )
        return message

    def create_run(self, thread_id, assistant_id, instructions=None):
        if instructions:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions=instructions
            )
        else:
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
        return run

    def create_and_run_thread(self, assistant_id, messages):
        run = self.client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={"messages": [{"role": msg["role"], "content": msg["content"]} for msg in messages]},
        )
        return run

    def retrieve_run(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run

    def update_run(self, thread_id, run_id, metadata):
        run = self.client.beta.threads.runs.update(
            thread_id=thread_id,
            run_id=run_id,
            metadata=metadata,
        )
        return run

    def submit_tool_outputs(self, thread_id, run_id, tool_outputs):
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=[{"tool_call_id": output["tool_call_id"], "output": output["output"]} for output in
                          tool_outputs],
        )
        return run

    def cancel_run(self, thread_id, run_id):
        run = self.client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id
        )
        return run

    def list_runs(self, thread_id):
        runs = self.client.beta.threads.runs.list(thread_id)
        return runs.data

    def list_run_steps(self, thread_id, run_id):
        run_steps = self.client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run_id)
        return run_steps.data

    def cancel_all_runs(self, thread_id):
        runs = self.list_runs(thread_id)
        for run in runs:
            print(f"Cancelling run {run.id}", "\r\n")
            self.cancel_run(thread_id, run.id)
