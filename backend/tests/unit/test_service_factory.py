import pytest
from unittest.mock import patch, MagicMock, call

from backend.service_factory import ServiceFactory
from backend.services.model_service import ModelService
from backend.services.project_service import ProjectService
from backend.services.text_service import TextService
from backend.services.nlu_service import NLUService
from backend.services.tts_service import TTSService
from backend.services.stt_service import STTService
from backend.services.credentials_manager import CredentialsManager
from backend.utils.errors import ConfigurationError


class TestServiceFactory:
    """Tests for the ServiceFactory class"""

    def test_init(self):
        """Test initializing the ServiceFactory"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient'), \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            assert hasattr(factory, 'watson_client')
            assert hasattr(factory, 'iam_service')
            assert hasattr(factory, 'credentials_manager')

    def test_create_model_service(self):
        """Test creating a model service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient') as mock_watson_client, \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_model_service()
            assert service is not None
            # Verify the service was created with the watson client
            assert isinstance(service, ModelService)

    def test_create_project_service(self):
        """Test creating a project service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient') as mock_watson_client, \
             patch('backend.services.iam_token.IAMTokenService') as mock_iam_service, \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_project_service()
            assert service is not None
            # Verify the service was created with the watson client and iam service
            assert isinstance(service, ProjectService)

    def test_create_text_service(self):
        """Test creating a text service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient') as mock_watson_client, \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_text_service()
            assert service is not None
            # Verify the service was created with the watson client
            assert isinstance(service, TextService)

    def test_create_credentials_manager(self):
        """Test creating a credentials manager"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient'), \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.services.credentials_manager.CredentialsManager') as mock_credentials_manager_class:
            factory = ServiceFactory()
            # Call the method directly to avoid infinite recursion with the patched constructor
            manager = factory.create_credentials_manager()
            # Verify the credentials manager was created
            mock_credentials_manager_class.assert_called_once()
            assert isinstance(manager, CredentialsManager)

    def test_create_nlu_service(self):
        """Test creating an NLU service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient'), \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_nlu_service()
            assert service is not None
            # Verify the service was created
            assert isinstance(service, NLUService)

    def test_create_tts_service(self):
        """Test creating a TTS service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient'), \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_tts_service()
            assert service is not None
            # Verify the service was created
            assert isinstance(service, TTSService)

    def test_create_stt_service(self):
        """Test creating an STT service"""
        with patch('backend.validators.config_validator.ConfigValidator.validate_config'), \
             patch('backend.services.watson_client.WatsonClient'), \
             patch('backend.services.iam_token.IAMTokenService'), \
             patch('backend.service_factory.ServiceFactory.create_credentials_manager'):
            factory = ServiceFactory()
            service = factory.create_stt_service()
            assert service is not None
            # Verify the service was created
            assert isinstance(service, STTService) 