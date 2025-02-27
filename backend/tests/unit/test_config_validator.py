import pytest
from unittest.mock import patch, MagicMock, call

from backend.validators.config_validator import ConfigValidator
from backend.utils.errors import ConfigurationError


class TestConfigValidator:
    """Tests for the ConfigValidator class"""

    def test_init(self):
        """Test initializing the ConfigValidator"""
        validator = ConfigValidator()
        
        # No assertions needed, just checking it initializes without error

    def test_validate_config_valid(self, mock_config):
        """Test validating a valid configuration"""
        # Mock the config with valid values
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        mock_config.STT_API_KEY = "stt_api_key"
        mock_config.STT_URL = "https://stt-url.com"
        mock_config.UPLOAD_FOLDER = "/path/to/uploads"
        mock_config.ALLOWED_EXTENSIONS = {"wav", "mp3"}
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method
        # Should not raise an exception
        validator.validate_config(mock_config)

    def test_validate_config_missing_watson_api_key(self, mock_config):
        """Test validating config with missing Watson API key"""
        # Mock the config with missing Watson API key
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "WATSON_API_KEY" in exc_info.value.message

    def test_validate_config_missing_watson_url(self, mock_config):
        """Test validating config with missing Watson URL"""
        # Mock the config with missing Watson URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "WATSON_URL" in exc_info.value.message

    def test_validate_config_missing_nlu_api_key(self, mock_config):
        """Test validating config with missing NLU API key"""
        # Mock the config with missing NLU API key
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = ""
        mock_config.NLU_URL = "https://nlu-url.com"
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "NLU_API_KEY" in exc_info.value.message

    def test_validate_config_missing_nlu_url(self, mock_config):
        """Test validating config with missing NLU URL"""
        # Mock the config with missing NLU URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "NLU_URL" in exc_info.value.message

    def test_validate_config_missing_speech_api_key(self, mock_config):
        """Test validating config with missing Speech API key"""
        # Mock the config with missing Speech API key
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = ""
        mock_config.SPEECH_URL = "https://speech-url.com"
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "SPEECH_API_KEY" in exc_info.value.message

    def test_validate_config_missing_speech_url(self, mock_config):
        """Test validating config with missing Speech URL"""
        # Mock the config with missing Speech URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "SPEECH_URL" in exc_info.value.message

    def test_validate_config_missing_tts_api_key(self, mock_config):
        """Test validating config with missing TTS API key"""
        # Mock the config with missing TTS API key
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = ""
        mock_config.TTS_URL = "https://tts-url.com"
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "TTS_API_KEY" in exc_info.value.message

    def test_validate_config_missing_tts_url(self, mock_config):
        """Test validating config with missing TTS URL"""
        # Mock the config with missing TTS URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "TTS_URL" in exc_info.value.message

    def test_validate_config_missing_stt_api_key(self, mock_config):
        """Test validating config with missing STT API key"""
        # Mock the config with missing STT API key
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        mock_config.STT_API_KEY = ""
        mock_config.STT_URL = "https://stt-url.com"
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "STT_API_KEY" in exc_info.value.message

    def test_validate_config_missing_stt_url(self, mock_config):
        """Test validating config with missing STT URL"""
        # Mock the config with missing STT URL
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        mock_config.STT_API_KEY = "stt_api_key"
        mock_config.STT_URL = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "STT_URL" in exc_info.value.message

    def test_validate_config_missing_upload_folder(self, mock_config):
        """Test validating config with missing upload folder"""
        # Mock the config with missing upload folder
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        mock_config.STT_API_KEY = "stt_api_key"
        mock_config.STT_URL = "https://stt-url.com"
        mock_config.UPLOAD_FOLDER = ""
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "UPLOAD_FOLDER" in exc_info.value.message

    def test_validate_config_missing_allowed_extensions(self, mock_config):
        """Test validating config with missing allowed extensions"""
        # Mock the config with missing allowed extensions
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        mock_config.NLU_API_KEY = "nlu_api_key"
        mock_config.NLU_URL = "https://nlu-url.com"
        mock_config.SPEECH_API_KEY = "speech_api_key"
        mock_config.SPEECH_URL = "https://speech-url.com"
        mock_config.TTS_API_KEY = "tts_api_key"
        mock_config.TTS_URL = "https://tts-url.com"
        mock_config.STT_API_KEY = "stt_api_key"
        mock_config.STT_URL = "https://stt-url.com"
        mock_config.UPLOAD_FOLDER = "/path/to/uploads"
        mock_config.ALLOWED_EXTENSIONS = set()  # Empty set
        
        # Create the validator
        validator = ConfigValidator()
        
        # Call the method and expect exception
        with pytest.raises(ConfigurationError) as exc_info:
            validator.validate_config(mock_config)
        
        assert exc_info.value.code == "MISSING_CONFIG"
        assert "ALLOWED_EXTENSIONS" in exc_info.value.message

    def test_validate_config_from_env_vars(self, mock_config):
        """Test validating config with values from environment variables"""
        # Mock the config with empty values
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = ""
        mock_config.NLU_API_KEY = ""
        mock_config.NLU_URL = ""
        mock_config.SPEECH_API_KEY = ""
        mock_config.SPEECH_URL = ""
        mock_config.TTS_API_KEY = ""
        mock_config.TTS_URL = ""
        mock_config.STT_API_KEY = ""
        mock_config.STT_URL = ""
        mock_config.UPLOAD_FOLDER = ""
        mock_config.ALLOWED_EXTENSIONS = set()
        
        # Mock os.environ with valid values
        with patch('os.environ', {
            'WATSON_API_KEY': 'env_api_key',
            'WATSON_URL': 'https://env-url.com',
            'NLU_API_KEY': 'env_nlu_api_key',
            'NLU_URL': 'https://env-nlu-url.com',
            'SPEECH_API_KEY': 'env_speech_api_key',
            'SPEECH_URL': 'https://env-speech-url.com',
            'TTS_API_KEY': 'env_tts_api_key',
            'TTS_URL': 'https://env-tts-url.com',
            'STT_API_KEY': 'env_stt_api_key',
            'STT_URL': 'https://env-stt-url.com',
            'UPLOAD_FOLDER': '/env/path/to/uploads',
            'ALLOWED_EXTENSIONS': 'wav,mp3'
        }):
            # Create the validator
            validator = ConfigValidator()
            
            # Call the method
            # Should not raise an exception
            validator.validate_config(mock_config)

    def test_validate_config_missing_all(self, mock_config):
        """Test validating config with all values missing"""
        # Mock the config with all empty values
        mock_config.WATSON_API_KEY = ""
        mock_config.WATSON_URL = ""
        mock_config.NLU_API_KEY = ""
        mock_config.NLU_URL = ""
        mock_config.SPEECH_API_KEY = ""
        mock_config.SPEECH_URL = ""
        mock_config.TTS_API_KEY = ""
        mock_config.TTS_URL = ""
        mock_config.STT_API_KEY = ""
        mock_config.STT_URL = ""
        mock_config.UPLOAD_FOLDER = ""
        mock_config.ALLOWED_EXTENSIONS = set()
        
        # Mock os.environ with empty values
        with patch('os.environ', {}):
            # Create the validator
            validator = ConfigValidator()
            
            # Call the method and expect exception
            with pytest.raises(ConfigurationError) as exc_info:
                validator.validate_config(mock_config)
            
            assert exc_info.value.code == "MISSING_CONFIG"
            assert "Multiple configuration values are missing" in exc_info.value.message 