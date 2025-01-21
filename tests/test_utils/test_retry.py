import pytest
import time
from unittest.mock import MagicMock, patch
from chatanvil.utils.retry import retry_with_exponential_backoff, retry_on_rate_limit
from chatanvil.utils.logging import ChatLogger

def test_retry_with_exponential_backoff_success():
    """Test successful retry with exponential backoff."""
    mock_func = MagicMock(return_value="success")
    decorated = retry_with_exponential_backoff()(mock_func)
    
    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 1

def test_retry_with_exponential_backoff_retry():
    """Test retry with exponential backoff on failure."""
    mock_func = MagicMock(side_effect=[ValueError, ValueError, "success"])
    mock_logger = MagicMock(spec=ChatLogger)
    
    decorated = retry_with_exponential_backoff(
        max_retries=3,
        base_delay=0.1,
        logger=mock_logger
    )(mock_func)
    
    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 3
    assert mock_logger.log_error.call_count == 2

def test_retry_with_exponential_backoff_max_retries():
    """Test retry with exponential backoff reaching max retries."""
    mock_func = MagicMock(side_effect=ValueError("Test error"))
    mock_logger = MagicMock(spec=ChatLogger)
    
    decorated = retry_with_exponential_backoff(
        max_retries=3,
        base_delay=0.1,
        logger=mock_logger
    )(mock_func)
    
    with pytest.raises(ValueError, match="Test error"):
        decorated()
    
    assert mock_func.call_count == 4  # Initial try + 3 retries
    assert mock_logger.log_error.call_count == 4

def test_retry_with_exponential_backoff_delay():
    """Test that delays between retries increase exponentially."""
    mock_func = MagicMock(side_effect=[ValueError, ValueError, "success"])
    mock_sleep = MagicMock()
    
    with patch('time.sleep', mock_sleep):
        decorated = retry_with_exponential_backoff(
            max_retries=3,
            base_delay=1.0,
            max_delay=4.0
        )(mock_func)
        
        decorated()
        
        # First retry should wait base_delay (1.0)
        # Second retry should wait min(base_delay * 2, max_delay) (2.0)
        assert mock_sleep.call_args_list[0][0][0] == 1.0
        assert mock_sleep.call_args_list[1][0][0] == 2.0

def test_retry_on_rate_limit_decorator():
    """Test retry_on_rate_limit decorator."""
    mock_func = MagicMock(side_effect=[ValueError("Rate limit"), "success"])
    
    # Test as decorator without parameters
    decorated = retry_on_rate_limit(mock_func)
    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 2
    
    # Test as decorator with parameters
    mock_func.reset_mock()
    mock_func.side_effect = [ValueError("Rate limit"), "success"]
    decorated = retry_on_rate_limit(max_retries=2)(mock_func)
    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 2

def test_retry_on_rate_limit_with_logger():
    """Test retry_on_rate_limit with logger."""
    mock_func = MagicMock(side_effect=[ValueError("Rate limit"), "success"])
    mock_logger = MagicMock(spec=ChatLogger)
    
    decorated = retry_on_rate_limit(
        max_retries=2,
        logger=mock_logger
    )(mock_func)
    
    result = decorated()
    assert result == "success"
    assert mock_func.call_count == 2
    assert mock_logger.log_error.call_count == 1
