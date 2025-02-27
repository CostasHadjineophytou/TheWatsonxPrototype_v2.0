import pytest
from unittest.mock import patch, MagicMock, call

from backend.services.credentials_manager import CredentialsManager
from backend.utils.errors import ConfigurationError


class TestCredentialsManager:
    """Tests for the CredentialsManager class"""

    def test_init(self, mock_config):
        """Test initializing the CredentialsManager"""
        manager = CredentialsManager(mock_config)
        
        assert manager.config == mock_config

    def test_get_service_credentials_valid(self, mock_config):
        """Test getting valid service credentials"""
        # Mock the config to return valid credentials
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method
        credentials = manager.get_service_credentials("watson")
        
        # Assertions
        assert credentials == {
            'api_key': 'test_api_key',
            'url': 'https://test-url.com'
        }

    def test_get_service_credentials_invalid_service(self, mock_config):
        """Test getting credentials for an invalid service"""
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            manager.get_service_credentials("invalid_service")
        
        assert exc_info.value.code == "INVALID_SERVICE"
        assert "Invalid service name" in exc_info.value.message

    def test_get_service_credentials_missing_api_key(self, mock_config):
        """Test getting credentials with missing API key"""
        # Mock the config with missing API key
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            manager.get_service_credentials("watson")
        
        assert exc_info.value.code == "MISSING_API_KEY"
        assert "API key not configured" in exc_info.value.message

    def test_get_service_credentials_missing_url(self, mock_config):
        """Test getting credentials with missing URL"""
        # Mock the config with missing URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = ""
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            manager.get_service_credentials("watson")
        
        assert exc_info.value.code == "MISSING_URL"
        assert "Service URL not configured" in exc_info.value.message

    def test_get_service_credentials_nlu(self, mock_config):
        """Test getting NLU service credentials"""
        # Mock the config to return valid NLU credentials
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method
        credentials = manager.get_service_credentials("nlu")
        
        # Assertions
        assert credentials == {
            'api_key': 'nlu_api_key',
            'url': 'https://nlu-url.com'
        }

    def test_get_service_credentials_speech(self, mock_config):
        """Test getting speech service credentials"""
        # Mock the config to return valid speech credentials
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method
        credentials = manager.get_service_credentials("speech")
        
        # Assertions
        assert credentials == {
            'api_key': 'speech_api_key',
            'url': 'https://speech-url.com'
        }

    def test_get_service_credentials_tts(self, mock_config):
        """Test getting TTS service credentials"""
        # Mock the config to return valid TTS credentials
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method
        credentials = manager.get_service_credentials("tts")
        
        # Assertions
        assert credentials == {
            'api_key': 'tts_api_key',
            'url': 'https://tts-url.com'
        }

    def test_get_service_credentials_stt(self, mock_config):
        """Test getting STT service credentials"""
        # Mock the config to return valid STT credentials
        mock_config.STT_API_KEY = "stt_api_key"
        mock_config.STT_URL = "https://stt-url.com"
        
        # Create the manager
        manager = CredentialsManager(mock_config)
        
        # Call the method
        credentials = manager.get_service_credentials("stt")
        
        # Assertions
        assert credentials == {
            'api_key': 'stt_api_key',
            'url': 'https://stt-url.com'
        }

    def test_get_service_credentials_env_vars(self, mock_config):
        """Test getting credentials from environment variables"""
        # Mock the config to return empty values (should fall back to env vars)
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = ""
        
        # Mock os.environ to return values
        with patch('os.environ', {
            'WATSON_API_KEY': 'env_api_key',
            'WATSON_URL': 'https://env-url.com'
        }):
            # Create the manager
            manager = CredentialsManager(mock_config)
            
            # Call the method
            credentials = manager.get_service_credentials("watson")
            
            # Assertions
            assert credentials == {
                'api_key': 'env_api_key',
                'url': 'https://env-url.com'
            }

    def test_get_service_credentials_missing_env_vars(self, mock_config):
        """Test getting credentials with missing config and env vars"""
        # Mock the config to return empty values
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Mock os.environ to return empty values
        with patch('os.environ', {}):
            # Create the manager
            manager = CredentialsManager(mock_config)
            
            # Call the method and expect exception
            with pytest.raises(ConfigurationError) as exc_info:
                manager.get_service_credentials("watson")
            
            assert exc_info.value.code == "MISSING_API_KEY"
            assert "API key not configured" in exc_info.value.message 