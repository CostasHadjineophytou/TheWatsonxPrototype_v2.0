from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError
from .credentials_manager import CredentialsManager
from ..validators.nlu_validator import NLUValidator
import logging

class NLUService(BaseService):
    """Handles raw NLU API interactions"""
    
    def __init__(self, credentials_manager: CredentialsManager, validator=None):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._nlu = None

        self.validator = validator or NLUValidator()

    def initialize(self):
        """Initialize NLU client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Natural Language Understanding")
            
            # Try API key validation first - this is the most important thing
            try:
                # Validate that the required resource exists - but catch errors
                self.validator.validate_resource(
                    required_resources=["natural-language-understanding"],
                    api_key=credentials['apikey'],
                    show_all_resources=False  # Only enable temporarily for debugging
                )
                logging.info("NLU service resources validated successfully")
            except ValidationError as val_err:
                # Log detailed error information about missing resources
                if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                    missing = val_err.details['missing_resources']
                    logging.warning(f"NLU validation failed - Missing resources: {', '.join(missing)}")
                    logging.warning(f"Please create these resources in your IBM Cloud account: {', '.join(missing)}")
                else:
                    logging.warning(f"NLU validation error: {str(val_err)}")
                # Continue with initialization anyway
            except Exception as ex:
                # For other exceptions, just log the error message
                logging.warning(f"NLU validation encountered an unexpected error: {str(ex)}")
            
            # Initialize the client even if validation had warnings
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._nlu = NaturalLanguageUnderstandingV1(
                version='2021-08-01',
                authenticator=authenticator
            )
            self._nlu.set_service_url(credentials['url'])
            logging.info("NLU service initialized successfully")
            
        except Exception as e:
            raise AuthenticationError(
                message="Failed to initialize NLU service",
                code="NLU_INIT_ERROR",
                details={"error": str(e)}
            )

    def analyze_text(self, text: str, features: dict) -> dict:
        """Raw API call to analyze text"""
        try:
            self.validator.validate_nlu_request(text, features)

            if not self._nlu:
                self.initialize()

            return self._nlu.analyze(
                text=text,
                features=features
            ).get_result()
            
        except ValidationError as e:
            raise e
        except AuthenticationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to analyze text") 