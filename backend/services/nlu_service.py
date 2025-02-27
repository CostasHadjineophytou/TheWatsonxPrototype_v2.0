from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .base_service import BaseService
from ..utils.errors import AuthenticationError, ValidationError

class NLUService(BaseService):
    """Handles raw NLU API interactions"""
    
    def __init__(self, credentials_manager):
        super().__init__()
        self.credentials_manager = credentials_manager
        self._nlu = None

    def initialize(self):
        """Initialize NLU client"""
        try:
            credentials = self.credentials_manager.get_service_credentials("Natural Language Understanding")
            authenticator = IAMAuthenticator(credentials['apikey'])
            self._nlu = NaturalLanguageUnderstandingV1(
                version='2021-08-01',
                authenticator=authenticator
            )
            self._nlu.set_service_url(credentials['url'])
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
        except ValidationError:
            raise
        except Exception as e:
            raise self.handle_error(e, "Failed to analyze text") 