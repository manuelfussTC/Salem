import os
import fnmatch


class FileExplainer:
    def __init__(self, openai_generator, root_path='website'):
        self.openai_generator = openai_generator
        self.root_path = root_path

    def explain_files(self, file_type, thread_id=None, run_id=None, assistant_id=None):
        """
        Sammelt Inhalte aller Dateien eines spezifischen Typs und sendet diese an GPT zur Analyse.
        """
        merged_content = ""
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if fnmatch.fnmatch(file, f'*.{file_type}'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        merged_content += f"\n\n---\n{file_path}\n---\n\n{content}"

        # Erstelle einen spezifischen Prompt, der den Inhalt erklärt
        prompt = f"Explain what those files actually do {file_type}-files:\n\n{merged_content}"
        print('Prompt:', prompt)

        # Verwende OpenAIGenerator, um Text basierend auf dem zusammengeführten Inhalt zu generieren
        explanation = self.openai_generator.generate_text(prompt, thread_id=thread_id, run_id=run_id, assistant_id=assistant_id)
        return explanation
