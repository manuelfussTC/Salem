#!/bin/bash

# Definiere Verzeichnisse
root_dir="./Salem"
python_dir="$root_dir/python"
php_dir="$root_dir/php"
config_dir="$root_dir/config"
media_dir="$root_dir/Website/Medien"

# Erstelle Verzeichnisse
mkdir -p "$python_dir" "$php_dir" "$config_dir" "$media_dir"

# Python-Klasse für ElevenLabs API
cat << EOF > "$python_dir/ElevenLabsTTS.py"
from elevenlabs import generate, play

class ElevenLabsTTS:
    def __init__(self, api_key=None):
        if api_key:
            from elevenlabs import set_api_key
            set_api_key(api_key)

    def synthesize(self, text):
        audio = generate(
            text=text,
            voice="Sasha",
            model="eleven_multilingual_v2",
        )
        play(audio)  # Übergeben des use_ffmpeg Parameters an die
EOF

# PHP-Klasse für OpenAI Anfragen
cat << EOF > "$php_dir/OpenAIGenerator.php"
<?php
set_time_limit(120); // Setzt die maximale Ausführungszeit auf 120 Sekunden

class OpenAIGenerator
{
    private string \$api_key;
    private const BASE_URL = 'https://api.openai.com/v1/';
    private string \$model_1 = "gpt-4-1106-preview"; // Spezielles Modell
    private string \$model_2 = "gpt-4"; // Standardmodell

    public function __construct(string \$configPath)
    {
        if (file_exists(\$configPath)) {
            \$configContents = file_get_contents(\$configPath);
            \$config = json_decode(\$configContents, true);
            if (json_last_error() === JSON_ERROR_NONE) {
                if (isset(\$config['openai_api_key'])) {
                    \$this->api_key = \$config['openai_api_key'];
                } else {
                    throw new Exception("API key not found in config.");
                }
            } else {
                throw new Exception("Error decoding JSON from config.");
            }
        } else {
            throw new Exception("Config file not found.");
        }
    }
    // Die Klasse wird hier weiter fortgesetzt...
}
EOF

# Konfigurationsdatei-Beispiel
echo '{"openai_api_key": "IhrAPIKeyHier"}' > "$config_dir/config.json"

# Informiere den Benutzer
echo "Projektstruktur für Salem wurde erstellt."
echo "Vergessen Sie nicht, Ihre API-Keys in '$config_dir/config.json' einzutragen."
