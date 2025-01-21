import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Configuration class for chat providers and logging."""
    
    # Provider-specific configurations
    service_provider: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    log_dir: Optional[str] = None
    debug: bool = False
    
    # Default configuration values
    DEFAULT_MAX_TOKENS = {
        'openai': 2048,
        'claude': 4000,
        'groq': 1024,
        'ollama': 2048
    }
    
    DEFAULT_TEMPERATURE = 0.7
    
    # Provider-specific default models
    PROVIDER_DEFAULT_MODELS = {
        'openai': 'gpt-4o-mini',  # Updated to match .env default
        'claude': 'claude-3-sonnet-20240229',
        'groq': 'mixtral-8x7b-32768',
        'ollama': 'llama3.1'  # Updated to match .env default
    }
    
    # Environment variable mappings
    ENV_API_KEYS = {
        'openai': 'OPENAI_API_KEY',
        'claude': 'ANTHROPIC_API_KEY',
        'groq': 'GROQ_API_KEY'
    }
    
    ENV_DEFAULT_MODELS = {
        'openai': 'OPENAI_DEFAULT_MODEL',
        'claude': 'ANTHROPIC_DEFAULT_MODEL',
        'groq': 'GROQ_DEFAULT_MODEL',
        'ollama': 'OLLAMA_DEFAULT_MODEL'
    }
    
    ENV_MAX_TOKENS = {
        'openai': 'OPENAI_MAX_TOKENS',
        'claude': 'ANTHROPIC_MAX_TOKENS',
        'groq': 'GROQ_MAX_TOKENS',
        'ollama': 'OLLAMA_MAX_TOKENS'
    }
    
    def __post_init__(self):
        """Initialize configuration with environment variables if not set programmatically."""
        if self.service_provider not in self.PROVIDER_DEFAULT_MODELS:
            raise ValueError(f"Unsupported service provider: {self.service_provider}")
            
        # Set API key from environment if not provided
        if self.api_key is None and self.service_provider in self.ENV_API_KEYS:
            env_key = self.ENV_API_KEYS[self.service_provider]
            self.api_key = os.getenv(env_key)
            
            if self.api_key is None and self.service_provider != 'ollama':
                raise ValueError(f"API key not found in environment variable: {env_key}")
        
        # Set model from environment if not provided
        if self.model is None:
            env_model_key = self.ENV_DEFAULT_MODELS.get(self.service_provider)
            if env_model_key:
                self.model = os.getenv(env_model_key, self.PROVIDER_DEFAULT_MODELS[self.service_provider])
            else:
                self.model = self.PROVIDER_DEFAULT_MODELS[self.service_provider]
        
        # Set log directory from environment if not provided
        if self.log_dir is None:
            self.log_dir = os.getenv('LOG_DIR')
            if self.log_dir and not os.path.isabs(self.log_dir):
                # Make relative paths relative to current working directory
                self.log_dir = os.path.abspath(self.log_dir)
        
        # Set logging configuration from environment
        self.debug = os.getenv('LOG_LEVEL', 'INFO').upper() == 'DEBUG'
        
        # Set temperature from environment
        self.temperature = float(os.getenv('TEMPERATURE', str(self.DEFAULT_TEMPERATURE)))
        
        # Set max tokens from environment or use provider-specific defaults
        env_max_tokens = self.ENV_MAX_TOKENS.get(self.service_provider)
        if env_max_tokens:
            self.max_tokens = int(os.getenv(env_max_tokens, str(self.DEFAULT_MAX_TOKENS[self.service_provider])))
        else:
            self.max_tokens = self.DEFAULT_MAX_TOKENS[self.service_provider]
    
    @property
    def provider_config(self) -> Dict[str, Any]:
        """Return provider-specific configuration."""
        config = {
            'model': self.model,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        
        if self.service_provider != 'ollama':
            config['api_key'] = self.api_key
            
        if self.service_provider == 'ollama':
            config['host'] = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
            
        return config
