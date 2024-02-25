# Project Salem

## Overview
This project offers a comprehensive solution integrating various functionalities such as automatic speech recognition (ASR), text-to-speech conversion (TTS), command interpretation, and interaction with the OpenAI API to generate responses based on user inputs. Developed in Python 3.10, it utilizes modern libraries and custom modules to ensure a seamless user experience.

## Developer's Note
Before we dive deeper into the documentation, I would like to extend a heartfelt apology for the code and some naming conventions that may have become a bit "wild" over the course of development. It was an intense and stressful weekend full of coding and creativity. I hope you still find joy and value in what has been created here. Thank you for your understanding and patience!

## Configuration
Before starting the program, you need to create a `config.json` file in the `config` folder. This file should contain the following configurations:

```json
{
  "openai_api_key": "sk-...",
  "elevenlabs_api_key": "...",
  "root_path": ".../.../..."
}
```

Ensure you provide your own API keys for OpenAI and ElevenLabs, as well as the desired root path.

## Installation

### Prerequisites
- Python 3.10
- pip (Python package installer)

### Installing Required Packages
To install the required Python packages, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes the following packages:
- openai
- elevenlabs
- sounddevice
- numpy

## Usage
To start the main application, execute the `main.py` script with Python 3.10:

```bash
python3 main.py
```

Ensure all project-specific modules (`asr.py`, `CommandParser.py`, etc.) are located in the same directory or appropriately referenced in your Python environment.

## Module Overview
- `main.py`: The entry point of the application, orchestrating the overall functionality.
- `asr.py`: Responsible for automatic speech recognition.
- `CommandParser.py`: Interprets commands and orchestrates actions based on these commands.
- `elevenlabstts.py`: Integrates ElevenLabs' API for text-to-speech conversion.
- `FileSearcher.py`: Provides file search functionality within the project.
- `OpenAIGenerator.py`: Manages interactions with the OpenAI API for generating textual content.
- `OpenAIHelper.py`: Assists in setting up and utilizing the OpenAI API.
- `recorder.py`: Manages audio recording for speech recognition.

Each module is designed to fulfill a specific function within the project. The interaction with OpenAI and ElevenLabs APIs is handled through the `OpenAIGenerator.py` and `elevenlabstts.py` modules, responsible for generating textual content and converting text to speech, respectively.

## Operating Instructions
- Start the program using the command above.
- Follow the on-screen instructions to interact with the program.
- The use of various functions is controlled by the commands defined in `CommandParser.py`.

## Contributing
Contributions to this project are welcome. Please ensure to follow the project's code standards and submit pull requests for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. 
