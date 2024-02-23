from python.FileSearcher import FileSearcher
from python.OpenAIGenerator import OpenAIGenerator

class CommandParser:
    def __init__(self, config_path='config/config.json'):
        self.openai_generator = OpenAIGenerator(config_path)
        self.file_searcher = FileSearcher(self.openai_generator)

    def parse_command(self, text, action, obj):
        if action in ['search', 'find']:
            if obj == 'file':
                # Hier wird angenommen, dass der Text das Dateiformat enthält
                search_result = self.file_searcher.search_by_file_type(text)
                print('Search result:', search_result)
                return search_result
            elif obj == 'text':
                # Wenn nach Inhalten gesucht wird, könnten wir alle Dateien mergen
                # und die Anfrage an GPT-3.5-turbo senden, um zu klären, was genau gesucht wird
                merged_content = self.file_searcher.merge_and_search_content(text)
                print('Merged content:', merged_content)
                # Verwenden GPT-3.5-turbo Modell für schnelle Antworten
                return merged_content
        return "Action unknown or not supported."
