import logging
from backend.config.config import Config
from backend.services.base_client import BaseClient
from backend.utils.errors import AuthenticationError

class IAMTokenService(BaseClient):
    """Handles IBM Cloud IAM token operations."""

    def __init__(self):
        # BaseClient checks for API key and may raise ConfigurationError if missing
        super().__init__()
        self.token_url = Config.IAM_TOKEN_URL

    def get_iam_token(self):
        """Retrieve IAM token using the configured API key."""
        try:
            # Validate credentials
            self.validator.validate_credentials({"api_key": self.api_key})

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
            }

            # Form data for IBM Cloud's IAM token endpoint
            data = {
                'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                'apikey': self.api_key,
            }

            # Use BaseClient's _make_request to unify behavior and error handling
            response_json = self._make_request(
                method='POST',
                url=self.token_url,
                headers=headers,
                data=data,
                is_form_data=True  # Tells _make_request to send the data as form data
            )

            # response_json is the parsed JSON dict returned by _make_request
            token = response_json.get('access_token')
            if not token:
                raise AuthenticationError(
                    message="No access token in response",
                    code="NO_TOKEN",
                    details={"response": response_json}
                )

            logging.info("Successfully retrieved IAM token")
            return token

        except AuthenticationError as auth_err:
            # Already a known authentication error; log if desired, then re-raise
            logging.error(f"IAM Token authentication error: {auth_err}")
            raise auth_err

        except Exception as e:
            # Convert any other unknown exception to our custom error types
            raise self.handle_error(e, "Failed to get IAM token") 