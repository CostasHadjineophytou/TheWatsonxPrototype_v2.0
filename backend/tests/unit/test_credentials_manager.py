import pytest
from unittest.mock import patch, MagicMock

from backend.services.credentials_manager import CredentialsManager
from backend.utils.errors import AuthenticationError, ConfigurationError, APIError


class TestCredentialsManager:
    """Tests for the CredentialsManager class"""

    @pytest.fixture
    def mock_iam_service(self):
        """Create a mock IAM token service"""
        with patch('backend.services.credentials_manager.IAMTokenService') as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            mock_instance.get_iam_token.return_value = "mock_token"
            yield mock_instance

    @pytest.fixture
    def credentials_manager(self, mock_iam_service):
        """Create a CredentialsManager instance with mocked dependencies"""
        with patch('backend.services.credentials_manager.Config') as mock_config:
            # Set up required config values
            mock_config.IBM_CLOUD_API_KEY = "test_api_key"
            mock_config.IBM_CLOUD_RESOURCE_URL = "https://test-resource-url.com"
            manager = CredentialsManager()
            manager.iam_service = mock_iam_service
            return manager

    def test_get_service_credentials_success(self, credentials_manager, mock_iam_service):
        """Test successful retrieval of service credentials"""
        # Mock the _make_request method to return valid resource data
        mock_resources = {
            'resources': [{
                'name': 'test-watson-service',
                'guid': 'test-instance-id',
            }]
        }
        mock_credentials = {
            'api_key': 'service_api_key',
            'url': 'https://service-url.com'
        }

        with patch.object(credentials_manager, '_make_request') as mock_request:
            # Set up mock responses
            mock_request.side_effect = [
                mock_resources,  # First call gets resources
                {'resources': [{'credentials': mock_credentials}]}  # Second call gets credentials
            ]

            # Call the method
            result = credentials_manager.get_service_credentials('watson')

            # Verify the result
            assert result == mock_credentials
            assert mock_iam_service.get_iam_token.called

    def test_get_service_credentials_no_instance(self, credentials_manager):
        """Test when no service instance is found"""
        mock_resources = {'resources': []}

        with patch.object(credentials_manager, '_make_request') as mock_request:
            mock_request.return_value = mock_resources

            with pytest.raises(AuthenticationError) as exc_info:
                credentials_manager.get_service_credentials('nonexistent-service')

            assert exc_info.value.code == "RESOURCE_NOT_FOUND"

    def test_get_service_credentials_api_error(self, credentials_manager):
        """Test handling of API errors"""
        with patch.object(credentials_manager, '_make_request') as mock_request:
            mock_request.side_effect = Exception("API Error")

            with pytest.raises(APIError) as exc_info:
                credentials_manager.get_service_credentials('watson')

            assert "API Error" in str(exc_info.value)

    def test_get_or_create_credentials_existing(self, credentials_manager):
        """Test retrieving existing credentials"""
        mock_credentials = {
            'api_key': 'existing_key',
            'url': 'https://existing-url.com'
        }
        mock_response = {
            'resources': [{
                'credentials': mock_credentials
            }]
        }

        with patch.object(credentials_manager, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            
            result = credentials_manager._get_or_create_credentials(
                'test-instance-id',
                {'Authorization': 'Bearer token'}
            )

            assert result == mock_credentials
            # Verify only GET request was made
            assert mock_request.call_count == 1

    def test_get_or_create_credentials_create_new(self, credentials_manager):
        """Test creating new credentials when none exist"""
        mock_new_credentials = {
            'api_key': 'new_key',
            'url': 'https://new-url.com'
        }

        with patch.object(credentials_manager, '_make_request') as mock_request:
            # First call returns empty resources, second call returns new credentials
            mock_request.side_effect = [
                {'resources': []},
                {'credentials': mock_new_credentials}
            ]

            result = credentials_manager._get_or_create_credentials(
                'test-instance-id',
                {'Authorization': 'Bearer token'}
            )

            assert result == mock_new_credentials
            # Verify both GET and POST requests were made
            assert mock_request.call_count == 2 