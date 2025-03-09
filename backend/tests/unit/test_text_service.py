import pytest
from unittest.mock import patch, MagicMock

from backend.services.text_service import TextService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import TEXT_GENERATION_RESPONSE
from backend.config.text_config import TextConfig


class TestTextService:
    """Tests for the TextService class"""

    def test_init(self, mock_watson_client):
        """Test initializing the TextService"""
        service = TextService(mock_watson_client)
        
        assert service.watson_client == mock_watson_client

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_valid(self, mock_model_inference, mock_watson_client):
        """Test processing text with valid parameters"""
        # Mock the ModelInference instance
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.return_value = TEXT_GENERATION_RESPONSE
        
        # Create the service
        service = TextService(mock_watson_client)
        
        # Call the method
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        result = service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert result == TEXT_GENERATION_RESPONSE
        assert result["generated_text"] == TEXT_GENERATION_RESPONSE["generated_text"]
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=mock_watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        )

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_invalid_model_id(self, mock_model_inference, mock_watson_client):
        """Test processing text with invalid model ID"""
        # Create the service and patch the validator
        service = TextService(mock_watson_client)
        
        # Patch the validator method
        with patch.object(service.validator, 'validate_model_id', side_effect=ValidationError(
            "Invalid model ID format", "INVALID_MODEL_ID"
        )):
            # Call the method and expect exception
            model_id = ""  # Invalid model ID
            project_id = "test-project"
            prompt = "Generate some text"
            # Use the default parameters from TextConfig
            params = TextConfig.DEFAULT_PARAMS.copy()
            # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
            params["decoding_method"] = "sample"
            
            with pytest.raises(ValidationError) as exc_info:
                service.process_prompt(model_id, project_id, prompt, params)
            
            assert exc_info.value.code == "INVALID_MODEL_ID"
            
            # Verify ModelInference was not created
            mock_model_inference.assert_not_called()

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_invalid_project_id(self, mock_model_inference, mock_watson_client):
        """Test processing text with invalid project ID"""
        # Create the service
        service = TextService(mock_watson_client)
        
        # Patch the validator methods
        with patch.object(service.validator, 'validate_project_id', side_effect=ValidationError(
            "Invalid project ID format", "INVALID_PROJECT_ID"
        )):
            # Call the method and expect exception
            model_id = "ibm/granite-20b-multilingual"
            project_id = ""  # Invalid project ID
            prompt = "Generate some text"
            # Use the default parameters from TextConfig
            params = TextConfig.DEFAULT_PARAMS.copy()
            # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
            params["decoding_method"] = "sample"
            
            with pytest.raises(ValidationError) as exc_info:
                service.process_prompt(model_id, project_id, prompt, params)
            
            assert exc_info.value.code == "INVALID_PROJECT_ID"
            
            # Verify ModelInference was not created
            mock_model_inference.assert_not_called()

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_invalid_params(self, mock_model_inference, mock_watson_client):
        """Test processing text with invalid parameters"""
        # Create the service
        service = TextService(mock_watson_client)
        
        # Patch the validator method
        with patch.object(service.validator, 'validate_watson_text_params', side_effect=ValidationError(
            "Invalid text parameters", "INVALID_TEXT_PARAMS", 
            {"invalid_params": ["invalid_param"]}
        )):
            # Call the method and expect exception
            model_id = "ibm/granite-20b-multilingual"
            project_id = "test-project"
            prompt = "Generate some text"
            # Use the default parameters from TextConfig with an invalid parameter
            params = TextConfig.DEFAULT_PARAMS.copy()
            # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
            params["decoding_method"] = "sample"
            params["invalid_param"] = "value"  # Invalid parameter
            
            with pytest.raises(ValidationError) as exc_info:
                service.process_prompt(model_id, project_id, prompt, params)
            
            assert exc_info.value.code == "INVALID_TEXT_PARAMS"
            assert "invalid_params" in exc_info.value.details
            
            # Verify ModelInference was not created
            mock_model_inference.assert_not_called()

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_api_error(self, mock_model_inference, mock_watson_client):
        """Test processing text with API error"""
        # Mock the ModelInference instance
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Create the service
        service = TextService(mock_watson_client)
        
        # Call the method and expect exception
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        with pytest.raises(APIError) as exc_info:
            service.process_prompt(model_id, project_id, prompt, params)
        
        assert exc_info.value.code == "API_ERROR"
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=mock_watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        )

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_auth_error(self, mock_model_inference, mock_watson_client):
        """Test processing text with authentication error"""
        # Create the service
        service = TextService(mock_watson_client)
        
        # Patch the validator method
        with patch.object(service.validator, 'validate_credentials', side_effect=AuthenticationError(
            "Authentication failed", "AUTHENTICATION_ERROR"
        )):
            # Call the method and expect exception
            model_id = "ibm/granite-20b-multilingual"
            project_id = "test-project"
            prompt = "Generate some text"
            # Use the default parameters from TextConfig
            params = TextConfig.DEFAULT_PARAMS.copy()
            # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
            params["decoding_method"] = "sample"
            
            with pytest.raises(AuthenticationError) as exc_info:
                service.process_prompt(model_id, project_id, prompt, params)
            
            assert exc_info.value.code == "AUTHENTICATION_ERROR"
            
            # Verify ModelInference was not created
            mock_model_inference.assert_not_called()

    @patch('backend.services.text_service.ModelInference')
    def test_process_prompt_empty_response(self, mock_model_inference, mock_watson_client):
        """Test processing text with empty response"""
        # Mock the ModelInference instance
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.return_value = ""
        
        # Create the service
        service = TextService(mock_watson_client)
        
        # Call the method
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        result = service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert result == ""
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=mock_watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        ) 