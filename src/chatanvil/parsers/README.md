# Chat-Anvil Parsers

This module provides different parsers to handle various response formats from chat models. You can check the [example](../examples/chat_with_parser.py) for more details.

## Available Parsers

### Default Parser
The most basic parser that returns responses as-is without any processing.

```python
from chatanvil import Chat

chat = Chat("openai", parser_type="default")
response = chat.get_response("Hello!")
```

### Markdown Parser
Handles markdown formatted responses and can extract code blocks.

```python
chat = Chat("openai", parser_type="markdown")
response = chat.get_response(
    "Write a Python function to calculate fibonacci numbers "
    "and explain how it works with markdown formatting."
)
code_blocks = chat.extract_code(response)  # Returns list of {language, content}
```

### JSON Parser
Handles JSON formatted responses. To use this parser effectively, you should specify in your prompt that you want the code in a specific format:

```python
chat = Chat("openai", parser_type="json")
response = chat.get_response(
    "Please provide a JSON response with a Python function. "
    "Format the code using {language: 'python', content: 'your_code_here'}"
)
code_blocks = chat.extract_code(response)
```

Expected JSON format:
```json
{
    "code": {
        "language": "python",
        "content": "def example():\n    return 'Hello World!'"
    }
}
```

### XML Parser
Handles XML formatted responses and extracts code from CDATA sections.

```python
chat = Chat("openai", parser_type="xml")
response = chat.get_response(
    "Provide an XML document with a Python function in a code element "
    "using CDATA section."
)
code_blocks = chat.extract_code(response)
```

Expected XML format:
```xml
<response>
    <code language="python">
        <![CDATA[
        def example():
            return 'Hello World!'
        ]]>
    </code>
</response>
```

## Common Parser Methods

All parsers implement these methods:

- `parse_response(response: str) -> str`: Process the raw response
- `extract_code(response: str) -> List[Dict[str, str]]`: Extract code blocks from the response

## Switching Parsers

You can switch parsers at runtime:

```python
chat = Chat("openai", parser_type="markdown")
chat.set_parser("json")  # Switch to JSON parser
current_parser = chat.get_current_parser()  # Returns "json"
```

## Best Practices

1. **Markdown Parser**:
   - Best for general use and documentation-style responses
   - Automatically handles code blocks with language tags

2. **JSON Parser**:
   - Use when you need structured data
   - Specify the expected format in your prompt
   - Works best with the format: `{language: "...", content: "..."}`

3. **XML Parser**:
   - Good for highly structured responses
   - Use CDATA sections for code blocks
   - Specify language in code element attributes

4. **Default Parser**:
   - Use when you don't need any special processing
   - Cannot extract code blocks 