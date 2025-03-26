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
import logging

class ManagerFactory:
    """Factory for creating manager instances"""
    _instance: Optional['ManagerFactory'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.service_factory = ServiceFactory()
            except Exception as e:
                logging.warning(f"Failed to initialize ServiceFactory: {str(e)}")
                cls._instance.service_factory = None
            
            # Create validators
            cls._instance.model_validator = ModelValidator()
            cls._instance.project_validator = ProjectValidator()
            cls._instance.text_validator = TextValidator()
            cls._instance.speech_validator = SpeechValidator()
            cls._instance.nlu_validator = NLUValidator()
        return cls._instance
    
    def create_model_manager(self) -> ModelManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_model_service()
                return ModelManager(service, self.model_validator)
        except Exception as e:
            logging.warning(f"Failed to create model service: {str(e)}")
        return ModelManager(None, self.model_validator)
        
    def create_project_manager(self) -> ProjectManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_project_service()
                return ProjectManager(service, self.project_validator)
        except Exception as e:
            logging.warning(f"Failed to create project service: {str(e)}")
        return ProjectManager(None, self.project_validator)
        
    def create_text_manager(self) -> TextManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_text_service()
                return TextManager(service, self.text_validator)
        except Exception as e:
            logging.warning(f"Failed to create text service: {str(e)}")
        return TextManager(None, self.text_validator)

    def create_nlu_manager(self) -> NLUManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_nlu_service()
                return NLUManager(service, self.nlu_validator)
        except Exception as e:
            logging.warning(f"Failed to create NLU service: {str(e)}")
        return NLUManager(None, self.nlu_validator)

    def create_tts_manager(self) -> TTSManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_tts_service()
                return TTSManager(service, self.speech_validator)
        except Exception as e:
            logging.warning(f"Failed to create TTS service: {str(e)}")
        return TTSManager(None, self.speech_validator)

    def create_stt_manager(self) -> STTManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_stt_service()
                return STTManager(service, self.speech_validator)
        except Exception as e:
            logging.warning(f"Failed to create STT service: {str(e)}")
        return STTManager(None, self.speech_validator)

    def create_audio_manager(self) -> AudioManager:
        return AudioManager()
        
    def create_service_checker(self) -> ServiceCheckerManager:
        try:
            if self.service_factory:
                service = self.service_factory.create_service_checker_service()
                return ServiceCheckerManager(service)
        except Exception as e:
            logging.warning(f"Failed to create service checker: {str(e)}")
        return ServiceCheckerManager(None) 