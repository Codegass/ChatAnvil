import pytest
from unittest.mock import MagicMock, patch
from chatanvil.core.chat import Chat
from chatanvil.providers.base import ChatProvider


def test_chat_initialization():
    """Test Chat class initialization."""
    chat = Chat(service_provider="openai")
    assert chat.provider_name == "openai"
    assert chat.provider is not None


def test_chat_invalid_provider():
    """Test initialization with invalid provider."""
    with pytest.raises(ValueError, match="Unsupported provider"):
        Chat(service_provider="invalid_provider")


@patch("chatanvil.core.chat.OpenAIChat")
def test_chat_response(mock_openai):
    """Test getting response from provider."""
    # Setup mock
    mock_instance = MagicMock()
    mock_instance.get_response.return_value = "Test response"
    mock_openai.return_value = mock_instance

    # Test
    chat = Chat(service_provider="openai")
    response = chat.get_response("Test message")

    assert response == "Test response"
    mock_instance.get_response.assert_called_once_with(
        "Test message", model=None, system_prompt=None, temperature=0.7, max_tokens=None
    )


@patch("chatanvil.core.chat.OpenAIChat")
def test_chat_with_system_prompt(mock_openai):
    """Test chat with system prompt."""
    # Setup mock
    mock_instance = MagicMock()
    mock_openai.return_value = mock_instance

    # Test
    chat = Chat(service_provider="openai")
    chat.set_system_prompt("You are a helpful assistant")
    chat.get_response("Test message")

    mock_instance.get_response.assert_called_once_with(
        "Test message",
        model=None,
        system_prompt="You are a helpful assistant",
        temperature=0.7,
        max_tokens=None,
    )


@patch("chatanvil.core.chat.OpenAIChat")
def test_chat_with_model_override(mock_openai):
    """Test chat with model override."""
    # Setup mock
    mock_instance = MagicMock()
    mock_openai.return_value = mock_instance

    # Test
    chat = Chat(service_provider="openai", model="gpt-4")
    chat.get_response("Test message")

    mock_instance.get_response.assert_called_once_with(
        "Test message",
        model="gpt-4",
        system_prompt=None,
        temperature=0.7,
        max_tokens=None,
    )
