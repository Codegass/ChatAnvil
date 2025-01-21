import pytest
from unittest.mock import MagicMock, patch
import requests
from chatanvil.providers.ollama import OllamaChat


@pytest.fixture
def ollama_chat():
    """Fixture for Ollama chat instance."""
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        # Mock successful connection check
        mock_get.return_value.status_code = 200
        chat = OllamaChat(base_url="http://localhost:11434")
        yield chat, mock_post, mock_get


def test_initialization():
    """Test Ollama chat initialization."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        chat = OllamaChat(base_url="http://localhost:11434")
        assert chat.base_url == "http://localhost:11434"
        assert chat.model is None


def test_initialization_connection_error():
    """Test initialization with connection error."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = "Server error"

        with pytest.raises(ConnectionError, match="Failed to connect to Ollama"):
            OllamaChat()


def test_get_response(ollama_chat):
    """Test getting response from Ollama."""
    chat, mock_post, _ = ollama_chat

    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"message": {"content": "Test response"}}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Test
    response = chat.get_response("Test message")

    assert response == "Test response"
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == "http://localhost:11434/api/chat"


def test_get_response_with_system_prompt(ollama_chat):
    """Test getting response with system prompt."""
    chat, mock_post, _ = ollama_chat

    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"message": {"content": "Test response"}}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Test
    response = chat.get_response(
        "Test message", system_prompt="You are a helpful assistant"
    )

    assert response == "Test response"
    mock_post.assert_called_once()
    call_json = mock_post.call_args[1]["json"]
    assert len(call_json["messages"]) == 2
    assert call_json["messages"][0]["role"] == "system"
    assert call_json["messages"][0]["content"] == "You are a helpful assistant"


def test_get_response_with_model(ollama_chat):
    """Test getting response with specific model."""
    chat, mock_post, _ = ollama_chat

    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {"message": {"content": "Test response"}}
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Test
    response = chat.get_response("Test message", model="llama2")

    assert response == "Test response"
    mock_post.assert_called_once()
    assert mock_post.call_args[1]["json"]["model"] == "llama2"


def test_get_response_error(ollama_chat):
    """Test error handling in get_response."""
    chat, mock_post, _ = ollama_chat
    mock_post.side_effect = requests.exceptions.RequestException("API Error")

    with pytest.raises(Exception, match="API Error"):
        chat.get_response("Test message")
