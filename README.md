# Chat Base

Chat Base is a Python project that provides a unified interface for interacting with various chat-based AI services, including OpenAI, Ollama, Groq, and Claude.

## Features

- Supports multiple AI service providers: OpenAI, Ollama, Groq, and Claude.
- Implements exponential backoff for retrying API requests.
- Logs API interactions and errors to log files.
- Allows setting and updating system prompts.
- Extracts code snippets from AI responses.
- Multiple output modes support:
  - Default mode: Regular chat experience
  - Markdown mode: Structured output in markdown format with code parsing
  - JSON mode: Structured output in JSON format for function calling
  - XML mode: Structured output with XML tags

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

### Basic Usage

```python
from model.chatbot import ChatBot

service_provider = 'openai'
chatbot = ChatBot(service_provider=service_provider)
print(chatbot.get_response('Hello, how are you?', "gpt-4"))
```

### Mode Selection

ChatBase supports four different output modes:

1. Default Mode
```python
chatbot = ChatBot(service_provider='openai', mode='default')
response = chatbot.get_response('What is Python?', "gpt-4")
# Returns regular chat response
```

2. Markdown Mode
```python
chatbot = ChatBot(service_provider='openai', mode='markdown')
response = chatbot.get_response('Write a Python function to sort a list', "gpt-4")
# Returns markdown-formatted response with code blocks
code_blocks = chatbot.parse_markdown(response)  # Extract code blocks
```

3. JSON Mode (Function Calling)
```python
chatbot = ChatBot(service_provider='openai', mode='json')
response = chatbot.get_response('Get current weather in New York', "gpt-4")
# Returns JSON-structured response
parsed_data = chatbot.parse_json(response)  # Parse JSON response
```

4. XML Mode
```python
chatbot = ChatBot(service_provider='openai', mode='xml')
response = chatbot.get_response('Analyze the sentiment of this text', "gpt-4")
# Returns XML-structured response
parsed_data = chatbot.parse_xml(response)  # Parse XML response
```

### Mode-Specific Features

#### Markdown Mode
- Automatically formats output in markdown
- Provides code block extraction
- Supports syntax highlighting
- Ideal for documentation and code examples

#### JSON Mode
- Structured output for programmatic use
- Perfect for function calling and API integrations
- Consistent data format for parsing
- Supports complex nested structures

#### XML Mode
- Tag-based structure for hierarchical data
- Easy to parse and validate
- Suitable for document-style outputs
- Supports attributes and nested elements

## Logging
Logs are saved in the `log` directory with timestamps in the filenames. Each service has its own log file.

