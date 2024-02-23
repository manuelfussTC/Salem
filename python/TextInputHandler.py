from python.CommandParser import CommandParser

class TextInputHandler:
    def __init__(self):
        self.command_parser = CommandParser()


    def handle_input(self, input_text):
        action, obj = self.identify_action_and_object(input_text)
        print(f"Action: {action}, Object: {obj}")
        if action and obj:
            return self.command_parser.parse_command(input_text, action, obj)
        else:
            print("Sorry, I did not understand this command.")

    def identify_action_and_object(self, input_text):
        # Listen der Aktionen und Objekte
        actions = ['find', 'search', 'change', 'replace', 'create', 'write', 'add', 'delete', 'remove', 'extend']
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