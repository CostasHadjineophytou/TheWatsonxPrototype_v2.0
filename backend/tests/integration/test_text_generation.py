import pytest
from unittest.mock import patch, MagicMock

from backend.services.text_service import TextService
from backend.services.watson_client import WatsonClient
from backend.service_factory import ServiceFactory
from backend.utils.errors import ValidationError, AuthenticationError, APIError


class TestTextGeneration:
    """Integration tests for text generation flow"""

    @patch('requests.post')
    def test_text_generation_flow(self, mock_post, mock_config):
        """Test the complete text generation flow from request to response"""
        # Mock the HTTP response from Watson API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{'generated_text': 'This is a test response from Watson'}]
        }
        mock_post.return_value = mock_response
        
        # Set up configuration
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the real components (not mocks)
        from backend.services.iam_token import IAMTokenService
        from backend.services.credentials_manager import CredentialsManager
        from backend.validators.service_validator import ServiceValidator
        
        # Initialize the components
        iam_service = IAMTokenService()
        credentials = {'api_key': 'test_api_key', 'url': 'https://test-url.com'}
        
        # Patch the IAM token service to return a mock token
        with patch.object(iam_service, 'get_token', return_value='mock_token'):
            # Create the Watson client
            watson_client = WatsonClient(credentials, iam_service)
            
            # Create the text service
            service_validator = ServiceValidator()
            text_service = TextService(watson_client, service_validator)
            
            # Process text
            model_id = "ibm/granite-20b-multilingual"
            project_id = "test-project"
            text = "Generate some text"
            params = {
                "temperature": 0.7,
                "max_new_tokens": 100,
                "decoding_method": "sample"
            }
            
            # Call the service
            response = text_service.process_text(model_id, project_id, text, params)
            
            # Assertions
            assert response == 'This is a test response from Watson'
            
            # Verify the HTTP request was made
            mock_post.assert_called_once()
            
            # Check that the request was made with the correct data
            call_args = mock_post.call_args[1]
            assert 'json' in call_args
            json_data = call_args['json']
            assert json_data['model_id'] == model_id
            assert json_data['project_id'] == project_id
            assert json_data['input'] == text
            assert 'parameters' in json_data
            assert json_data['parameters']['temperature'] == params['temperature']
            assert json_data['parameters']['max_new_tokens'] == params['max_new_tokens']
            assert json_data['parameters']['decoding_method'] == params['decoding_method']

    @patch('requests.post')
    def test_text_generation_validation_error(self, mock_post, mock_config):
        """Test text generation with validation error"""
        # Set up configuration
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the real components (not mocks)
        from backend.services.iam_token import IAMTokenService
        from backend.validators.service_validator import ServiceValidator
        
        # Initialize the components
        iam_service = IAMTokenService()
        credentials = {'api_key': 'test_api_key', 'url': 'https://test-url.com'}
        
        # Patch the IAM token service to return a mock token
        with patch.object(iam_service, 'get_token', return_value='mock_token'):
            # Create the Watson client
            watson_client = WatsonClient(credentials, iam_service)
            
            # Create the text service with a validator that will raise an exception
            service_validator = ServiceValidator()
            
            # Patch the validator to raise an exception for model ID
            with patch.object(service_validator, 'validate_model_id', 
                             side_effect=ValidationError("Invalid model ID", "INVALID_MODEL_ID")):
                
                text_service = TextService(watson_client, service_validator)
                
                # Process text with invalid model ID
                model_id = ""  # Invalid model ID
                project_id = "test-project"
                text = "Generate some text"
                params = {"temperature": 0.7}
                
                # Call the service and expect exception
                with pytest.raises(ValidationError) as exc_info:
                    text_service.process_text(model_id, project_id, text, params)
                
                assert exc_info.value.code == "INVALID_MODEL_ID"
                
                # Verify no HTTP request was made
                mock_post.assert_not_called()

    @patch('requests.post')
    def test_text_generation_api_error(self, mock_post, mock_config):
        """Test text generation with API error"""
        # Mock the HTTP response with an error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_post.return_value = mock_response
        
        # Set up configuration
        mock_config.WATSON_API_KEY = "test_api_key"
        mock_config.WATSON_URL = "https://test-url.com"
        
        # Create the real components (not mocks)
        from backend.services.iam_token import IAMTokenService
        from backend.validators.service_validator import ServiceValidator
        
        # Initialize the components
        iam_service = IAMTokenService()
        credentials = {'api_key': 'test_api_key', 'url': 'https://test-url.com'}
        
        # Patch the IAM token service to return a mock token
        with patch.object(iam_service, 'get_token', return_value='mock_token'):
            # Create the Watson client
            watson_client = WatsonClient(credentials, iam_service)
            
            # Create the text service
            service_validator = ServiceValidator()
            text_service = TextService(watson_client, service_validator)
            
            # Process text
            model_id = "ibm/granite-20b-multilingual"
            project_id = "test-project"
            text = "Generate some text"
            params = {"temperature": 0.7}
            
            # Call the service and expect exception
            with pytest.raises(APIError) as exc_info:
                text_service.process_text(model_id, project_id, text, params)
            
            assert "API_ERROR" in exc_info.value.code
            
            # Verify the HTTP request was made
            mock_post.assert_called_once() 