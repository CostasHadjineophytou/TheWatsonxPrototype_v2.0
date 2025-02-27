import pytest
from unittest.mock import patch, MagicMock

from backend.services.model_service import ModelService
from backend.utils.errors import ValidationError, APIError


class TestModelService:
    """Tests for the ModelService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the ModelService"""
        service = ModelService(mock_watson_client)
        assert service.watson_client == mock_watson_client
        assert hasattr(service, 'file_manager')

    @patch('backend.utils.file_manager.FileManager.save_json')
    def test_list_models_success(self, mock_save_json, mock_watson_client):
        """Test listing models successfully"""
        mock_response = {
            "resources": [
                {
                    "model_id": "test_model",
                    "name": "Test Model"
                }
            ]
        }
        mock_watson_client.client.foundation_models.get_model_specs.return_value = mock_response
        
        service = ModelService(mock_watson_client)
        result = service.list_models()
        
        assert result == mock_response
        mock_watson_client.client.foundation_models.get_model_specs.assert_called_once()
        mock_save_json.assert_called_once_with("data/cloud/models.json", mock_response["resources"])

    def test_list_models_validation_error(self, mock_watson_client):
        """Test listing models with invalid credentials"""
        service = ModelService(mock_watson_client)
        
        # Mock validator to raise ValidationError
        with patch.object(service.validator, 'validate_credentials') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid credentials", "INVALID_CREDENTIALS")
            
            with pytest.raises(ValidationError) as exc_info:
                service.list_models()
            
            assert exc_info.value.code == "INVALID_CREDENTIALS"
            mock_watson_client.client.foundation_models.get_model_specs.assert_not_called()

    def test_list_models_api_error(self, mock_watson_client):
        """Test listing models with API error"""
        mock_watson_client.client.foundation_models.get_model_specs.side_effect = Exception("API Error")
        
        service = ModelService(mock_watson_client)
        with pytest.raises(APIError) as exc_info:
            service.list_models()
        
        assert str(exc_info.value) == "API Error"

    def test_get_model_specs_success(self, mock_watson_client):
        """Test getting model specs successfully"""
        mock_model = {
            "model_id": "test_model",
            "name": "Test Model"
        }
        mock_response = {
            "resources": [mock_model]
        }
        mock_watson_client.client.foundation_models.get_model_specs.return_value = mock_response
        
        service = ModelService(mock_watson_client)
        result = service.get_model_specs("test_model")
        
        assert result == mock_model
        mock_watson_client.client.foundation_models.get_model_specs.assert_called_once()

    def test_get_model_specs_not_found(self, mock_watson_client):
        """Test getting specs for non-existent model"""
        mock_response = {
            "resources": [
                {
                    "model_id": "other_model",
                    "name": "Other Model"
                }
            ]
        }
        mock_watson_client.client.foundation_models.get_model_specs.return_value = mock_response
        
        service = ModelService(mock_watson_client)
        result = service.get_model_specs("test_model")
        
        assert result is None

    def test_get_model_specs_invalid_id(self, mock_watson_client):
        """Test getting model specs with invalid model ID"""
        service = ModelService(mock_watson_client)
        
        with patch.object(service.validator, 'validate_model_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid model ID", "INVALID_MODEL_ID")
            
            with pytest.raises(ValidationError) as exc_info:
                service.get_model_specs("")
            
            assert exc_info.value.code == "INVALID_MODEL_ID"
            mock_watson_client.client.foundation_models.get_model_specs.assert_not_called()

    def test_get_model_specs_api_error(self, mock_watson_client):
        """Test getting model specs with API error"""
        mock_watson_client.client.foundation_models.get_model_specs.side_effect = Exception("API Error")
        
        service = ModelService(mock_watson_client)
        with pytest.raises(APIError) as exc_info:
            service.get_model_specs("test_model")
        
        assert str(exc_info.value) == "API Error" 