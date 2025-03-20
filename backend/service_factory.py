from backend.services.watson_client import WatsonClient
from backend.services.iam_token import IAMTokenService
from backend.services.model_service import ModelService
from backend.services.project_service import ProjectService
from backend.services.text_service import TextService
from backend.services.credentials_manager import CredentialsManager
from backend.services.nlu_service import NLUService
from backend.services.tts_service import TTSService
from backend.services.stt_service import STTService
from backend.services.service_checker import ServiceCheckerService
from .validators.config_validator import ConfigValidator
from .validators.base_validator import BaseValidator
from .validators.stt_validator import STTValidator
from .validators.text_validator import TextValidator
# Import other validators as needed

class ServiceFactory:
    """Factory for creating service instances with appropriate validators
    
    This factory creates service instances and injects the appropriate validators:
    - Generic services use the BaseValidator (provided by BaseComponent)
    - Specialized services receive their specific validators
    
    The architecture follows a composition pattern where:
    1. BaseComponent provides error handling and basic validation
    2. Service-specific validators extend BaseValidator for specialized validation
    3. Services override the default validator when needed
    """
    
    def __init__(self):
        # Validate configuration
        ConfigValidator.validate_config()
        
        # Create core services
        self.watson_client = WatsonClient()
        self.iam_service = IAMTokenService()
        self.credentials_manager = self.create_credentials_manager()
        
        # Create validators
        # Generic services will use BaseValidator (already provided by BaseComponent)
        # Specific services will use their dedicated validators
        self.stt_validator = STTValidator()
        self.text_validator = TextValidator()
        # Initialize other validators as needed
        
    def create_model_service(self) -> ModelService:
        # Uses BaseValidator from BaseComponent
        return ModelService(self.watson_client)
        
    def create_project_service(self) -> ProjectService:
        # Uses BaseValidator from BaseComponent
        return ProjectService(self.watson_client, self.iam_service)
        
    def create_text_service(self) -> TextService:
        # Inject the text-specific validator
        return TextService(self.watson_client, self.text_validator)
        
    def create_credentials_manager(self) -> CredentialsManager:
        # Uses BaseValidator from BaseComponent
        return CredentialsManager()

    def create_nlu_service(self) -> NLUService:
        # TODO: Create and inject NLUValidator
        return NLUService(self.credentials_manager)

    def create_tts_service(self) -> TTSService:
        # TODO: Create and inject TTSValidator
        return TTSService(self.credentials_manager)

    def create_stt_service(self) -> STTService:
        # Inject the STT-specific validator
        return STTService(self.credentials_manager, self.stt_validator)
        
    def create_service_checker_service(self) -> ServiceCheckerService:
        # Uses BaseValidator from BaseComponent
        return ServiceCheckerService(self.iam_service) 