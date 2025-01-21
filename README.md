# ChatAnvil

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
pip install chatanvil
```

## Quick Start

```python
# After installation via pip
from anvil import Chat  # Simple alias
# or
from chatanvil import Chat  # Full package name

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
    model='gpt-4o'
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
git clone git@github.com:Codegass/ChatAnvil.git
cd ChatAnvil
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

4. Run examples:
```bash
# Examples in the repository use direct imports
python examples/basic_chat.py
python examples/chat_with_parser.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
