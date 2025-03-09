import pytest
from unittest.mock import patch, MagicMock

from backend.services.nlu_service import NLUService
from backend.utils.errors import ValidationError, AuthenticationError, APIError
from backend.tests.fixtures.sample_responses import NLU_ANALYSIS_RESPONSE


class TestNLUService:
    """Tests for the NLUService class"""

    def test_init(self, mock_credentials_manager):
        """Test initializing the NLUService"""
        service = NLUService(mock_credentials_manager)
        assert service.credentials_manager == mock_credentials_manager
        assert service._nlu is None

    def test_initialize_success(self, mock_credentials_manager):
        """Test successful NLU client initialization"""
        mock_credentials = {
            'apikey': 'test_api_key',
            'url': 'https://test-url.com'
        }
        mock_credentials_manager.get_service_credentials.return_value = mock_credentials
        
        service = NLUService(mock_credentials_manager)
        service.initialize()
        
        mock_credentials_manager.get_service_credentials.assert_called_once_with("Natural Language Understanding")
        assert service._nlu is not None

    def test_initialize_error(self, mock_credentials_manager):
        """Test NLU client initialization failure"""
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Failed to get credentials", "NLU_INIT_ERROR"
        )
        
        service = NLUService(mock_credentials_manager)
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.initialize()
        
        assert exc_info.value.code == "NLU_INIT_ERROR"
        assert service._nlu is None

    def test_analyze_text_success(self, mock_credentials_manager):
        """Test analyzing text successfully"""
        service = NLUService(mock_credentials_manager)
        
        # Mock the NLU client
        mock_nlu = MagicMock()
        mock_result = MagicMock()
        mock_result.get_result.return_value = NLU_ANALYSIS_RESPONSE
        mock_nlu.analyze.return_value = mock_result
        service._nlu = mock_nlu
        
        text = "Sample text for analysis"
        features = {
            'sentiment': {'document': True},
            'entities': {'sentiment': True, 'limit': 10},
            'keywords': {'sentiment': True, 'limit': 10}
        }
        
        result = service.analyze_text(text, features)
        
        assert result == NLU_ANALYSIS_RESPONSE
        mock_nlu.analyze.assert_called_once_with(
            text=text,
            features=features
        )

    def test_analyze_text_validation_error(self, mock_credentials_manager):
        """Test analyzing text with validation error"""
        service = NLUService(mock_credentials_manager)
        
        with patch.object(service.validator, 'validate_nlu_request') as mock_validate:
            mock_validate.side_effect = ValidationError(
                "Invalid request", "INVALID_REQUEST"
            )
            
            with pytest.raises(ValidationError) as exc_info:
                service.analyze_text("Sample text", {'sentiment': {}})
            
            assert exc_info.value.code == "INVALID_REQUEST"
            assert service._nlu is None

    def test_analyze_text_auth_error(self, mock_credentials_manager):
        """Test analyzing text with authentication error"""
        service = NLUService(mock_credentials_manager)
        mock_credentials_manager.get_service_credentials.side_effect = AuthenticationError(
            "Authentication failed", "NLU_INIT_ERROR"
        )
        
        text = "Sample text"
        features = {'sentiment': {'document': True}}
        
        with pytest.raises(AuthenticationError) as exc_info:
            service.analyze_text(text, features)
        
        assert exc_info.value.code == "NLU_INIT_ERROR"

    def test_analyze_text_api_error(self, mock_credentials_manager):
        """Test analyzing text with API error"""
        service = NLUService(mock_credentials_manager)
        
        # Mock the NLU client
        mock_nlu = MagicMock()
        mock_nlu.analyze.side_effect = Exception("Failed to analyze text")
        service._nlu = mock_nlu
        
        text = "Sample text"
        features = {'sentiment': {'document': True}}
        
        with pytest.raises(APIError) as exc_info:
            service.analyze_text(text, features)
        
        assert "Failed to analyze text" in str(exc_info.value)

    def test_analyze_text_empty_text(self, mock_credentials_manager):
        """Test analyzing with empty text"""
        service = NLUService(mock_credentials_manager)
        
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_text("", {'sentiment': {'document': True}})
        
        assert exc_info.value.code == "EMPTY_TEXT"
        assert service._nlu is None

    def test_analyze_text_invalid_features(self, mock_credentials_manager):
        """Test analyzing with invalid features"""
        service = NLUService(mock_credentials_manager)
        
        with pytest.raises(ValidationError) as exc_info:
            service.analyze_text("Sample text", {'invalid_feature': {}})
        
        assert exc_info.value.code == "INVALID_FEATURES"
        assert service._nlu is None
