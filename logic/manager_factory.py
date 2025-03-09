from typing import Optional
from backend.service_factory import ServiceFactory
from logic.managers.model_manager import ModelManager
from logic.managers.project_manager import ProjectManager
from logic.managers.text_manager import TextManager
from logic.managers.tts_manager import TTSManager
from logic.managers.stt_manager import STTManager
from logic.managers.nlu_manager import NLUManager
from logic.managers.service_checker_manager import ServiceCheckerManager
from logic.validators import (
    ModelValidator, 
    ProjectValidator, 
    TextValidator,
    SpeechValidator,
    NLUValidator
)
from backend.utils.audio_player import AudioPlayer
from logic.managers.audio_manager import AudioManager

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
            cls._instance.speech_validator = SpeechValidator()
            cls._instance.nlu_validator = NLUValidator()
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

    def create_nlu_manager(self) -> NLUManager:
        nlu_service = self.service_factory.create_nlu_service()
        return NLUManager(nlu_service, self.nlu_validator)

    def create_tts_manager(self) -> TTSManager:
        tts_service = self.service_factory.create_tts_service()
        return TTSManager(tts_service, self.speech_validator)

    def create_stt_manager(self) -> STTManager:
        stt_service = self.service_factory.create_stt_service()
        return STTManager(stt_service, self.speech_validator)

    def create_audio_manager(self) -> AudioManager:
        return AudioManager()
        
    def create_service_checker(self) -> ServiceCheckerManager:
        service = self.service_factory.create_service_checker_service()
        return ServiceCheckerManager(service) 