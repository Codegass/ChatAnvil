"""
ChatAnvil - A unified interface for interacting with various chat-based AI services.
"""

from .core.chat import Chat
from .core.config import Config

__version__ = "0.1.0"
__all__ = ["Chat", "Config"]

# 创建一个简单的别名模块
import sys
import types

# 创建一个新的模块对象
anvil = types.ModuleType('anvil')
anvil.Chat = Chat
anvil.Config = Config
anvil.__version__ = __version__

# 将模块添加到 sys.modules
sys.modules['anvil'] = anvil
