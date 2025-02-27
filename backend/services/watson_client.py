from ibm_watsonx_ai import APIClient, Credentials
from backend.config.config import Config
from .base_service import BaseService
from ..utils.errors import ValidationError

class WatsonClient(BaseService):
    """Handles the base Watson client setup and authentication."""
    
    def __init__(self):
        """Initialize Watson client with validation and error handling"""
        super().__init__()
        
        try:
            # Validate credentials
            credentials = {
                'api_key': Config.IBM_CLOUD_API_KEY,
                'url': Config.IBM_CLOUD_MODELS_URL
            }
            self.validator.validate_credentials(credentials)
            
            # Create credentials object using the API key & models URL
            self.credentials = Credentials(
                url=credentials['url'],
                api_key=credentials['api_key']
            )
            
            # Create APIClient object with error handling
            try:
                self.client = APIClient(self.credentials)
            except Exception as e:
                raise self.handle_error(e, "Failed to initialize Watson API client")
                
        except ValidationError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to initialize Watson client") 