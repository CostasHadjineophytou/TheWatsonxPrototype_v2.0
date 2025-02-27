import pytest
import os
from unittest.mock import patch, mock_open

from backend.validators.service_validator import ServiceValidator
from backend.utils.errors import ValidationError, AuthenticationError
from backend.config.text_config import TextConfig
from backend.config.nlu_config import NLUConfig
from backend.config.speech_config import SpeechConfig


class TestServiceValidator:
    """Tests for the ServiceValidator class"""

    def test_validate_credentials_valid(self):
        """Test validating valid credentials"""
        validator = ServiceValidator()
        credentials = {'api_key': 'test_api_key', 'url': 'https://test-url.com'}
        
        # Should not raise an exception
        validator.validate_credentials(credentials)

    def test_validate_credentials_missing(self):
        """Test validating missing credentials"""
        validator = ServiceValidator()
        
        with pytest.raises(AuthenticationError) as exc_info:
            validator.validate_credentials(None)
        
        assert exc_info.value.code == "NO_CREDENTIALS"
        assert "No credentials provided" in exc_info.value.message

    def test_validate_credentials_no_api_key(self):
        """Test validating credentials without API key"""
        validator = ServiceValidator()
        credentials = {'url': 'https://test-url.com'}
        
        with pytest.raises(AuthenticationError) as exc_info:
            validator.validate_credentials(credentials)
        
        assert exc_info.value.code == "NO_API_KEY"
        assert "API key is required" in exc_info.value.message

    def test_validate_model_id_valid(self):
        """Test validating valid model ID"""
        validator = ServiceValidator()
        model_id = "ibm/granite-20b-multilingual"
        
        # Should not raise an exception
        validator.validate_model_id(model_id)

    def test_validate_model_id_invalid(self):
        """Test validating invalid model ID"""
        validator = ServiceValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_model_id("")
        
        assert exc_info.value.code == "INVALID_MODEL_ID"
        assert "Invalid model ID format" in exc_info.value.message

    def test_validate_project_id_valid(self):
        """Test validating valid project ID"""
        validator = ServiceValidator()
        project_id = "project-id-123"
        
        # Should not raise an exception
        validator.validate_project_id(project_id)

    def test_validate_project_id_invalid(self):
        """Test validating invalid project ID"""
        validator = ServiceValidator()
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_project_id("")
        
        assert exc_info.value.code == "INVALID_PROJECT_ID"
        assert "Invalid project ID format" in exc_info.value.message

    def test_validate_text_params_valid(self):
        """Test validating valid text parameters"""
        validator = ServiceValidator()
        params = TextConfig.DEFAULT_PARAMS.copy()
        
        # Should not raise an exception
        validator.validate_text_params(params)

    def test_validate_text_params_missing(self):
        """Test validating text parameters with missing parameters"""
        validator = ServiceValidator()
        params = {'temperature': 0.7}  # Missing other required params
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_text_params(params)
        
        assert exc_info.value.code == "INVALID_TEXT_PARAMS"
        assert "missing_params" in exc_info.value.details

    def test_validate_text_params_invalid(self):
        """Test validating text parameters with invalid parameters"""
        validator = ServiceValidator()
        params = TextConfig.DEFAULT_PARAMS.copy()
        params['invalid_param'] = 'value'
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_text_params(params)
        
        assert exc_info.value.code == "INVALID_TEXT_PARAMS"
        assert "invalid_params" in exc_info.value.details
        assert "invalid_param" in exc_info.value.details["invalid_params"]

    def test_validate_watson_text_params_valid(self):
        """Test validating valid Watson text parameters"""
        validator = ServiceValidator()
        params = {
            'decoding_method': 'sample',
            'max_new_tokens': 100,
            'temperature': 0.7,
            'top_p': 1.0,
            'top_k': 50,
            'repetition_penalty': 1.0
        }
        
        # Should not raise an exception
        validator.validate_watson_text_params(params)

    def test_validate_watson_text_params_camel_case(self):
        """Test validating Watson text parameters with camelCase names"""
        validator = ServiceValidator()
        params = {
            'decodingMethod': 'sample',
            'maxNewTokens': 100,
            'temperature': 0.7,
            'topP': 1.0,
            'topK': 50,
            'repetitionPenalty': 1.0
        }
        
        # Should not raise an exception
        validator.validate_watson_text_params(params)

    def test_validate_watson_text_params_missing(self):
        """Test validating Watson text parameters with missing parameters"""
        validator = ServiceValidator()
        params = {'temperature': 0.7}  # Missing other required params
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_watson_text_params(params)
        
        assert exc_info.value.code == "MISSING_WATSON_PARAMS"
        assert "missing_params" in exc_info.value.details

    def test_validate_tts_request_valid(self):
        """Test validating valid TTS request"""
        validator = ServiceValidator()
        text = "This is a test text"
        voice = "en-US_MichaelV3Voice"
        params = {'pitch': 0, 'speed': 0}
        
        # Should not raise an exception
        validator.validate_tts_request(text, voice, params)

    def test_validate_tts_request_empty_text(self):
        """Test validating TTS request with empty text"""
        validator = ServiceValidator()
        text = ""
        voice = "en-US_MichaelV3Voice"
        params = {'pitch': 0, 'speed': 0}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_tts_request(text, voice, params)
        
        assert exc_info.value.code == "INVALID_TEXT"
        assert "Invalid text length" in exc_info.value.message

    def test_validate_tts_request_text_too_long(self):
        """Test validating TTS request with text that's too long"""
        validator = ServiceValidator()
        text = "a" * (SpeechConfig.MAX_TEXT_LENGTH + 1)
        voice = "en-US_MichaelV3Voice"
        params = {'pitch': 0, 'speed': 0}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_tts_request(text, voice, params)
        
        assert exc_info.value.code == "INVALID_TEXT"
        assert "Invalid text length" in exc_info.value.message

    def test_validate_tts_request_no_voice(self):
        """Test validating TTS request with no voice"""
        validator = ServiceValidator()
        text = "This is a test text"
        voice = ""
        params = {'pitch': 0, 'speed': 0}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_tts_request(text, voice, params)
        
        assert exc_info.value.code == "INVALID_VOICE"
        assert "Voice must be specified" in exc_info.value.message

    def test_validate_tts_request_invalid_pitch(self):
        """Test validating TTS request with invalid pitch"""
        validator = ServiceValidator()
        text = "This is a test text"
        voice = "en-US_MichaelV3Voice"
        params = {'pitch': SpeechConfig.PITCH_RANGE[1] + 1, 'speed': 0}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_tts_request(text, voice, params)
        
        assert exc_info.value.code == "INVALID_PITCH"
        assert "Invalid pitch value" in exc_info.value.message

    def test_validate_tts_request_invalid_speed(self):
        """Test validating TTS request with invalid speed"""
        validator = ServiceValidator()
        text = "This is a test text"
        voice = "en-US_MichaelV3Voice"
        params = {'pitch': 0, 'speed': SpeechConfig.SPEED_RANGE[1] + 1}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_tts_request(text, voice, params)
        
        assert exc_info.value.code == "INVALID_SPEED"
        assert "Invalid speed value" in exc_info.value.message

    def test_validate_audio_file_exists(self):
        """Test validating an audio file that exists"""
        validator = ServiceValidator()
        
        # Mock os.path.exists and os.path.getsize
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1000):
            # Should not raise an exception
            validator.validate_audio_file("test_file.wav")

    def test_validate_audio_file_not_found(self):
        """Test validating an audio file that doesn't exist"""
        validator = ServiceValidator()
        
        # Mock os.path.exists
        with patch('os.path.exists', return_value=False):
            with pytest.raises(ValidationError) as exc_info:
                validator.validate_audio_file("nonexistent_file.wav")
            
            assert exc_info.value.code == "FILE_NOT_FOUND"
            assert "Audio file not found" in exc_info.value.message

    def test_validate_audio_file_too_large(self):
        """Test validating an audio file that's too large"""
        validator = ServiceValidator()
        
        # Mock os.path.exists and os.path.getsize
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=SpeechConfig.MAX_AUDIO_SIZE + 1):
            with pytest.raises(ValidationError) as exc_info:
                validator.validate_audio_file("large_file.wav")
            
            assert exc_info.value.code == "FILE_TOO_LARGE"
            assert "File too large for API" in exc_info.value.message

    def test_validate_nlu_features_valid(self):
        """Test validating valid NLU features"""
        validator = ServiceValidator()
        features = {
            'sentiment': {},
            'entities': {'sentiment': True}
        }
        
        # Should not raise an exception
        validator.validate_nlu_features(features)

    def test_validate_nlu_features_invalid_feature(self):
        """Test validating NLU features with invalid feature"""
        validator = ServiceValidator()
        features = {
            'sentiment': {},
            'invalid_feature': {}
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_features(features)
        
        assert exc_info.value.code == "INVALID_NLU_FEATURES"
        assert "invalid_features" in exc_info.value.details
        assert "invalid_feature" in exc_info.value.details["invalid_features"]

    def test_validate_nlu_features_invalid_params(self):
        """Test validating NLU features with invalid parameters"""
        validator = ServiceValidator()
        features = {
            'sentiment': {'invalid_param': True}
        }
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_features(features)
        
        assert exc_info.value.code == "INVALID_FEATURE_PARAMS"
        assert "invalid_params" in exc_info.value.details
        assert "invalid_param" in exc_info.value.details["invalid_params"]

    def test_validate_nlu_request_valid(self):
        """Test validating valid NLU request"""
        validator = ServiceValidator()
        text = "This is a test text"
        features = {'sentiment': {}}
        
        # Should not raise an exception
        validator.validate_nlu_request(text, features)

    def test_validate_nlu_request_invalid_text_type(self):
        """Test validating NLU request with invalid text type"""
        validator = ServiceValidator()
        text = 123  # Not a string
        features = {'sentiment': {}}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_request(text, features)
        
        assert exc_info.value.code == "INVALID_TEXT_TYPE"
        assert "Text must be a string" in exc_info.value.message

    def test_validate_nlu_request_empty_text(self):
        """Test validating NLU request with empty text"""
        validator = ServiceValidator()
        text = ""
        features = {'sentiment': {}}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_request(text, features)
        
        assert exc_info.value.code == "EMPTY_TEXT"
        assert "Text cannot be empty" in exc_info.value.message

    def test_validate_nlu_request_invalid_features_type(self):
        """Test validating NLU request with invalid features type"""
        validator = ServiceValidator()
        text = "This is a test text"
        features = "not a dict"
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_request(text, features)
        
        assert exc_info.value.code == "INVALID_FEATURES_TYPE"
        assert "Features must be a dictionary" in exc_info.value.message

    def test_validate_nlu_request_invalid_features(self):
        """Test validating NLU request with invalid features"""
        validator = ServiceValidator()
        text = "This is a test text"
        features = {'invalid_feature': {}}
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_nlu_request(text, features)
        
        assert exc_info.value.code == "INVALID_FEATURES"
        assert "Invalid features" in exc_info.value.message 