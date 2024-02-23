import requests
import json

class OpenAIGenerator:
    BASE_URL = 'https://api.openai.com/v1/'
    MODEL_1 = 'gpt-4-1106-preview'  # Special model
    MODEL_2 = 'gpt-4'  # Standard model

    def __init__(self, config_path):
        try:
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            self.api_key = config.get('openai_api_key')
            if not self.api_key:
                raise ValueError("API key not found in config.")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAIGenerator: {e}")

    def generate_text(self, prompt, max_tokens=4000):
        # Try the first model
        response = self._make_request('completions', prompt, self.MODEL_1, max_tokens)
        if self._is_response_valid(response):
            return response['choices'][0]['text'].strip()

        # If the first model fails, try the second model
        response = self._make_request('completions', prompt, self.MODEL_2, max_tokens)
        if self._is_response_valid(response):
            return response['choices'][0]['text'].strip()

        return "Failed to generate text."

    def _make_request(self, endpoint, prompt, model, max_tokens):
        url = self.BASE_URL + endpoint
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = json.dumps({
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens
        })

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP request failed with status code {response.status_code}"}

    def _is_response_valid(self, response):
        if not response.get('choices') or not response['choices'][0].get('text'):
            return False
        return True

