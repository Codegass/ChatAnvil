import pytest
from unittest.mock import MagicMock, patch
from chat_base.providers.groq import GroqChat

@pytest.fixture
def groq_chat():
    """Fixture for Groq chat instance."""
    with patch('groq.Client') as mock_client:
        chat = GroqChat(api_key="test_key")
        chat.client = mock_client
        yield chat

def test_initialization():
    """Test Groq chat initialization."""
    with patch('groq.Client'):
        chat = GroqChat(api_key="test_key")
        assert chat.api_key == "test_key"
        assert chat.model is None

def test_initialization_no_key():
    """Test initialization without API key."""
    with pytest.raises(ValueError, match="Groq API key is required"):
        GroqChat()

def test_get_response(groq_chat):
    """Test getting response from Groq."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    groq_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = groq_chat.get_response("Test message")
    
    assert response == "Test response"
    groq_chat.client.chat.completions.create.assert_called_once()

def test_get_response_with_system_prompt(groq_chat):
    """Test getting response with system prompt."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    groq_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = groq_chat.get_response(
        "Test message",
        system_prompt="You are a helpful assistant"
    )
    
    assert response == "Test response"
    call_args = groq_chat.client.chat.completions.create.call_args[1]
    assert len(call_args["messages"]) == 2
    assert call_args["messages"][0]["role"] == "system"
    assert call_args["messages"][0]["content"] == "You are a helpful assistant"

def test_get_response_with_model(groq_chat):
    """Test getting response with specific model."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    groq_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = groq_chat.get_response("Test message", model="mixtral-8x7b")
    
    assert response == "Test response"
    groq_chat.client.chat.completions.create.assert_called_once()
    assert groq_chat.client.chat.completions.create.call_args[1]["model"] == "mixtral-8x7b"

def test_get_response_default_max_tokens(groq_chat):
    """Test default max_tokens value in get_response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    groq_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = groq_chat.get_response("Test message")
    
    assert response == "Test response"
    groq_chat.client.chat.completions.create.assert_called_once()
    assert groq_chat.client.chat.completions.create.call_args[1]["max_tokens"] == 400

def test_get_response_custom_max_tokens(groq_chat):
    """Test custom max_tokens value in get_response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    groq_chat.client.chat.completions.create.return_value = mock_response
    
    # Test
    response = groq_chat.get_response("Test message", max_tokens=1000)
    
    assert response == "Test response"
    groq_chat.client.chat.completions.create.assert_called_once()
    assert groq_chat.client.chat.completions.create.call_args[1]["max_tokens"] == 1000

def test_get_response_error(groq_chat):
    """Test error handling in get_response."""
    groq_chat.client.chat.completions.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        groq_chat.get_response("Test message")
