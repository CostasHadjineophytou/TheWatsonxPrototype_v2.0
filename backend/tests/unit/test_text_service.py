import pytest
from unittest.mock import patch, MagicMock, call

from backend.services.text_service import TextService
from backend.utils.errors import ValidationError, AuthenticationError, APIError


class TestTextService:
    """Tests for the TextService class"""

    def test_init(self, mock_watson_client, mock_service_validator):
        """Test initializing the TextService"""
        service = TextService(mock_watson_client, mock_service_validator)
        
        assert service.client == mock_watson_client
        assert service.validator == mock_service_validator

    def test_process_text_valid(self, mock_watson_client, mock_service_validator):
        """Test processing text with valid parameters"""
        # Mock the client's generate_text method
        mock_watson_client.generate_text.return_value = "Generated text response"
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        text = "Generate some text"
        params = {
            "temperature": 0.7,
            "max_new_tokens": 100,
            "decoding_method": "sample"
        }
        
        result = service.process_text(model_id, project_id, text, params)
        
        # Assertions
        assert result == "Generated text response"
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        mock_service_validator.validate_watson_text_params.assert_called_once_with(params)
        
        # Verify client method was called
        mock_watson_client.generate_text.assert_called_once_with(
            model_id, project_id, text, params
        )

    def test_process_text_invalid_model_id(self, mock_watson_client, mock_service_validator):
        """Test processing text with invalid model ID"""
        # Mock the validator to raise an exception for model ID
        mock_service_validator.validate_model_id.side_effect = ValidationError(
            "Invalid model ID format", "INVALID_MODEL_ID"
        )
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method and expect exception
        model_id = ""  # Invalid model ID
        project_id = "test-project"
        text = "Generate some text"
        params = {"temperature": 0.7}
        
        with pytest.raises(ValidationError) as exc_info:
            service.process_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "INVALID_MODEL_ID"
        
        # Verify validator method was called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        
        # Verify other methods were not called
        mock_service_validator.validate_project_id.assert_not_called()
        mock_service_validator.validate_watson_text_params.assert_not_called()
        mock_watson_client.generate_text.assert_not_called()

    def test_process_text_invalid_project_id(self, mock_watson_client, mock_service_validator):
        """Test processing text with invalid project ID"""
        # Mock the validator to raise an exception for project ID
        mock_service_validator.validate_project_id.side_effect = ValidationError(
            "Invalid project ID format", "INVALID_PROJECT_ID"
        )
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method and expect exception
        model_id = "ibm/granite-20b-multilingual"
        project_id = ""  # Invalid project ID
        text = "Generate some text"
        params = {"temperature": 0.7}
        
        with pytest.raises(ValidationError) as exc_info:
            service.process_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "INVALID_PROJECT_ID"
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        
        # Verify other methods were not called
        mock_service_validator.validate_watson_text_params.assert_not_called()
        mock_watson_client.generate_text.assert_not_called()

    def test_process_text_invalid_params(self, mock_watson_client, mock_service_validator):
        """Test processing text with invalid parameters"""
        # Mock the validator to raise an exception for text parameters
        mock_service_validator.validate_watson_text_params.side_effect = ValidationError(
            "Invalid text parameters", "INVALID_TEXT_PARAMS", 
            {"invalid_params": ["invalid_param"]}
        )
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method and expect exception
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        text = "Generate some text"
        params = {"invalid_param": "value"}  # Invalid parameter
        
        with pytest.raises(ValidationError) as exc_info:
            service.process_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "INVALID_TEXT_PARAMS"
        assert "invalid_params" in exc_info.value.details
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        mock_service_validator.validate_watson_text_params.assert_called_once_with(params)
        
        # Verify client method was not called
        mock_watson_client.generate_text.assert_not_called()

    def test_process_text_api_error(self, mock_watson_client, mock_service_validator):
        """Test processing text with API error"""
        # Mock the client to raise an API error
        mock_watson_client.generate_text.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method and expect exception
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        text = "Generate some text"
        params = {"temperature": 0.7}
        
        with pytest.raises(APIError) as exc_info:
            service.process_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "API_ERROR"
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        mock_service_validator.validate_watson_text_params.assert_called_once_with(params)
        
        # Verify client method was called
        mock_watson_client.generate_text.assert_called_once_with(
            model_id, project_id, text, params
        )

    def test_process_text_auth_error(self, mock_watson_client, mock_service_validator):
        """Test processing text with authentication error"""
        # Mock the client to raise an authentication error
        mock_watson_client.generate_text.side_effect = AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method and expect exception
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        text = "Generate some text"
        params = {"temperature": 0.7}
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.process_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        mock_service_validator.validate_watson_text_params.assert_called_once_with(params)
        
        # Verify client method was called
        mock_watson_client.generate_text.assert_called_once_with(
            model_id, project_id, text, params
        )

    def test_process_text_empty_response(self, mock_watson_client, mock_service_validator):
        """Test processing text with empty response"""
        # Mock the client to return an empty string
        mock_watson_client.generate_text.return_value = ""
        
        # Create the service
        service = TextService(mock_watson_client, mock_service_validator)
        
        # Call the method
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        text = "Generate some text"
        params = {"temperature": 0.7}
        
        result = service.process_text(model_id, project_id, text, params)
        
        # Assertions
        assert result == ""
        
        # Verify validator methods were called
        mock_service_validator.validate_model_id.assert_called_once_with(model_id)
        mock_service_validator.validate_project_id.assert_called_once_with(project_id)
        mock_service_validator.validate_watson_text_params.assert_called_once_with(params)
        
        # Verify client method was called
        mock_watson_client.generate_text.assert_called_once_with(
            model_id, project_id, text, params
        ) 