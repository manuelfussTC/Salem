from python.CommandParser import CommandParser

class TextInputHandler:
    def __init__(self):
        self.command_parser = CommandParser()

    def handle_input(self, input_text, thread_id=None, run_id=None, assistant_id=None):
        action, obj = self.identify_action_and_object(input_text)
        # Übergibt die aktuelle Thread-ID an den CommandParser

        response = self.command_parser.parse_command(input_text, action, obj, thread_id, run_id, assistant_id)
        # Aktualisiere self.thread_id basierend auf der Antwort, falls eine neue Thread-ID zurückgegeben wird
        return response

    def identify_action_and_object(self, input_text):
        # Listen der Aktionen und Objekte
        actions = ['find', 'search', 'change', 'replace', 'create', 'write', 'add', 'delete', 'remove', 'extend', 'explain', 'tell', 'describe']
        objects = ['image', 'text', 'section', 'file']

        action = None
        obj = None

        for action_candidate in actions:
            if action_candidate in input_text:
                action = action_candidate  # Setzen des Aktionstyps als String
                break

        for object_candidate in objects:
            if object_candidate in input_text:
                obj = object_candidate  # Setzen des Objekttyps als String
                break

        return action, obj