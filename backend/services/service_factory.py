from backend.services.watson_client import WatsonClient
from backend.services.iam_token import IAMTokenService
from backend.services.model_service import ModelService
from backend.services.project_service import ProjectService
from backend.services.text_service import TextService
from backend.services.credentials_manager import CredentialsManager

class ServiceFactory:
    """Factory for creating service instances"""
    
    def __init__(self):
        self.watson_client = WatsonClient()
        self.iam_service = IAMTokenService()
        
    def create_model_service(self) -> ModelService:
        return ModelService(self.watson_client)
        
    def create_project_service(self) -> ProjectService:
        return ProjectService(self.watson_client, self.iam_service)
        
    def create_text_service(self) -> TextService:
        return TextService(self.watson_client)
        
    def create_credentials_manager(self) -> CredentialsManager:
        return CredentialsManager() 