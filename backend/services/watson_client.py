from ibm_watsonx_ai import APIClient, Credentials
from backend.config.config import Config
from .base_service import BaseService
from ..utils.errors import ValidationError, APIError

class WatsonClient(BaseService):
    """Handles the base Watson client setup and authentication."""
    
    def __init__(self):
        """Initialize Watson client with validation and error handling"""
        try:
            super().__init__()
            
            credentials = {
                'api_key': Config.IBM_CLOUD_API_KEY,
                'url': Config.IBM_CLOUD_MODELS_URL
            }
            self.validator.validate_credentials(credentials)
            
            self.credentials = Credentials(
                url=credentials['url'],
                api_key=credentials['api_key']
            )
            
            self.client = APIClient(self.credentials)
                
        except ValidationError as e:
            raise e
        except Exception as e:
            if isinstance(e, APIError):
                raise e
            raise self.handle_error(e, "Failed to initialize Watson client") 