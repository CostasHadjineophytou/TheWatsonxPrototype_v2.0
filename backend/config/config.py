import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management"""
    # API Keys and Authentication
    IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
    
    # Service URLs
    IBM_CLOUD_MODELS_URL = os.getenv('IBM_CLOUD_MODELS_URL')
    IBM_CLOUD_PROJECTS_URL = os.getenv('IBM_CLOUD_PROJECTS_URL')
    IAM_TOKEN_URL = os.getenv('IAM_TOKEN_URL')

    @staticmethod
    def validate():
        """Validate all required configuration is present"""
        required_vars = [
            'IBM_CLOUD_API_KEY',
            'IBM_CLOUD_MODELS_URL',
            'IBM_CLOUD_PROJECTS_URL',
            'IAM_TOKEN_URL'
        ]
        
        missing = [var for var in required_vars 
                  if not getattr(Config, var)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")