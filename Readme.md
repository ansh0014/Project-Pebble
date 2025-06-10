# Pebbel - AI Voice Assistant

Pebbel is an intelligent voice-controlled AI assistant that can perform various tasks through voice commands. It integrates with Groq AI for advanced language processing capabilities and includes desktop automation features.

## Features

- Voice command recognition and response
- Integration with Groq AI for natural language processing
- Hotkey activation (Win+F11) for easy access
- Conversation history tracking
- Desktop automation capabilities
- Error handling and automatic recovery
- Configurable AI model settings

## Prerequisites

- Python 3.7 or higher
- Windows operating system (for hotkey functionality)
- Microphone for voice input
- Speakers for voice output

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Pebbel.git
cd Pebbel
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Groq API credentials:

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL_NAME=your_model_name_here
```

## Dependencies

The project uses the following main dependencies:

- `groq==0.22.0`: AI language model integration
- `python-dotenv==1.1.0`: Environment variable management
- `keyboard==0.13.5`: Hotkey detection
- `SpeechRecognition==3.14.2`: Voice recognition
- `PyAudio==0.2.14`: Audio input/output handling
- `PyAutoGUI==0.9.54`: Desktop automation
- `requests==2.32.3`: HTTP requests
- `pydantic==2.11.3`: Data validation
- `psutil==7.0.0`: System utilities
- `pycaw==20240210`: Windows audio control

For a complete list of dependencies, see `requirements.txt`.

## Usage

1. Run the main script:

```bash
python main.py
```

2. Press `Win+F11` to activate/deactivate the assistant
3. Speak your commands when the assistant is active
4. Use exit keywords like "exit", "quit", "shutdown", "stop", or "bye" to deactivate the assistant

## Voice Commands

The assistant responds to various voice commands, including:

- "Open AI" - Activates AI conversation mode
- Exit keywords to stop the assistant
- Custom commands defined in the command router

## Project Structure

- `main.py`: Core application logic and voice command processing
- `config.py`: Configuration and API key management
- `command_router.py`: Command processing and routing
- `Storedata_Groq.py`: Conversation history management
- `utils/`: Utility functions for voice recognition and speech synthesis

## Error Handling

The assistant includes robust error handling:

- Maximum error threshold (5 errors) before automatic shutdown
- Automatic recovery from minor errors
- Detailed error logging

## System Requirements

- Windows 10 or higher
- Python 3.7+
- Microphone and speakers
- Internet connection for AI features
- Sufficient system resources for voice processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- Groq AI for providing the language model integration
- All contributors and users of the project
