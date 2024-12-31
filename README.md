# Chat-base

A flexible and extensible Python library for interacting with multiple AI chat providers. Currently supports OpenAI, Anthropic (Claude), Groq, and Ollama.

## Features

- Unified interface for multiple AI chat providers
- Easy provider switching with consistent API
- Built-in retry mechanisms and error handling
- Configurable logging
- Environment variable support
- Type hints throughout

## Installation

```bash
pip install chat-base
```

## Quick Start

```python
from chat_base.core.chat import Chat

# Initialize with OpenAI
chat = Chat(service_provider='openai')

# Get a response
response = chat.get_response(
    message="What is the capital of France?",
    temperature=0.7
)
print(response)

# Switch to Claude
claude_chat = Chat(
    service_provider='claude',
    system_prompt="You are a helpful assistant that specializes in geography."
)

response = claude_chat.get_response(
    message="What are the top 3 largest cities in Japan?"
)
print(response)
```

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Or set them programmatically:

```python
chat = Chat(
    service_provider='openai',
    api_key='your-api-key',
    model='gpt-4'
)
```

## Supported Providers

- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Groq
- Ollama (local models)

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chat-base.git
cd chat-base
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
