from typing import Optional
from backend.service_factory import ServiceFactory
from logic.managers.model_manager import ModelManager
from logic.managers.project_manager import ProjectManager
from logic.managers.text_manager import TextManager
from logic.utils.file_manager import FileManager
from logic.validators import ModelValidator, ProjectValidator, TextValidator

class ManagerFactory:
    """Factory for creating manager instances"""
    _instance: Optional['ManagerFactory'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.service_factory = ServiceFactory()
            # Create validators
            cls._instance.model_validator = ModelValidator()
            cls._instance.project_validator = ProjectValidator()
            cls._instance.text_validator = TextValidator()
        return cls._instance

    def create_model_manager(self) -> ModelManager:
        service = self.service_factory.create_model_service()
        return ModelManager(service, self.model_validator)
        
    def create_project_manager(self) -> ProjectManager:
        service = self.service_factory.create_project_service()
        return ProjectManager(service, self.project_validator)
        
    def create_text_manager(self) -> TextManager:
        service = self.service_factory.create_text_service()
        return TextManager(service, self.text_validator) 