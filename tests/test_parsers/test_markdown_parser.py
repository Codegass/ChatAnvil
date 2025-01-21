import pytest
from chatanvil.parsers.markdown import MarkdownParser

def test_markdown_parser_initialization():
    """Test markdown parser initialization."""
    parser = MarkdownParser()
    assert parser.type == 'markdown'

def test_parse_response():
    """Test parsing markdown response."""
    parser = MarkdownParser()
    response = "# Title\nSome text\n```python\ncode\n```"
    parsed = parser.parse_response(response)
    assert parsed == response  # Markdown parser preserves formatting

def test_extract_code_single_block():
    """Test extracting single code block."""
    parser = MarkdownParser()
    response = "```python\ndef hello():\n    print('Hello')\n```"
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 1
    assert blocks[0]['language'] == 'python'
    assert 'def hello():' in blocks[0]['content']

def test_extract_code_multiple_blocks():
    """Test extracting multiple code blocks."""
    parser = MarkdownParser()
    response = """```python
def hello():
    print('Hello')
```
    Some text
    ```javascript
    console.log('Hello');
    ```
    """
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 2
    assert blocks[0]['language'] == 'python'
    assert blocks[1]['language'] == 'javascript'

def test_extract_code_no_language():
    """Test extracting code block without language specification."""
    parser = MarkdownParser()
    response = "```\ncode\n```"
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 1
    assert blocks[0]['language'] == ''

def test_extract_code_malformed_blocks():
    """Test extracting malformed code blocks."""
    parser = MarkdownParser()
    response = """
    ```python
    unclosed block
    
    ``` invalid
    another block```
    """
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 0  # Should handle malformed blocks gracefully

def test_extract_code_with_indentation():
    """Test extracting code blocks with indentation."""
    parser = MarkdownParser()
    response = """
        ```python
        def indented():
            pass
        ```
    """
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 1
    assert "def indented():" in blocks[0]['content']

def test_extract_code_with_empty_blocks():
    """Test extracting empty code blocks."""
    parser = MarkdownParser()
    response = "```python\n```"
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 1
    assert blocks[0]['content'] == "" 