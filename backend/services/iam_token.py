import logging
from backend.config.config import Config
from backend.utils.base_client import BaseClient
from backend.utils.errors import AuthenticationError
from backend.utils.error_handling import handle_api_error
from backend.validators.service_validator import ServiceValidator

class IAMTokenService(BaseClient):
    """Handles IBM Cloud IAM token operations"""
    
    def __init__(self):
        super().__init__()
        self.token_url = Config.IAM_TOKEN_URL
        self.validator = ServiceValidator()

    def get_iam_token(self):
        """Retrieve IAM token using API key"""
        try:
            # Example if you want credentials validation
            self.validator.validate_credentials({"api_key": self.api_key})
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }
            
            # Form data as shown in the tutorial
            data = {
                'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                'apikey': self.api_key,
            }
            
            response = self._make_request(
                method='POST',
                url=self.token_url,
                headers=headers,
                data=data,
                is_form_data=True  # Specify this is form data
            )
            
            token = response.get('access_token')
            if not token:
                raise AuthenticationError(
                    message="No access token in response",
                    code="NO_TOKEN",
                    details={"response": response}
                )
                
            logging.info("Successfully retrieved IAM token")
            return token
            
        except Exception as e:
            logging.error(f"Failed to get IAM token: {str(e)}")
            raise handle_api_error(e) 