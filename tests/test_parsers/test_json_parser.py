import pytest
from chatanvil.parsers.json_parser import JSONParser

def test_json_parser_initialization():
    """Test JSON parser initialization."""
    parser = JSONParser()
    assert parser.type == 'json'

def test_parse_response_valid_json():
    """Test parsing valid JSON response."""
    parser = JSONParser()
    response = '{"code": {"language": "python", "content": "print(\'hello\')"}'
    parsed = parser.parse_response(response)
    assert isinstance(parsed, str)
    assert 'python' in parsed
    assert 'print' in parsed

def test_extract_code_from_json():
    """Test extracting code from JSON structure."""
    parser = JSONParser()
    response = '''
    {
        "code": {
            "language": "python",
            "content": "def hello():\\n    print('Hello')"
        }
    }
    '''
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 1
    assert blocks[0]['language'] == 'python'
    assert 'def hello():' in blocks[0]['content']

def test_extract_nested_code():
    """Test extracting code from nested JSON structure."""
    parser = JSONParser()
    response = '''
    {
        "functions": {
            "main": {
                "language": "python",
                "content": "def main():\\n    pass"
            },
            "helper": {
                "language": "python",
                "content": "def helper():\\n    pass"
            }
        }
    }
    '''
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 2

def test_parse_invalid_json():
    """Test parsing invalid JSON response."""
    parser = JSONParser()
    response = '{"code": invalid json'
    
    with pytest.raises(ValueError, match="Invalid JSON response"):
        parser.parse_response(response)

def test_extract_code_invalid_structure():
    """Test extracting code from invalid JSON structure."""
    parser = JSONParser()
    response = '{"data": "not a code block"}'
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 0  # Should return empty list for invalid structure

def test_extract_code_missing_fields():
    """Test extracting code with missing required fields."""
    parser = JSONParser()
    response = '''
    {
        "code": {
            "language": "python"
            # missing content field
        }
    }
    '''
    
    blocks = parser.extract_code(response)
    assert len(blocks) == 0  # Should skip invalid code blocks 