import logging
from backend.config.config import Config
from backend.services.base_client import BaseClient
from backend.utils.errors import AuthenticationError, ValidationError
from backend.utils.token_utils import get_iam_token

class IAMTokenService(BaseClient):
    """Handles IBM Cloud IAM token operations."""

    def __init__(self):
        # BaseClient checks for API key and may raise ConfigurationError if missing
        super().__init__()
        self.token_url = Config.IAM_TOKEN_URL

    def get_api_key(self):
        """
        Get the API key used by this service
        
        Returns:
            The API key string
        """
        return self.api_key

    def get_iam_token(self):
        """Retrieve IAM token using the configured API key."""
        try:
            # Validate credentials
            self.validator.validate_credentials({"api_key": self.api_key})
            
            # Use the centralised token utility function
            token = get_iam_token(self.api_key)
            
            logging.info("Successfully retrieved IAM token")
            return token

        except ValidationError as e:
            raise e
        except AuthenticationError as e:
            logging.error(f"IAM Token authentication error: {e}")
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to get IAM token") 