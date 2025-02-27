import pytest
from unittest.mock import patch, MagicMock

from backend.utils.base_handler import BaseHandler
from backend.utils.errors import (
    BackendError, APIError, AuthenticationError
)


class TestBaseHandler:
    """Tests for the BaseHandler class"""
    
    def test_init(self):
        """Test initializing the BaseHandler"""
        handler = BaseHandler()
        
        # Check that validator is initialized
        assert hasattr(handler, 'validator')
    
    @patch('backend.utils.error_handling.handle_api_error')
    @patch('logging.error')
    def test_handle_error_standard_exception(self, mock_logging, mock_handle_api_error):
        """Test handling a standard exception"""
        # Setup
        handler = BaseHandler()
        error = Exception("Test error")
        context = "Test context"
        
        # Mock the handle_api_error function
        mock_api_error = APIError("API error", "API_ERROR")
        mock_handle_api_error.return_value = mock_api_error
        
        # Call the method
        result = handler.handle_error(error, context)
        
        # Assertions
        mock_logging.assert_called_once_with(f"{context}: {str(error)}")
        mock_handle_api_error.assert_called_once_with(error)
        assert result == mock_api_error
    
    @patch('backend.utils.error_handling.handle_api_error')
    @patch('logging.error')
    def test_handle_error_without_context(self, mock_logging, mock_handle_api_error):
        """Test handling an error without context"""
        # Setup
        handler = BaseHandler()
        error = Exception("Test error")
        
        # Mock the handle_api_error function
        mock_api_error = APIError("API error", "API_ERROR")
        mock_handle_api_error.return_value = mock_api_error
        
        # Call the method
        result = handler.handle_error(error)
        
        # Assertions
        mock_logging.assert_called_once_with(f"Error: {str(error)}")
        mock_handle_api_error.assert_called_once_with(error)
        assert result == mock_api_error
    
    @patch('backend.utils.error_handling.handle_api_error')
    @patch('logging.error')
    def test_handle_error_backend_error(self, mock_logging, mock_handle_api_error):
        """Test handling a BackendError"""
        # Setup
        handler = BaseHandler()
        error = AuthenticationError("Auth error", "AUTH_ERROR")
        context = "Test context"
        
        # Call the method
        result = handler.handle_error(error, context)
        
        # Assertions
        mock_logging.assert_called_once_with(f"{context}: {str(error)}")
        # handle_api_error should not be called for BackendError instances
        mock_handle_api_error.assert_not_called()
        # The original error should be returned
        assert result == error
    
    @patch('backend.validators.service_validator.ServiceValidator')
    def test_validator_initialization(self, mock_validator_class):
        """Test that the validator is properly initialized"""
        # Setup
        mock_validator = MagicMock()
        mock_validator_class.return_value = mock_validator
        
        # Create the handler
        handler = BaseHandler()
        
        # Assertions
        assert handler.validator == mock_validator 