from ibm_watsonx_ai import APIClient, Credentials
from backend.config.config import Config

class WatsonClient:
    """Handles the base Watson client setup and authentication."""
    
    def __init__(self):
        self.api_key = Config.IBM_CLOUD_API_KEY
        self.models_url = Config.IBM_CLOUD_MODELS_URL
        
        # Create credentials object using the API key & models URL
        self.credentials = Credentials(
            url=self.models_url,
            api_key=self.api_key
        )
        # Create APIClient object using the credentials
        self.client = APIClient(self.credentials) 