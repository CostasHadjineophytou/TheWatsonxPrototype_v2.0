import pytest
from unittest.mock import patch, MagicMock, call

from backend.services.model_service import ModelService
from backend.utils.errors import ValidationError, AuthenticationError, APIError


class TestModelService:
    """Tests for the ModelService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the ModelService"""
        service = ModelService(mock_watson_client)
        assert service.client == mock_watson_client

    @patch('requests.get')
    def test_get_models_success(self, mock_get, mock_watson_client):
        """Test getting models successfully"""
        # Mock the client's get_request method
        mock_response = {
            'resources': [
                {
                    'model_id': 'ibm/granite-20b-multilingual',
                    'name': 'Granite 20B Multilingual',
                    'type': 'foundation_model'
                },
                {
                    'model_id': 'ibm/mpt-7b-instruct',
                    'name': 'MPT 7B Instruct',
                    'type': 'foundation_model'
                }
            ]
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method
        result = service.get_models()
        
        # Assertions
        assert result == mock_response
        mock_watson_client.get_request.assert_called_once_with('/v2/models')

    def test_get_models_auth_error(self, mock_watson_client):
        """Test getting models with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.get_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_models()
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v2/models')

    def test_get_models_api_error(self, mock_watson_client):
        """Test getting models with API error"""
        # Mock the client to raise an API error
        mock_watson_client.get_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_models()
        
        assert exc_info.value.code == "API_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v2/models')

    @patch('requests.get')
    def test_get_model_by_id_success(self, mock_get, mock_watson_client):
        """Test getting a specific model by ID successfully"""
        # Mock the client's get_request method
        model_id = 'ibm/granite-20b-multilingual'
        mock_response = {
            'model_id': model_id,
            'name': 'Granite 20B Multilingual',
            'type': 'foundation_model',
            'description': 'IBM Granite 20B Multilingual model'
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method
        result = service.get_model_by_id(model_id)
        
        # Assertions
        assert result == mock_response
        mock_watson_client.get_request.assert_called_once_with(f'/v2/models/{model_id}')

    def test_get_model_by_id_invalid_id(self, mock_watson_client):
        """Test getting a model with invalid ID"""
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method with empty ID and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.get_model_by_id("")
        
        assert exc_info.value.code == "INVALID_MODEL_ID"
        mock_watson_client.get_request.assert_not_called()

    def test_get_model_by_id_auth_error(self, mock_watson_client):
        """Test getting a model with authentication error"""
        # Mock the client to raise an authentication error
        model_id = 'ibm/granite-20b-multilingual'
        mock_watson_client.get_request.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(AuthenticationError) as exc_info:
            service.get_model_by_id(model_id)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        mock_watson_client.get_request.assert_called_once_with(f'/v2/models/{model_id}')

    def test_get_model_by_id_api_error(self, mock_watson_client):
        """Test getting a model with API error"""
        # Mock the client to raise an API error
        model_id = 'ibm/granite-20b-multilingual'
        mock_watson_client.get_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.get_model_by_id(model_id)
        
        assert exc_info.value.code == "API_ERROR"
        mock_watson_client.get_request.assert_called_once_with(f'/v2/models/{model_id}')

    @patch('requests.get')
    def test_filter_models_by_type_success(self, mock_get, mock_watson_client):
        """Test filtering models by type successfully"""
        # Mock the client's get_request method
        mock_response = {
            'resources': [
                {
                    'model_id': 'ibm/granite-20b-multilingual',
                    'name': 'Granite 20B Multilingual',
                    'type': 'foundation_model'
                },
                {
                    'model_id': 'ibm/mpt-7b-instruct',
                    'name': 'MPT 7B Instruct',
                    'type': 'foundation_model'
                },
                {
                    'model_id': 'ibm/custom-model',
                    'name': 'Custom Model',
                    'type': 'custom_model'
                }
            ]
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method
        result = service.filter_models_by_type('foundation_model')
        
        # Assertions
        assert len(result) == 2
        assert all(model['type'] == 'foundation_model' for model in result)
        mock_watson_client.get_request.assert_called_once_with('/v2/models')

    def test_filter_models_by_type_empty_type(self, mock_watson_client):
        """Test filtering models with empty type"""
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method with empty type and expect exception
        with pytest.raises(ValidationError) as exc_info:
            service.filter_models_by_type("")
        
        assert exc_info.value.code == "INVALID_MODEL_TYPE"
        mock_watson_client.get_request.assert_not_called()

    def test_filter_models_by_type_no_matches(self, mock_watson_client):
        """Test filtering models with no matches"""
        # Mock the client's get_request method
        mock_response = {
            'resources': [
                {
                    'model_id': 'ibm/granite-20b-multilingual',
                    'name': 'Granite 20B Multilingual',
                    'type': 'foundation_model'
                },
                {
                    'model_id': 'ibm/mpt-7b-instruct',
                    'name': 'MPT 7B Instruct',
                    'type': 'foundation_model'
                }
            ]
        }
        mock_watson_client.get_request.return_value = mock_response
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method
        result = service.filter_models_by_type('custom_model')
        
        # Assertions
        assert len(result) == 0
        mock_watson_client.get_request.assert_called_once_with('/v2/models')

    def test_filter_models_by_type_api_error(self, mock_watson_client):
        """Test filtering models with API error"""
        # Mock the client to raise an API error
        mock_watson_client.get_request.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = ModelService(mock_watson_client)
        
        # Call the method and expect exception
        with pytest.raises(APIError) as exc_info:
            service.filter_models_by_type('foundation_model')
        
        assert exc_info.value.code == "API_ERROR"
        mock_watson_client.get_request.assert_called_once_with('/v2/models') 