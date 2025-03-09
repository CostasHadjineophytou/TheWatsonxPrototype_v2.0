import pytest
from unittest.mock import patch, MagicMock

from backend.services.text_service import TextService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import TEXT_GENERATION_RESPONSE
from backend.config.text_config import TextConfig


class TestTextGeneration:
    """Integration tests for text generation flow"""

    @pytest.fixture
    def setup_text_service(self, mock_watson_client):
        """Setup text service with mocked dependencies"""
        return TextService(mock_watson_client)

    @patch('backend.services.text_service.ModelInference')
    def test_text_generation_flow(self, mock_model_inference, mock_config, setup_text_service, sample_text_response):
        """Test the complete text generation flow from request to response"""
        # Mock the HTTP response from Watson API
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.return_value = TEXT_GENERATION_RESPONSE
        
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        # Call the service
        response = text_service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert response == TEXT_GENERATION_RESPONSE
        assert "generated_text" in response
        assert response["generated_text"] == TEXT_GENERATION_RESPONSE["generated_text"]
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=text_service.watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        )

    @patch('backend.services.text_service.ModelInference')
    def test_text_generation_validation_error(self, mock_model_inference, setup_text_service):
        """Test text generation with validation error"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Patch the validator to raise an exception for model ID
        with patch.object(text_service.validator, 'validate_model_id', side_effect=ValidationError(
            "Invalid model ID", "INVALID_MODEL_ID"
        )):
            # Process text with invalid model ID
            model_id = ""  # Invalid model ID
            project_id = "test-project"
            prompt = "Generate some text"
            # Use the default parameters from TextConfig
            params = TextConfig.DEFAULT_PARAMS.copy()
            # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
            params["decoding_method"] = "sample"
            
            # Call the service and expect exception
            with pytest.raises(ValidationError) as exc_info:
                text_service.process_prompt(model_id, project_id, prompt, params)
            
            assert exc_info.value.code == "INVALID_MODEL_ID"
            
            # Verify ModelInference was not created
            mock_model_inference.assert_not_called()

    @patch('backend.services.text_service.ModelInference')
    def test_text_generation_api_error(self, mock_model_inference, setup_text_service):
        """Test text generation with API error"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the ModelInference instance
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        # Call the service and expect exception
        with pytest.raises(APIError) as exc_info:
            text_service.process_prompt(model_id, project_id, prompt, params)
        
        assert exc_info.value.code == "API_ERROR"
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=text_service.watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        )
        
    @patch('backend.services.text_service.ModelInference')
    def test_text_generation_with_sample_response(self, mock_model_inference, setup_text_service):
        """Test text generation using the sample response fixture"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the ModelInference instance
        mock_model_instance = MagicMock()
        mock_model_inference.return_value = mock_model_instance
        mock_model_instance.generate_text.return_value = TEXT_GENERATION_RESPONSE
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        # Use the default parameters from TextConfig
        params = TextConfig.DEFAULT_PARAMS.copy()
        # Add decoding_method which is required by the validator but not in DEFAULT_PARAMS
        params["decoding_method"] = "sample"
        
        # Call the service
        response = text_service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert response == TEXT_GENERATION_RESPONSE
        assert "generated_text" in response
        assert response["model_id"] == "ibm/granite-20b-multilingual"
        
        # Verify ModelInference was created correctly
        mock_model_inference.assert_called_once_with(
            model_id=model_id,
            credentials=text_service.watson_client.credentials,
            project_id=project_id
        )
        
        # Verify generate_text was called on the model instance
        mock_model_instance.generate_text.assert_called_once_with(
            prompt=prompt, params=params
        ) 