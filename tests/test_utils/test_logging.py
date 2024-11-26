import pytest
import os
import logging
from unittest.mock import patch, MagicMock
from chat_base.utils.logging import ChatLogger

@pytest.fixture
def mock_config():
    with patch('chat_base.utils.logging.Config') as mock:
        config = MagicMock()
        config.log_dir = "/tmp/chat_base_logs"
        config.debug = False
        mock.return_value = config
        yield mock

def test_logger_initialization(mock_config, tmp_path):
    """Test logger initialization."""
    with patch('chat_base.utils.logging.os.makedirs') as mock_makedirs:
        logger = ChatLogger("test_provider")
        
        # Check if log directory is created
        mock_makedirs.assert_called_once_with("/tmp/chat_base_logs", exist_ok=True)
        
        # Check logger configuration
        assert logger.provider == "test_provider"
        assert logger.logger.name == "chat_base.test_provider"
        assert logger.logger.level == logging.INFO

def test_logger_debug_mode(mock_config):
    """Test logger in debug mode."""
    mock_config.return_value.debug = True
    
    logger = ChatLogger("test_provider")
    assert logger.logger.level == logging.DEBUG
    
    # Check if we have both file and console handlers
    handlers = logger.logger.handlers
    assert len(handlers) == 2
    assert any(isinstance(h, logging.FileHandler) for h in handlers)
    assert any(isinstance(h, logging.StreamHandler) for h in handlers)

def test_log_request(mock_config):
    """Test request logging."""
    logger = ChatLogger("test_provider")
    
    # Mock the logger's info method
    logger.logger.info = MagicMock()
    
    # Test with minimal parameters
    logger.log_request("Test message", None)
    logger.logger.info.assert_called_once()
    assert "Test message" in logger.logger.info.call_args[0][0]
    
    # Test with all parameters
    logger.logger.info.reset_mock()
    logger.log_request(
        "Test message",
        "gpt-4",
        "You are a helpful assistant"
    )
    logger.logger.info.assert_called_once()
    log_message = logger.logger.info.call_args[0][0]
    assert "Test message" in log_message
    assert "gpt-4" in log_message
    assert "You are a helpful assistant" in log_message

def test_log_response(mock_config):
    """Test response logging."""
    logger = ChatLogger("test_provider")
    logger.logger.info = MagicMock()
    
    logger.log_response("Test response")
    logger.logger.info.assert_called_once()
    assert "Test response" in logger.logger.info.call_args[0][0]

def test_log_error(mock_config):
    """Test error logging."""
    logger = ChatLogger("test_provider")
    logger.logger.error = MagicMock()
    
    error = ValueError("Test error")
    logger.log_error(error)
    logger.logger.error.assert_called_once()
    assert "Test error" in logger.logger.error.call_args[0][0]
    
    # Test with additional message
    logger.logger.error.reset_mock()
    logger.log_error(error, "Additional context")
    logger.logger.error.assert_called_once()
    log_message = logger.logger.error.call_args[0][0]
    assert "Test error" in log_message
    assert "Additional context" in log_message
