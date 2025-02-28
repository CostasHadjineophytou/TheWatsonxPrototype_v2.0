import pytest
from unittest.mock import MagicMock

from logic.managers.nlu_manager import NLUManager
from logic.validators.nlu_validator import NLUValidator
from logic.tests.fixtures.sample_responses import NLU_ANALYSIS_RESULT


class TestNLUIntegration:
    """Integration tests for NLU analysis flow in the logic layer"""

    @pytest.fixture
    def setup_nlu_integration(self):
        """Setup NLU components for logic layer integration testing"""
        # Create mock service that simulates successful responses
        mock_service = MagicMock()
        
        # Setup default success response
        mock_service.analyze_text.return_value = NLU_ANALYSIS_RESULT
        
        # Setup error for invalid requests
        def service_side_effect(text, features):
            if not text or not text.strip():
                raise ValueError("Empty text")
            if not features:
                raise ValueError("No features specified")
            return NLU_ANALYSIS_RESULT
            
        mock_service.analyze_text.side_effect = service_side_effect
        
        # Create validator
        validator = NLUValidator()
        
        # Create manager with real validator but mock service
        manager = NLUManager(nlu_service=mock_service, validator=validator)
        
        return manager

    def test_nlu_analysis_flow(self, setup_nlu_integration):
        """Test basic NLU analysis flow through the logic layer"""
        manager = setup_nlu_integration
        
        # Test with sample text and features
        result = manager.analyze_text(
            text="Sample text for analysis",
            features=["sentiment", "entities", "keywords"]
        )
        
        # Verify response structure and content
        assert "error" not in result
        assert "sentiment" in result
        assert result["sentiment"]["label"] == "positive"
        assert result["sentiment"]["score"] == 0.8
        assert "entities" in result
        assert len(result["entities"]) > 0
        assert result["entities"][0]["text"] == "John"
        assert "keywords" in result
        assert len(result["keywords"]) > 0

    def test_nlu_feature_validation(self, setup_nlu_integration):
        """Test NLU feature validation"""
        manager = setup_nlu_integration
        
        # Test with invalid features
        result = manager.analyze_text(
            text="Test text",
            features=["invalid_feature"]
        )
        assert "error" in result
        assert "invalid features" in result["error"].lower()
        
        # Test with empty features list
        result = manager.analyze_text(
            text="Test text",
            features=[]
        )
        assert "error" in result
        assert "feature" in result["error"].lower()
        
        # Test with 'all' feature
        result = manager.analyze_text(
            text="Test text",
            features=["all"]
        )
        assert "error" not in result
        assert "sentiment" in result
        assert "entities" in result
        assert "keywords" in result

    def test_nlu_text_validation(self, setup_nlu_integration):
        """Test NLU text validation"""
        manager = setup_nlu_integration
        
        # Test with empty text
        result = manager.analyze_text(
            text="",
            features=["sentiment"]
        )
        assert "error" in result
        assert "text is required" in result["error"].lower()
        
        # Test with whitespace text
        result = manager.analyze_text(
            text="   ",
            features=["sentiment"]
        )
        assert "error" in result
        assert "text is required" in result["error"].lower()

    def test_nlu_error_handling(self, setup_nlu_integration):
        """Test NLU error handling in logic layer"""
        manager = setup_nlu_integration
        
        # Mock service to raise an error
        manager.nlu_service.analyze_text.side_effect = Exception("Service error")
        
        # Test service error handling
        result = manager.analyze_text(
            text="Test text",
            features=["sentiment"]
        )
        
        # Verify error handling
        assert "error" in result
        assert "failed" in result["error"].lower()

    def test_nlu_response_transformation(self, setup_nlu_integration):
        """Test NLU response transformation"""
        manager = setup_nlu_integration

        # Override mock response with partial data
        partial_response = {
            "sentiment": {
                "document": {
                    "label": "neutral",
                    "score": 0.5
                }
            }
        }
        # Reset the side effect and set a new return value
        manager.nlu_service.analyze_text.side_effect = None
        manager.nlu_service.analyze_text.return_value = partial_response

        # Test transformation of partial response
        result = manager.analyze_text(
            text="Test text",
            features=["sentiment"]
        )

        # Verify transformation
        assert "error" not in result
        assert "sentiment" in result
        assert result["sentiment"]["label"] == "neutral"
        assert result["sentiment"]["score"] == 0.5
        assert "entities" not in result  # Should not be present in partial response
