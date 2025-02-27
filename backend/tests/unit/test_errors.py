import pytest
from backend.utils.errors import (
    BackendError, 
    APIError, 
    AuthenticationError, 
    ServiceError, 
    ValidationError, 
    ConfigurationError, 
    FileError,
    AudioError
)


class TestErrors:
    """Tests for the error classes in the backend.utils.errors module"""
    
    def test_backend_error_init(self):
        """Test initializing the base BackendError class"""
        message = "Test error message"
        code = "TEST_ERROR"
        details = {"key": "value"}
        
        error = BackendError(message, code, details)
        
        assert error.message == message
        assert error.code == code
        assert error.details == details
        assert str(error) == message
    
    def test_backend_error_without_details(self):
        """Test initializing BackendError without details"""
        message = "Test error message"
        code = "TEST_ERROR"
        
        error = BackendError(message, code)
        
        assert error.message == message
        assert error.code == code
        assert error.details is None
    
    def test_api_error(self):
        """Test APIError class"""
        message = "API error"
        code = "API_ERROR"
        details = {"status_code": 500}
        
        error = APIError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_authentication_error(self):
        """Test AuthenticationError class"""
        message = "Authentication failed"
        code = "AUTH_ERROR"
        details = {"reason": "Invalid token"}
        
        error = AuthenticationError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_service_error(self):
        """Test ServiceError class"""
        message = "Service unavailable"
        code = "SERVICE_ERROR"
        details = {"service": "text"}
        
        error = ServiceError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_validation_error(self):
        """Test ValidationError class"""
        message = "Invalid input"
        code = "VALIDATION_ERROR"
        details = {"field": "model_id", "reason": "Required field missing"}
        
        error = ValidationError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_configuration_error(self):
        """Test ConfigurationError class"""
        message = "Missing configuration"
        code = "CONFIG_ERROR"
        details = {"missing": ["API_KEY"]}
        
        error = ConfigurationError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_file_error(self):
        """Test FileError class"""
        message = "File not found"
        code = "FILE_ERROR"
        details = {"path": "/path/to/file.json"}
        
        error = FileError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_audio_error(self):
        """Test AudioError class"""
        message = "Audio playback failed"
        code = "AUDIO_ERROR"
        details = {"file": "output.wav"}
        
        error = AudioError(message, code, details)
        
        assert isinstance(error, BackendError)
        assert error.message == message
        assert error.code == code
        assert error.details == details
    
    def test_error_inheritance(self):
        """Test that all error classes inherit from BackendError"""
        error_classes = [
            APIError,
            AuthenticationError,
            ServiceError,
            ValidationError,
            ConfigurationError,
            FileError,
            AudioError
        ]
        
        for error_class in error_classes:
            assert issubclass(error_class, BackendError)
            
            # Create an instance and check it's a BackendError
            instance = error_class("Test", "TEST")
            assert isinstance(instance, BackendError) 