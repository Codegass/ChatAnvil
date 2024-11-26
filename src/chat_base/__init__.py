"""
Chat Base - A unified interface for interacting with various chat-based AI services.
"""

from .core.chat import Chat
from .core.config import Config

__version__ = "0.1.0"
__all__ = ["Chat", "Config"]
