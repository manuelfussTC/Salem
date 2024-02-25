from python.FileSearcher import FileSearcher
from python.OpenAIGenerator import OpenAIGenerator

class CommandParser:
    def __init__(self, config_path='config/config.json'):
        self.openai_generator = OpenAIGenerator(config_path)
        self.file_searcher = FileSearcher(self.openai_generator)


    def handle_generic_request(self, text, thread_id=None, run_id=None, assistant_id=None):
        generic_response = self.openai_generator.generate_text(text, thread_id, run_id, assistant_id)
        return generic_response
