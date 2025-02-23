from typing import Optional
from backend.services.service_factory import ServiceFactory
from logic.managers.model_manager import ModelManager
from logic.managers.project_manager import ProjectManager
from logic.managers.text_manager import TextManager

class ManagerFactory:
    """Factory for creating manager instances"""
    _instance: Optional['ManagerFactory'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.service_factory = ServiceFactory()
        return cls._instance

    def create_model_manager(self) -> ModelManager:
        return ModelManager(self.service_factory.create_model_service())
        
    def create_project_manager(self) -> ProjectManager:
        return ProjectManager(self.service_factory.create_project_service())
        
    def create_text_manager(self) -> TextManager:
        return TextManager(self.service_factory.create_text_service()) 