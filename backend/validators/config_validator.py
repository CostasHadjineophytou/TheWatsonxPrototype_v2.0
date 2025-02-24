from typing import List, Dict, Any
from ..utils.errors import ConfigurationError
from ..config.config import Config

class ConfigValidator:
    """Validates only environment-related configuration"""
    
    @staticmethod
    def validate_config() -> None:
        """Validate base configuration/environment variables"""
        required_vars = [
            'IBM_CLOUD_API_KEY',
            'IBM_CLOUD_MODELS_URL',
            'IBM_CLOUD_PROJECTS_URL',
            'IAM_TOKEN_URL'
        ]
        
        missing = [var for var in required_vars if not getattr(Config, var)]
        
        if missing:
            raise ConfigurationError(
                message="Missing required configuration",
                code="MISSING_CONFIG",
                details={"missing": missing}
            ) 