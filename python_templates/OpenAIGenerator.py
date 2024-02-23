import openai
import json

class OpenAIGenerator:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.api_key = config['openai_api_key']
        openai.api_key = self.api_key

    def generate_text(self, prompt, max_tokens=4000, model="gpt-4"):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()

    def tag_image(self, base64_image, prompt, model="gpt-4-vision-preview"):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            attachments=[
                {
                    "data": base64_image,
                    "type": "image"
                }
            ],
            max_tokens=300
        )
        return response.choices[0].text.strip()
