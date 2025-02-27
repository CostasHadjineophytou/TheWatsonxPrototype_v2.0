import pytest
from unittest.mock import patch, MagicMock

from backend.utils.error_handling import handle_api_error
from backend.utils.errors import (
    BackendError, APIError, AuthenticationError, 
    ServiceError, ConfigurationError
)


class TestErrorHandling:
    """Tests for the error_handling module"""
    
    def test_handle_api_error_authentication(self):
        """Test handling authentication errors"""
        error = Exception("Authentication failed for API request")
        result = handle_api_error(error)
        
        assert isinstance(result, AuthenticationError)
        assert result.code == "AUTH_ERROR"
        assert str(error) in result.message
    
    def test_handle_api_error_configuration(self):
        """Test handling configuration errors"""
        error = Exception("Configuration is missing required fields")
        result = handle_api_error(error)
        
        assert isinstance(result, ConfigurationError)
        assert result.code == "CONFIG_ERROR"
        assert str(error) in result.message
    
    def test_handle_api_error_not_found(self):
        """Test handling not found errors"""
        error = Exception("Resource not found: model_id=123")
        result = handle_api_error(error)
        
        assert isinstance(result, APIError)
        assert result.code == "NOT_FOUND"
        assert str(error) in result.message
    
    def test_handle_api_error_rate_limit(self):
        """Test handling rate limit errors"""
        error = Exception("Rate limit exceeded for this API key")
        result = handle_api_error(error)
        
        assert isinstance(result, ServiceError)
        assert result.code == "RATE_LIMIT"
        assert str(error) in result.message
    
    def test_handle_api_error_generic(self):
        """Test handling generic API errors"""
        error = Exception("Unknown API error occurred")
        result = handle_api_error(error)
        
        assert isinstance(result, APIError)
        assert result.code == "API_ERROR"
        assert str(error) in result.message
    
    def test_handle_api_error_case_insensitive(self):
        """Test that error handling is case insensitive"""
        error = Exception("AUTHENTICATION failed")
        result = handle_api_error(error)
        
        assert isinstance(result, AuthenticationError)
        assert result.code == "AUTH_ERROR"
        
    def test_handle_api_error_with_details(self):
        """Test handling errors with additional details in the message"""
        error = Exception("Authentication failed: Invalid API key provided (key=***)")
        result = handle_api_error(error)
        
        assert isinstance(result, AuthenticationError)
        assert result.code == "AUTH_ERROR"
        assert str(error) in result.message 