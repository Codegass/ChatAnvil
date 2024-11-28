import pytest
from unittest.mock import MagicMock, patch
from chat_base.providers.claude import ClaudeChat

@pytest.fixture
def claude_chat():
    """Fixture for Claude chat instance."""
    with patch('anthropic.Client') as mock_client:
        chat = ClaudeChat(api_key="test_key")
        chat.client = mock_client
        yield chat

def test_initialization():
    """Test Claude chat initialization."""
    with patch('anthropic.Client'):
        chat = ClaudeChat(api_key="test_key")
        assert chat.api_key == "test_key"
        assert chat.model is None

def test_initialization_no_key():
    """Test initialization without API key."""
    with pytest.raises(ValueError, match="Claude API key is required"):
        ClaudeChat()

def test_get_response(claude_chat):
    """Test getting response from Claude."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    claude_chat.client.messages.create.return_value = mock_response
    
    # Test
    response = claude_chat.get_response("Test message")
    
    assert response == "Test response"
    claude_chat.client.messages.create.assert_called_once()

def test_get_response_default_max_tokens(claude_chat):
    """Test default max_tokens value in get_response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    claude_chat.client.messages.create.return_value = mock_response
    
    # Test
    response = claude_chat.get_response("Test message")
    
    assert response == "Test response"
    claude_chat.client.messages.create.assert_called_once()
    assert claude_chat.client.messages.create.call_args[1]["max_tokens"] == 4000

def test_get_response_custom_max_tokens(claude_chat):
    """Test custom max_tokens value in get_response."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    claude_chat.client.messages.create.return_value = mock_response
    
    # Test
    response = claude_chat.get_response("Test message", max_tokens=1000)
    
    assert response == "Test response"
    claude_chat.client.messages.create.assert_called_once()
    assert claude_chat.client.messages.create.call_args[1]["max_tokens"] == 1000

def test_get_response_with_system_prompt(claude_chat):
    """Test getting response with system prompt."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    claude_chat.client.messages.create.return_value = mock_response
    
    # Test
    response = claude_chat.get_response(
        "Test message",
        system_prompt="You are a helpful assistant"
    )
    
    assert response == "Test response"
    call_args = claude_chat.client.messages.create.call_args[1]
    assert "system" in call_args
    assert call_args["system"] == "You are a helpful assistant"
    assert len(call_args["messages"]) == 1
    assert call_args["messages"][0]["role"] == "user"
    assert call_args["messages"][0]["content"] == "Test message"

def test_get_response_with_model(claude_chat):
    """Test getting response with specific model."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Test response")]
    claude_chat.client.messages.create.return_value = mock_response
    
    # Test
    response = claude_chat.get_response("Test message", model="claude-3-opus")
    
    assert response == "Test response"
    claude_chat.client.messages.create.assert_called_once()
    assert claude_chat.client.messages.create.call_args[1]["model"] == "claude-3-opus"

def test_get_response_error(claude_chat):
    """Test error handling in get_response."""
    claude_chat.client.messages.create.side_effect = Exception("API Error")
    
    with pytest.raises(Exception, match="API Error"):
        claude_chat.get_response("Test message")
