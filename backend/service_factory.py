from backend.services.watson_client import WatsonClient
from backend.services.iam_token import IAMTokenService
from backend.services.model_service import ModelService
from backend.services.project_service import ProjectService
from backend.services.text_service import TextService
from backend.services.credentials_manager import CredentialsManager
from backend.services.nlu_service import NLUService
from backend.services.tts_service import TTSService
from backend.services.stt_service import STTService
from .validators.config_validator import ConfigValidator

class ServiceFactory:
    """Factory for creating service instances"""
    
    def __init__(self):
        ConfigValidator.validate_config()
        self.watson_client = WatsonClient()
        self.iam_service = IAMTokenService()
        self.credentials_manager = self.create_credentials_manager()
        
    def create_model_service(self) -> ModelService:
        return ModelService(self.watson_client)
        
    def create_project_service(self) -> ProjectService:
        return ProjectService(self.watson_client, self.iam_service)
        
    def create_text_service(self) -> TextService:
        return TextService(self.watson_client)
        
    def create_credentials_manager(self) -> CredentialsManager:
        return CredentialsManager()

    def create_nlu_service(self) -> NLUService:
        return NLUService(self.credentials_manager)

    def create_tts_service(self) -> TTSService:
        return TTSService(self.credentials_manager)

    def create_stt_service(self) -> STTService:
        return STTService(self.credentials_manager) 