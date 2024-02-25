import json
import os
import subprocess
from datetime import datetime
from openai import OpenAI
from python.OpenAIHelper import OpenAIHelper
import time  # Für die Wartezeit zwischen den Statusabfragen
import re
from subprocess import call
import shutil


class OpenAIGenerator:
    BASE_URL = 'https://api.openai.com/v1/'
    MODEL_1 = 'gpt-4-1106-preview'  # Special GPT-4 model
    MODEL_2 = 'gpt-4'  # Standard GPT-4 model
    MODEL_3 = 'gpt-3.5-turbo-16k'  # GPT-3.5-Turbo model
    FALLBACK_MODEL = 'gpt-4'  # Fallback-Modell, wenn die ursprüngliche Anfrage fehlschlägt

    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            self.api_key = config.get('openai_api_key')
            if not self.api_key:
                raise ValueError("API key not found in config.")
            self.helper = OpenAIHelper(self.api_key)
        except Exception as e:
            raise Exception('Failed to initialize OpenAIGenerator: {e}')

        self.client = OpenAI(api_key=self.api_key)
        # self.helper.delete_all_assistants()

    def execute_and_move_shell_script(self, script_path, thread_id):

        if os.path.exists(script_path):
            print(f"Executing shell script: {script_path}")
            subprocess.call(["sh", script_path])

            executed_directory = "shellscripts/executed"
            os.makedirs(executed_directory, exist_ok=True)
            shutil.move(script_path, executed_directory)

            success_prompt = f"Executed and moved the shell script to: {executed_directory}"
            print(success_prompt)
            self.helper.create_thread_message(thread_id, "user", success_prompt)
            return success_prompt, True  # Rückgabe eines Tuples mit success_prompt und True
        else:
            print(f"Shell script not found: {script_path}")
            return f"Shell script not found: {script_path}", False

    def write_shell_command_to_file(self, shell_command, thread_id):
        # Extract all commands between ```bash and ```
        bash_command_pattern = r"```(bash|shell)(.*?)```"
        bash_commands = re.findall(bash_command_pattern, shell_command, re.DOTALL)

        for bash_command_tuple in bash_commands:
            # Select the command text from the tuple, which is the second group
            bash_command_content = bash_command_tuple[1].strip()

            # Create the filename with the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directory = "shellscripts"
            filename = f"{directory}/script_{timestamp}.sh"

            # Ensure the directory exists
            os.makedirs(directory, exist_ok=True)

            # Write the Bash command to the file
            with open(filename, "w") as file:
                file.write(bash_command_content)

            success_prompt = f"Shell command written to file: {filename}"
            print('success_prompt: ', success_prompt)

            # Create a thread message and execute the script
            self.helper.create_thread_message(thread_id, "user", success_prompt)
            self.execute_and_move_shell_script(filename, thread_id)
        return True

    def generate_text(self, prompt, thread_id=None, run_id=None, assistant_id=None, model_version="gpt-4-1106-preview",
                      max_tokens=4000):
        # print('model_version: ', model_version)
        if model_version not in [self.MODEL_1, self.MODEL_2, self.MODEL_3]:
            return "Invalid model version specified."
        else:
            extended_prompt = (f"when you are instructed to change anything on the website, always return a shell code "
                               f"snippet. here is the prompt: {prompt}")
            # Für GPT-4 Modelle, nutze die Thread-Logik
            response = self._make_request_gpt_4(extended_prompt, thread_id, run_id, assistant_id)

        return response

    def buildAnswerWithGPT4(self, prompt, latest_message):
        final_prompt = (f"this was my prompt: {prompt} and this the assistants answer: {latest_message}. Generate "
                        f"a very short answer,  very high level, from the point of view "
                        f"of the assistant like a summary of the original answer but with necessary information, "
                        f"from the assistant.")
        completion = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "user", "content": final_prompt}
            ]
        )
        return completion.choices[0].message.content

    def _make_request_gpt_4(self, prompt, thread_id=None, run_id=None, assistant_id=None):

        current_old_run = self.helper.retrieve_run(thread_id, run_id)

        # Warte, bis der Run-Status auf "completed" gesetzt ist
        while current_old_run.status != 'completed':
            time.sleep(1)  # Warte eine Sekunde vor der nächsten Statusabfrage

        self.helper.create_thread_message(thread_id, "user", prompt)

        current_run = self.helper.create_run(thread_id, assistant_id)

        run_id = current_run.id

        # Warte, bis der Run-Status auf "completed" gesetzt ist
        while current_run.status != 'completed':
            time.sleep(1)  # Warte eine Sekunde vor der nächsten Statusabfrage
            current_run = self.helper.retrieve_run(thread_id, run_id)  # Aktualisiere den Run-Status

        # Hole die neueste Nachricht vom Assistant als Antwort, nachdem der Run abgeschlossen ist
        latest_message = self.helper.get_latest_message_content(thread_id)
        self.helper.create_thread_message(thread_id, "user", latest_message)
        shellWritten = self.write_shell_command_to_file(latest_message, thread_id)
        if shellWritten:
            answerToMe = self.buildAnswerWithGPT4(prompt, 'Shell command written to file and executed.')
        else:
            answerToMe = self.buildAnswerWithGPT4(prompt, latest_message)
        return answerToMe
        # self.process_latest_message(latest_message)

        # chat_history = self.helper.get_all_messages_content_as_a_chat_history(thread_id)
        # return response_text, shell_action_required
