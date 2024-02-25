import os


class FileSearcher:
    def __init__(self, root_path='website'):
        self.root_path = root_path

    def mergeAllFileContentWithPath(self):
        """
        Merges all files in the root and subfolders of the website folder
        """
        merged_content = ""
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    merged_content += f"\n\n---\n{file_path}\n---\n\n{content}"
        return merged_content
