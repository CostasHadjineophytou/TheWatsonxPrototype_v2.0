import pytest
from unittest.mock import patch, MagicMock, create_autospec

from backend.services.watson_client import WatsonClient
from backend.utils.errors import AuthenticationError, APIError, ValidationError
from backend.config.config import Config
from backend.validators.service_validator import ServiceValidator


class TestWatsonClient:
    """Tests for the WatsonClient class"""

    @pytest.fixture
    def mock_validator(self):
        """Create a mock validator"""
        validator = create_autospec(ServiceValidator, instance=True)
        return validator

    @pytest.fixture
    def mock_handle_error(self):
        """Create a mock handle_error method"""
        def _handle_error(error, message):
            return APIError(message, str(error))
        return MagicMock(side_effect=_handle_error)

    @pytest.fixture
    def mock_watson_client(self, mock_validator, mock_handle_error):
        """Create a mock Watson client for testing"""
        with patch('backend.utils.base_handler.BaseHandler.__init__', return_value=None):
            # Create the client
            client = WatsonClient()
            
            # Set up the client's mock attributes
            client.credentials = MagicMock()
            client.client = MagicMock()
            client.validator = mock_validator
            client.handle_error = mock_handle_error
            
            return client

    def test_init_success(self):
        """Test successful initialization of WatsonClient"""
        mock_validator = create_autospec(ServiceValidator, instance=True)
        mock_handle_error = MagicMock()
        
        with patch('backend.utils.base_handler.ServiceValidator', return_value=mock_validator) as mock_validator_class, \
             patch('backend.services.watson_client.Credentials') as mock_credentials, \
             patch('backend.services.watson_client.APIClient') as mock_api_client, \
             patch.object(WatsonClient, 'handle_error', mock_handle_error):
            
            # Create mock credentials object
            mock_creds_instance = MagicMock()
            mock_credentials.return_value = mock_creds_instance
            
            # Create mock API client
            mock_api_instance = MagicMock()
            mock_api_client.return_value = mock_api_instance
            
            # Initialize the client
            client = WatsonClient()
            
            # Verify ServiceValidator was created
            mock_validator_class.assert_called_once()
            
            # Verify validate_credentials was called with correct parameters
            mock_validator.validate_credentials.assert_called_once_with({
                'api_key': Config.IBM_CLOUD_API_KEY,
                'url': Config.IBM_CLOUD_MODELS_URL
            })
            
            # Verify Credentials was created with correct parameters
            mock_credentials.assert_called_once_with(
                url=Config.IBM_CLOUD_MODELS_URL,
                api_key=Config.IBM_CLOUD_API_KEY
            )
            
            # Verify APIClient was created with the credentials
            mock_api_client.assert_called_once_with(mock_creds_instance)
            
            # Verify client attributes
            assert client.credentials == mock_creds_instance
            assert client.client == mock_api_instance
            
            # Verify handle_error was not called
            mock_handle_error.assert_not_called()

    def test_init_validation_error(self):
        """Test initialization with validation error"""
        mock_validator = create_autospec(ServiceValidator, instance=True)
        mock_validator.validate_credentials.side_effect = ValidationError(
            "Invalid credentials", "INVALID_CREDENTIALS"
        )
        mock_handle_error = MagicMock()
        
        with patch('backend.utils.base_handler.ServiceValidator', return_value=mock_validator), \
             patch.object(WatsonClient, 'handle_error', mock_handle_error):
            
            with pytest.raises(ValidationError) as exc_info:
                WatsonClient()
            
            assert exc_info.value.code == "INVALID_CREDENTIALS"
            assert "Invalid credentials" in str(exc_info.value)
            
            # Verify validate_credentials was called
            mock_validator.validate_credentials.assert_called_once_with({
                'api_key': Config.IBM_CLOUD_API_KEY,
                'url': Config.IBM_CLOUD_MODELS_URL
            })
            
            # Verify handle_error was not called
            mock_handle_error.assert_not_called()

    def test_init_api_client_error(self):
        """Test initialization with API client error"""
        mock_validator = create_autospec(ServiceValidator, instance=True)
        mock_handle_error = MagicMock(return_value=APIError(
            "Failed to initialize Watson client", "API_CLIENT_ERROR"
        ))
        
        with patch('backend.utils.base_handler.ServiceValidator', return_value=mock_validator), \
             patch('backend.services.watson_client.Credentials') as mock_credentials, \
             patch('backend.services.watson_client.APIClient') as mock_api_client, \
             patch.object(WatsonClient, 'handle_error', mock_handle_error):
            
            # Create mock credentials object
            mock_creds_instance = MagicMock()
            mock_credentials.return_value = mock_creds_instance
            
            # Make APIClient raise an exception
            mock_api_client.side_effect = Exception("API client error")
            
            with pytest.raises(APIError) as exc_info:
                WatsonClient()
            
            assert "Failed to initialize Watson client" in str(exc_info.value)
            mock_handle_error.assert_called_once_with(
                mock_api_client.side_effect,
                "Failed to initialize Watson client"
            )

    def test_init_generic_error(self):
        """Test initialization with a generic error"""
        mock_validator = create_autospec(ServiceValidator, instance=True)
        mock_handle_error = MagicMock(return_value=APIError(
            "Failed to initialize Watson client", "INIT_ERROR"
        ))
        
        with patch('backend.utils.base_handler.BaseHandler.__init__', side_effect=Exception("Generic error")) as mock_base_init, \
             patch('backend.utils.base_handler.ServiceValidator', return_value=mock_validator), \
             patch.object(WatsonClient, 'handle_error', mock_handle_error):
            
            with pytest.raises(APIError) as exc_info:
                WatsonClient()
            
            assert "Failed to initialize Watson client" in str(exc_info.value)
            mock_handle_error.assert_called_once_with(
                mock_base_init.side_effect,
                "Failed to initialize Watson client"
            ) 