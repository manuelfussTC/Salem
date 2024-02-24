from python.FileSearcher import FileSearcher
from python.OpenAIGenerator import OpenAIGenerator
from python.FileExplainer import FileExplainer

class CommandParser:
    def __init__(self, config_path='config/config.json'):
        self.openai_generator = OpenAIGenerator(config_path)
        self.file_searcher = FileSearcher(self.openai_generator)
        self.file_explainer = FileExplainer(self.openai_generator)

    def parse_command(self, text, action, obj, thread_id=None, run_id=None, assistant_id=None):
        if action and obj:
            if action in ['search', 'find'] and obj == 'file':
                search_result = self.file_searcher.search_by_file_type(text, thread_id, run_id, assistant_id)
                return search_result
            elif action in ['explain', 'tell', 'describe'] and obj == 'file':
                explanation = self.file_explainer.explain_files(text, thread_id, run_id, assistant_id)
                return explanation
            # Erweitere hier für weitere Aktionen und Objekte
        else:
            # Verarbeite eine generische Anfrage, wenn keine spezifische Aktion oder Objekt erkannt wurde
            return self.handle_generic_request(text, thread_id, run_id, assistant_id)

    def handle_generic_request(self, text, thread_id=None, run_id=None, assistant_id=None):
        # Verarbeite die Anfrage als generischen Text, möglicherweise unter Nutzung des Thread-Kontexts
        print('Handling generic request:', text)
        generic_response = self.openai_generator.generate_text(text, thread_id, run_id, assistant_id)
        return generic_response
