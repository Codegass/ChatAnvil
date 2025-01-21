import pytest
from unittest.mock import MagicMock, patch
from chatanvil.providers.openai import OpenAIChat

@pytest.fixture
def openai_chat():
    """Fixture for OpenAI chat instance."""
    with patch('openai.OpenAI') as mock_openai:
        chat = OpenAIChat(api_key="test_key")
        chat.client = mock_openai
        yield chat

def test_initialization():
    """Test OpenAI chat initialization."""
    with patch('openai.OpenAI'):
        chat = OpenAIChat(api_key="test_key")
        assert chat.api_key == "test_key"
        assert chat.model is None

def test_initialization_no_key():
    """Test initialization without API key."""
    with pytest.raises(ValueError, match="OpenAI API key is required"):
        OpenAIChat()

def test_get_response(openai_chat):
    """Test getting response from OpenAI."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    openai_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = openai_chat.get_response("Test message")
    
    assert response == "Test response"
    openai_chat.client.chat.completions.create.assert_called_once()

def test_get_response_with_system_prompt(openai_chat):
    """Test getting response with system prompt."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    openai_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = openai_chat.get_response(
        "Test message",
        system_prompt="You are a helpful assistant"
    )
    
    assert response == "Test response"
    call_args = openai_chat.client.chat.completions.create.call_args[1]
    assert len(call_args["messages"]) == 2
    assert call_args["messages"][0]["role"] == "system"
    assert call_args["messages"][0]["content"] == "You are a helpful assistant"

def test_get_response_with_model(openai_chat):
    """Test getting response with specific model."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    openai_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = openai_chat.get_response("Test message", model="gpt-4")
    
    assert response == "Test response"
    openai_chat.client.chat.completions.create.assert_called_once()
    assert openai_chat.client.chat.completions.create.call_args[1]["model"] == "gpt-4"

def test_get_response_error(openai_chat):
    """Test error handling in get_response."""
    openai_chat.client.chat.completions.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        openai_chat.get_response("Test message")
