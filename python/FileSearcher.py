import json
import os
import fnmatch


class FileSearcher:
    def __init__(self, openai_generator, root_path='website'):
        self.openai_generator = openai_generator
        self.root_path = root_path

    def search_by_file_type(self, search_prompt, thread_id=None, run_id=None, assistant_id=None):
        """
        Sucht nach allen Dateien im root und Unterordnern des Website-Ordners mit dem angegebenen Dateityp.
        """
        # Hier wird angenommen, dass der Text das Dateiformat enthält
        prompt_to_get_filetype = f"Given the text '{search_prompt}', identify the file type mentioned and format the response as JSON. For example, if the file type is 'html', respond with: {{\"file_type\": \"html\"}}."


        file_type = self.openai_generator.generate_text(prompt_to_get_filetype, model_version="gpt-3.5-turbo-16k")
        # Konvertiere den JSON-String in ein Python-Diktat


        # find all files with the given file type
        matches = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if fnmatch.fnmatch(file, f'*.{file_type}'):
                    matches.append(os.path.join(root, file))
        # now generate the answer from gpt-4 to the question in the search_prompt together with the final matches
        final_prompt_for_openai = f"Tell me in a short and informal way, high level, no technical talk, the result of the search for '{search_prompt}' and the files found: {matches}"
        final_answer = self.openai_generator.generate_text(final_prompt_for_openai, thread_id=thread_id, run_id=run_id, assistant_id=assistant_id)
        return True

    # @TODO: Implement the merge_and_search_content method and return a final answer from GPT-4-1106-preview
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
        response = self.openai_generator.generate_text(merged_content, model="gpt-3.5-turbo-16k")
        return response
