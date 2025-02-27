import pytest
from unittest.mock import patch, MagicMock, call

from backend.services.watson_client import WatsonClient
from backend.utils.errors import AuthenticationError, APIError, ValidationError


class TestWatsonClient:
    """Tests for the WatsonClient class"""

    def test_init_valid_credentials(self, mock_credentials, mock_iam_service):
        """Test initializing with valid credentials"""
        # Should not raise an exception
        client = WatsonClient(mock_credentials, mock_iam_service)
        assert client.credentials == mock_credentials
        assert client.iam_service == mock_iam_service

    def test_init_invalid_credentials(self, mock_iam_service):
        """Test initializing with invalid credentials"""
        with pytest.raises(AuthenticationError) as exc_info:
            WatsonClient(None, mock_iam_service)
        
        assert exc_info.value.code == "NO_CREDENTIALS"
        assert "No credentials provided" in exc_info.value.message

    def test_init_no_api_key(self, mock_iam_service):
        """Test initializing with credentials missing API key"""
        credentials = {'url': 'https://test-url.com'}
        
        with pytest.raises(AuthenticationError) as exc_info:
            WatsonClient(credentials, mock_iam_service)
        
        assert exc_info.value.code == "NO_API_KEY"
        assert "API key is required" in exc_info.value.message

    def test_get_headers(self, mock_watson_client, mock_iam_token):
        """Test getting headers with IAM token"""
        # Mock the get_token method to return a mock token
        mock_watson_client.iam_service.get_token.return_value = mock_iam_token
        
        headers = mock_watson_client.get_headers()
        
        assert headers['Authorization'] == f'Bearer {mock_iam_token}'
        assert headers['Content-Type'] == 'application/json'
        mock_watson_client.iam_service.get_token.assert_called_once()

    @patch('requests.post')
    def test_post_request_success(self, mock_post, mock_watson_client):
        """Test successful POST request"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'success'}
        mock_post.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method
        endpoint = '/test-endpoint'
        data = {'key': 'value'}
        result = mock_watson_client.post_request(endpoint, data)
        
        # Assertions
        assert result == {'result': 'success'}
        mock_post.assert_called_once_with(
            f"{mock_watson_client.credentials['url']}{endpoint}",
            json=data,
            headers=mock_watson_client.get_headers.return_value
        )
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_post_request_auth_error(self, mock_post, mock_watson_client):
        """Test POST request with authentication error"""
        # Mock the response for auth error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_post.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        data = {'key': 'value'}
        
        with pytest.raises(AuthenticationError) as exc_info:
            mock_watson_client.post_request(endpoint, data)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        assert "Authentication failed" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_post_request_api_error(self, mock_post, mock_watson_client):
        """Test POST request with API error"""
        # Mock the response for API error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_post.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        data = {'key': 'value'}
        
        with pytest.raises(APIError) as exc_info:
            mock_watson_client.post_request(endpoint, data)
        
        assert exc_info.value.code == "API_ERROR"
        assert "API request failed" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_post_request_validation_error(self, mock_post, mock_watson_client):
        """Test POST request with validation error"""
        # Mock the response for validation error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}
        mock_post.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        data = {'key': 'value'}
        
        with pytest.raises(ValidationError) as exc_info:
            mock_watson_client.post_request(endpoint, data)
        
        assert exc_info.value.code == "VALIDATION_ERROR"
        assert "Invalid request parameters" in exc_info.value.message
        
        # Verify the request was made
        mock_post.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_post_request_connection_error(self, mock_post, mock_watson_client):
        """Test POST request with connection error"""
        # Mock post to raise ConnectionError
        mock_post.side_effect = ConnectionError("Connection failed")
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        data = {'key': 'value'}
        
        with pytest.raises(APIError) as exc_info:
            mock_watson_client.post_request(endpoint, data)
        
        assert exc_info.value.code == "CONNECTION_ERROR"
        assert "Failed to connect to API" in exc_info.value.message
        
        # Verify the request was attempted
        mock_post.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.get')
    def test_get_request_success(self, mock_get, mock_watson_client):
        """Test successful GET request"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'success'}
        mock_get.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method
        endpoint = '/test-endpoint'
        params = {'key': 'value'}
        result = mock_watson_client.get_request(endpoint, params)
        
        # Assertions
        assert result == {'result': 'success'}
        mock_get.assert_called_once_with(
            f"{mock_watson_client.credentials['url']}{endpoint}",
            params=params,
            headers=mock_watson_client.get_headers.return_value
        )
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.get')
    def test_get_request_auth_error(self, mock_get, mock_watson_client):
        """Test GET request with authentication error"""
        # Mock the response for auth error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_get.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        params = {'key': 'value'}
        
        with pytest.raises(AuthenticationError) as exc_info:
            mock_watson_client.get_request(endpoint, params)
        
        assert exc_info.value.code == "AUTHENTICATION_ERROR"
        assert "Authentication failed" in exc_info.value.message
        
        # Verify the request was made
        mock_get.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.get')
    def test_get_request_api_error(self, mock_get, mock_watson_client):
        """Test GET request with API error"""
        # Mock the response for API error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {'error': 'Internal Server Error'}
        mock_get.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        params = {'key': 'value'}
        
        with pytest.raises(APIError) as exc_info:
            mock_watson_client.get_request(endpoint, params)
        
        assert exc_info.value.code == "API_ERROR"
        assert "API request failed" in exc_info.value.message
        
        # Verify the request was made
        mock_get.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.get')
    def test_get_request_validation_error(self, mock_get, mock_watson_client):
        """Test GET request with validation error"""
        # Mock the response for validation error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': 'Bad Request'}
        mock_get.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        params = {'key': 'value'}
        
        with pytest.raises(ValidationError) as exc_info:
            mock_watson_client.get_request(endpoint, params)
        
        assert exc_info.value.code == "VALIDATION_ERROR"
        assert "Invalid request parameters" in exc_info.value.message
        
        # Verify the request was made
        mock_get.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.get')
    def test_get_request_connection_error(self, mock_get, mock_watson_client):
        """Test GET request with connection error"""
        # Mock get to raise ConnectionError
        mock_get.side_effect = ConnectionError("Connection failed")
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method and expect exception
        endpoint = '/test-endpoint'
        params = {'key': 'value'}
        
        with pytest.raises(APIError) as exc_info:
            mock_watson_client.get_request(endpoint, params)
        
        assert exc_info.value.code == "CONNECTION_ERROR"
        assert "Failed to connect to API" in exc_info.value.message
        
        # Verify the request was attempted
        mock_get.assert_called_once()
        mock_watson_client.get_headers.assert_called_once()

    def test_generate_text(self, mock_watson_client):
        """Test generating text"""
        # Mock post_request
        mock_watson_client.post_request = MagicMock(return_value={
            'results': [{'generated_text': 'This is a test response'}]
        })
        
        # Call the method
        model_id = 'ibm/granite-20b-multilingual'
        project_id = 'test-project'
        text = 'Generate some text'
        params = {'temperature': 0.7}
        
        result = mock_watson_client.generate_text(model_id, project_id, text, params)
        
        # Assertions
        assert result == 'This is a test response'
        mock_watson_client.post_request.assert_called_once_with(
            f'/v1/text/generation?version=2023-05-29',
            {
                'model_id': model_id,
                'project_id': project_id,
                'input': text,
                'parameters': params
            }
        )

    def test_generate_text_no_results(self, mock_watson_client):
        """Test generating text with no results"""
        # Mock post_request with empty results
        mock_watson_client.post_request = MagicMock(return_value={
            'results': []
        })
        
        # Call the method
        model_id = 'ibm/granite-20b-multilingual'
        project_id = 'test-project'
        text = 'Generate some text'
        params = {'temperature': 0.7}
        
        with pytest.raises(APIError) as exc_info:
            mock_watson_client.generate_text(model_id, project_id, text, params)
        
        assert exc_info.value.code == "NO_RESULTS"
        assert "No results returned from API" in exc_info.value.message
        
        # Verify the request was made
        mock_watson_client.post_request.assert_called_once()

    def test_analyze_text(self, mock_watson_client):
        """Test analyzing text with NLU"""
        # Mock post_request
        mock_watson_client.post_request = MagicMock(return_value={
            'sentiment': {'document': {'score': 0.8, 'label': 'positive'}}
        })
        
        # Call the method
        text = 'Analyze this text'
        features = {'sentiment': {}}
        
        result = mock_watson_client.analyze_text(text, features)
        
        # Assertions
        assert result['sentiment']['document']['score'] == 0.8
        assert result['sentiment']['document']['label'] == 'positive'
        mock_watson_client.post_request.assert_called_once_with(
            '/v1/analyze?version=2022-04-07',
            {
                'text': text,
                'features': features
            }
        )

    @patch('requests.post')
    def test_text_to_speech(self, mock_post, mock_watson_client):
        """Test text to speech conversion"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'audio_data'
        mock_post.return_value = mock_response
        
        # Mock get_headers
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        
        # Call the method
        text = 'Convert this text to speech'
        voice = 'en-US_MichaelV3Voice'
        params = {'pitch': 0, 'speed': 0}
        
        result = mock_watson_client.text_to_speech(text, voice, params)
        
        # Assertions
        assert result == b'audio_data'
        
        # Verify the correct URL and headers were used
        expected_url = f"{mock_watson_client.credentials['url']}/v1/synthesize?voice={voice}"
        mock_post.assert_called_once_with(
            expected_url,
            data=text,
            headers={'Authorization': 'Bearer token', 'Content-Type': 'application/json', 'Accept': 'audio/wav'},
            params={'pitch': 0, 'speed': 0}
        )
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_speech_to_text(self, mock_post, mock_watson_client):
        """Test speech to text conversion"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [{'alternatives': [{'transcript': 'This is a test transcript'}]}]
        }
        mock_post.return_value = mock_response
        
        # Mock get_headers and open file
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        mock_open = MagicMock()
        mock_open.read.return_value = b'audio_data'
        
        # Call the method
        with patch('builtins.open', return_value=mock_open):
            result = mock_watson_client.speech_to_text('test_file.wav')
        
        # Assertions
        assert result == 'This is a test transcript'
        
        # Verify the correct URL and headers were used
        expected_url = f"{mock_watson_client.credentials['url']}/v1/recognize"
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        assert call_args['url'] == expected_url
        assert call_args['headers'] == {'Authorization': 'Bearer token', 'Content-Type': 'audio/wav'}
        assert call_args['data'] == b'audio_data'
        mock_watson_client.get_headers.assert_called_once()

    @patch('requests.post')
    def test_speech_to_text_no_results(self, mock_post, mock_watson_client):
        """Test speech to text with no results"""
        # Mock the response with no results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_post.return_value = mock_response
        
        # Mock get_headers and open file
        mock_watson_client.get_headers = MagicMock(return_value={'Authorization': 'Bearer token'})
        mock_open = MagicMock()
        mock_open.read.return_value = b'audio_data'
        
        # Call the method
        with patch('builtins.open', return_value=mock_open):
            result = mock_watson_client.speech_to_text('test_file.wav')
        
        # Assertions
        assert result == ""  # Empty string when no results
        mock_post.assert_called_once()
        mock_watson_client.get_headers.assert_called_once() 