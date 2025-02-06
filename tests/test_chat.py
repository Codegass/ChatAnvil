import pytest
from unittest.mock import MagicMock, patch
from chatanvil.core.chat import Chat
from chatanvil.providers.base import ChatProvider


def test_chat_initialization():
    """Test Chat class initialization."""
    chat = Chat(service_provider="openai")
    assert chat.provider_name == "openai"
    assert chat.provider is not None
    assert chat.parser_type == "default"  # 默认解析器


def test_chat_with_parser():
    """Test Chat class initialization with parser."""
    chat = Chat(service_provider="openai", parser_type="markdown")
    assert chat.provider_name == "openai"
    assert chat.provider is not None
    assert chat.parser_type == "markdown"


def test_chat_invalid_parser():
    """Test initialization with invalid parser."""
    with pytest.raises(ValueError, match="Unsupported parser"):
        Chat(service_provider="openai", parser_type="invalid_parser")


def test_chat_invalid_provider():
    """Test initialization with invalid provider."""
    with pytest.raises(ValueError, match="Unsupported provider.*"):
        Chat(service_provider="invalid_provider")


@patch("chatanvil.providers.openai.OpenAIChat")
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


@patch("chatanvil.providers.openai.OpenAIChat")
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


@patch("chatanvil.providers.openai.OpenAIChat")
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


@patch("chatanvil.core.chat.OpenAIChat")
def test_parser_switching(mock_openai):
    """Test parser switching functionality."""
    chat = Chat(service_provider="openai", parser_type="markdown")
    assert chat.get_current_parser() == "markdown"

    chat.set_parser("json")
    assert chat.get_current_parser() == "json"

    with pytest.raises(ValueError, match="Unsupported parser"):
        chat.set_parser("invalid_parser")


@patch("chatanvil.core.chat.OpenAIChat")
def test_chat_completion(mock_openai):
    """Test chat completion with multiple messages."""
    # Setup mock
    mock_instance = MagicMock()
    mock_instance.get_chat_completion.return_value = "Test completion"
    mock_openai.return_value = mock_instance

    # Test
    chat = Chat(service_provider="openai")
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]
    response = chat.get_chat_completion(messages=messages)

    assert response == "Test completion"
    mock_instance.get_chat_completion.assert_called_once_with(
        messages=messages,
        model=None,
        temperature=0.7,
        max_tokens=None,
    )
