import os
import fnmatch
import openai
from python.OpenAIGenerator import OpenAIGenerator

class FileSearcher:
    def __init__(self, openai_generator, root_path='website'):
        self.openai_generator = openai_generator
        self.root_path = root_path

    def search_by_file_type(self, search_prompt):
        """
        Sucht nach allen Dateien im root und Unterordnern des Website-Ordners mit dem angegebenen Dateityp.
        """
        # Hier wird angenommen, dass der Text das Dateiformat enthält
        prompt_to_get_filetype = f"extract the file type from the text to search for files of that type\n\n{search_prompt}"
        file_type = self.openai_generator.generate_text(prompt_to_get_filetype, model="gpt-3.5-turbo")
        print('File type:', file_type)
        pattern = f'*.{file_type}'
        result = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    result.append(os.path.join(root, file))
        return result

    def merge_and_search_content(self, search_prompt):
        """
        Merget alle Dateien im root und in Unterordnern des Website-Ordners,
        und gibt den zusammengeführten Inhalt zusammen mit dem Such-Prompt an GPT weiter.
        """
        merged_content = ""
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    merged_content += f"\n\n---\n{file_path}\n---\n\n{content}"

        # Hier wird der zusammengeführte Inhalt an GPT übergeben.
        # Dies erfordert einen gültigen API-Schlüssel und eine Anpassung an deine spezifischen Anforderungen.
        response = self.openai_generator.generate_text(merged_content, model="gpt-3.5-turbo")
        return response
