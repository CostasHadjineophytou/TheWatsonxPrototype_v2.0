import pytest
from unittest.mock import patch, MagicMock

from backend.services.text_service import TextService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import TEXT_GENERATION_RESPONSE


class TestTextGeneration:
    """Integration tests for text generation flow"""

    @pytest.fixture
    def setup_text_service(self, mock_watson_client, mock_service_validator, mock_iam_service):
        """Setup text service with mocked dependencies"""
        return TextService(mock_watson_client, mock_service_validator)

    @patch('requests.post')
    def test_text_generation_flow(self, mock_post, mock_config, setup_text_service, sample_text_response):
        """Test the complete text generation flow from request to response"""
        # Mock the HTTP response from Watson API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{'generated_text': sample_text_response}]
        }
        mock_post.return_value = mock_response
        
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the client's generate_text method to return the full sample response
        text_service.client.generate_text.return_value = TEXT_GENERATION_RESPONSE
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        params = {
            "temperature": 0.7,
            "max_new_tokens": 100,
            "decoding_method": "sample"
        }
        
        # Call the service
        response = text_service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert response == TEXT_GENERATION_RESPONSE
        assert "generated_text" in response
        assert response["generated_text"] == TEXT_GENERATION_RESPONSE["generated_text"]
        
        # Verify the client method was called with correct parameters
        text_service.client.generate_text.assert_called_once_with(
            model_id, project_id, prompt, params
        )

    def test_text_generation_validation_error(self, setup_text_service):
        """Test text generation with validation error"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the validator to raise an exception for model ID
        text_service.validator.validate_model_id.side_effect = ValidationError(
            "Invalid model ID", "INVALID_MODEL_ID"
        )
        
        # Process text with invalid model ID
        model_id = ""  # Invalid model ID
        project_id = "test-project"
        prompt = "Generate some text"
        params = {"temperature": 0.7}
        
        # Call the service and expect exception
        with pytest.raises(ValidationError) as exc_info:
            text_service.process_prompt(model_id, project_id, prompt, params)
        
        assert exc_info.value.code == "INVALID_MODEL_ID"
        
        # Verify client method was not called
        text_service.client.generate_text.assert_not_called()

    def test_text_generation_api_error(self, setup_text_service):
        """Test text generation with API error"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the client to raise an API error
        text_service.client.generate_text.side_effect = APIError(
            "API request failed", "API_ERROR"
        )
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        params = {"temperature": 0.7}
        
        # Call the service and expect exception
        with pytest.raises(APIError) as exc_info:
            text_service.process_prompt(model_id, project_id, prompt, params)
        
        assert exc_info.value.code == "API_ERROR"
        
        # Verify client method was called
        text_service.client.generate_text.assert_called_once_with(
            model_id, project_id, prompt, params
        )
        
    def test_text_generation_with_sample_response(self, setup_text_service):
        """Test text generation using the sample response fixture"""
        # Get the text service from fixture
        text_service = setup_text_service
        
        # Mock the client's generate_text method to return the sample response
        text_service.client.generate_text.return_value = TEXT_GENERATION_RESPONSE
        
        # Process text
        model_id = "ibm/granite-20b-multilingual"
        project_id = "test-project"
        prompt = "Generate some text"
        params = {"temperature": 0.7}
        
        # Call the service
        response = text_service.process_prompt(model_id, project_id, prompt, params)
        
        # Assertions
        assert response == TEXT_GENERATION_RESPONSE
        assert "generated_text" in response
        assert response["model_id"] == "ibm/granite-20b-multilingual"
        
        # Verify client method was called
        text_service.client.generate_text.assert_called_once_with(
            model_id, project_id, prompt, params
        ) 