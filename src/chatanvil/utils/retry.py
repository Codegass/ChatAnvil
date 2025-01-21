import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Union, Tuple
from .logging import ChatLogger


def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    logger: Optional[ChatLogger] = None,
) -> Callable:
    """Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry
        logger: Optional ChatLogger instance for logging retries
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            delay = base_delay

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        if logger:
                            logger.log_error(e, f"Failed after {max_retries} retries")
                        raise

                    # Calculate next delay with exponential backoff
                    delay = min(delay * 2, max_delay)

                    if logger:
                        logger.log_error(
                            e,
                            f"Attempt {retries}/{max_retries} failed. "
                            f"Retrying in {delay:.1f} seconds...",
                        )

                    time.sleep(delay)

        return wrapper

    return decorator


def retry_on_rate_limit(
    func: Optional[Callable] = None,
    *,
    max_retries: int = 5,
    base_delay: float = 2.0,
    logger: Optional[ChatLogger] = None,
) -> Union[Callable, Any]:
    """Decorator specifically for handling rate limit errors.

    This can be used with or without parameters:
    @retry_on_rate_limit
    def func(): ...

    or

    @retry_on_rate_limit(max_retries=3)
    def func(): ...
    """
    if func is None:
        return lambda f: retry_with_exponential_backoff(
            max_retries=max_retries,
            base_delay=base_delay,
            exceptions=(Exception,),  # Replace with specific rate limit exceptions
            logger=logger,
        )(f)

    return retry_with_exponential_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        exceptions=(Exception,),  # Replace with specific rate limit exceptions
        logger=logger,
    )(func)
