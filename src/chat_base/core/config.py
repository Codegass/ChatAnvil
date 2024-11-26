import os
from dataclasses import dataclass
from typing import Optional, Dict
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
    
    def __post_init__(self):
        """Initialize configuration with environment variables if not set programmatically."""
        if self.service_provider not in self.PROVIDER_DEFAULT_MODELS:
            raise ValueError(f"Unsupported service provider: {self.service_provider}")
            
        # Set API key from environment if not provided
        if self.api_key is None and self.service_provider in self.ENV_API_KEYS:
            env_key = self.ENV_API_KEYS[self.service_provider]
            self.api_key = os.getenv(env_key)
            
            if self.api_key is None and self.service_provider != 'ollama':
                raise ValueError(f"API key not found. Please set {env_key} environment variable or provide api_key parameter.")
        
        # Set model from environment or default if not provided
        if self.model is None:
            env_model_key = self.ENV_DEFAULT_MODELS[self.service_provider]
            self.model = os.getenv(env_model_key, self.PROVIDER_DEFAULT_MODELS[self.service_provider])
            
        # Set logging configuration from environment
        self.log_dir = os.getenv('LOG_FILE', 'logs')
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.debug = log_level.upper() == 'DEBUG'
            
    @property
    def provider_config(self) -> Dict[str, Optional[str]]:
        """Return provider-specific configuration."""
        config: Dict[str, Optional[str]] = {'model': self.model}
        
        if self.service_provider != 'ollama':
            config['api_key'] = self.api_key
            
        if self.service_provider == 'ollama':
            config['host'] = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
            
        return config
