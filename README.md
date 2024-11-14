# Chat Base

Chat Base is a Python project that provides a unified interface for interacting with various chat-based AI services, including OpenAI, Ollama, Groq, and Claude.

## Features

- Supports multiple AI service providers: OpenAI, Ollama, Groq, and Claude.
- Implements exponential backoff for retrying API requests.
- Logs API interactions and errors to log files.
- Allows setting and updating system prompts.
- Extracts code snippets from AI responses.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/codegass/chat-base.git
    cd chat-base
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

### Using Global Environment Variables
Set the necessary environment variables for the API keys:
```sh
export OPENAI_KEY='your_openai_api_key'
export CLAUDE_KEY='your_claude_api_key'
export GROQ_KEY='your_groq_api_key'
```

You can consider to set these key as environment variables in your `.bashrc` or `.bash_profile` file. If you are using windows, you can set these keys in the environment variables settings.

### Using .env file
Create a file named `.env` in the root directory and add the following lines:

```
OPENAI_KEY='your_openai_api_key'
CLAUDE_KEY='your_claude_api_key'
GROQ_KEY='your_groq_api_key'
```
    
Then, install the `python-dotenv` package:
```sh
pip install python-dotenv
```

and load the environment variables in the `main.py` file:
```python
from dotenv import load_dotenv
load_dotenv()

from model.chatbot import ChatBot

service_provider = 'openai'
chatbot = ChatBot(service_provider=service_provider) 
# if you don't want to use the environment variables, you can use the local_key approach
print(chatbot.get_response('Hello, how are you?', "gpt-4o"))
```

This will be useful if you are using separate keys from same service provider for different projects.

### Using local_key approach
Also, you can use the local_key approach to store the keys in a file named `SCRECTS_DEV.py` (or other as you prefered) in the root directory. The file should contain the following lines:

```python
OPENAI_KEY = 'your_openai_api_key'
CLAUDE_KEY = 'your_claude_api_key'
GROQ_KEY = 'your_groq_api_key'
```

and add the following line to the `.gitignore` file:

```
SCRECTS_DEV.py (or other name you used)
```

lastly, you can import the keys in the `main.py` file as follows:

```python
from model.chatbot import ChatBot
from SCRECTS_DEV import OPENAI_KEY, CLAUDE_KEY, GROQ_KEY # if you used a different name, replace SCRECTS_DEV with the name you used

service_provider = 'openai'
chatbot = ChatBot(local_key=OPENAI_KEY, service_provider=service_provider) 
# if you don't want to use the local_key approach, you can use the environment variables and remove the local_key parameter
print(chatbot.get_response('Hello, how are you?', "gpt-4o"))
```




## Usage

You can use the `main.py` script to interact with the chat services. Modify the `service_provider` parameter to switch between different AI services.

```sh
python main.py
```

## Logging
Logs are saved in the `log` directory with timestamps in the filenames. Each service has its own log file.

