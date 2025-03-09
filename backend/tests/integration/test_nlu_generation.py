import pytest
from unittest.mock import patch, MagicMock

from backend.services.nlu_service import NLUService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import NLU_ANALYSIS_RESPONSE


class TestNLUAnalysis:
    """Integration tests for NLU analysis flow"""

    @pytest.fixture
    def setup_nlu_service(self, mock_credentials_manager):
        """Setup NLU service with mocked dependencies"""
        return NLUService(mock_credentials_manager)

    @patch('backend.services.nlu_service.NaturalLanguageUnderstandingV1')
    def test_nlu_analysis_flow(self, mock_nlu_v1, setup_nlu_service, sample_nlu_response):
        """Test the complete NLU analysis flow from request to response"""
        # Mock the NLU client response
        mock_nlu_instance = MagicMock()
        mock_nlu_v1.return_value = mock_nlu_instance
        mock_nlu_instance.analyze.return_value.get_result.return_value = NLU_ANALYSIS_RESPONSE
        
        # Get the NLU service from fixture
        nlu_service = setup_nlu_service
        
        # Process text
        text = "IBM is a leader in AI and machine learning. John Doe thinks their technology is excellent!"
        features = {
            "sentiment": {},
            "entities": {},
            "keywords": {}
        }
        
        # Call the service
        response = nlu_service.analyze_text(text, features)
        
        # Assertions
        assert response == NLU_ANALYSIS_RESPONSE
        assert "sentiment" in response
        assert "entities" in response
        assert "keywords" in response
        assert response["sentiment"]["document"]["label"] == "positive"
        
        # Verify NLU client was called correctly
        mock_nlu_instance.analyze.assert_called_once_with(
            text=text,
            features=features
        )

    @patch('backend.services.nlu_service.NaturalLanguageUnderstandingV1')
    def test_nlu_analysis_validation_error(self, mock_nlu_v1, setup_nlu_service):
        """Test NLU analysis with validation error"""
        nlu_service = setup_nlu_service
        
        # Patch the validator to raise an exception
        with patch.object(nlu_service.validator, 'validate_nlu_request', side_effect=ValidationError(
            "Invalid text input", "INVALID_TEXT"
        )):
            text = ""  # Invalid text
            features = {"sentiment": {}}
            
            # Call the service and expect exception
            with pytest.raises(ValidationError) as exc_info:
                nlu_service.analyze_text(text, features)
            
            assert exc_info.value.code == "INVALID_TEXT"
            
            # Verify NLU client was not called
            mock_nlu_v1.assert_not_called()

    @patch('backend.services.nlu_service.NaturalLanguageUnderstandingV1')
    def test_nlu_analysis_api_error(self, mock_nlu_v1, setup_nlu_service):
        """Test NLU analysis with API error"""
        # Mock the NLU client to raise an API error
        mock_nlu_instance = MagicMock()
        mock_nlu_v1.return_value = mock_nlu_instance
        mock_nlu_instance.analyze.side_effect = Exception("API request failed")
        
        nlu_service = setup_nlu_service
        
        # Process text
        text = "Test text for API error"
        features = {"sentiment": {}}
        
        # Call the service and expect exception
        with pytest.raises(APIError) as exc_info:
            nlu_service.analyze_text(text, features)
        
        assert "API request failed" in str(exc_info.value)
        
        # Verify NLU client was called
        mock_nlu_instance.analyze.assert_called_once_with(
            text=text,
            features=features
        ) 