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

Set the necessary environment variables for the API keys:
```sh
export OPENAI_API_KEY='your_openai_api_key'
export CLAUDE_API_KEY='your_claude_api_key'
export GROQ_API_KEY='your_groq_api_key'
```

## Usage

You can use the `main.py` script to interact with the chat services. Modify the `service_provider` parameter to switch between different AI services.

```sh
python main.py
```

## Logging
Logs are saved in the `log` directory with timestamps in the filenames. Each service has its own log file.

