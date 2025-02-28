import pytest
from unittest.mock import MagicMock

from logic.managers.text_manager import TextManager
from logic.models.text_request import TextRequest
from logic.validators.text_validator import TextValidator
from backend.config.text_config import TextConfig


class TestTextIntegration:
    """Integration tests for text generation flow in the logic layer"""

    @pytest.fixture
    def setup_text_integration(self):
        """Setup text generation components for logic layer integration testing"""
        # Create mock service that simulates successful responses
        mock_service = MagicMock()
        
        # Setup default success response
        mock_service.process_prompt.return_value = "Generated response text"
        
        # Setup error for invalid requests
        def service_side_effect(model_id, project_id, prompt, params):
            if not model_id or not project_id:
                raise ValueError("Missing required parameters")
            if not prompt or not prompt.strip():
                raise ValueError("Empty prompt")
            return "Generated response text"
            
        mock_service.process_prompt.side_effect = service_side_effect
        
        # Create validator
        validator = TextValidator()
        
        # Create manager with real validator but mock service
        manager = TextManager(text_service=mock_service, validator=validator)
        
        return manager

    def test_text_generation_flow(self, setup_text_integration):
        """Test basic text generation flow through the logic layer"""
        manager = setup_text_integration
        
        # Create request with required parameters
        request = TextRequest(
            text="Generate a response",
            model_id="test_model",
            project_id="test_project"
        )
        
        # Execute generation
        response = manager.process_text(request)
        
        # Verify response
        assert not response.error
        assert response.text == "Generated response text"
        assert response.model_id == "test_model"
        assert response.prompt
        assert response.parameters_used

    def test_text_parameter_validation(self, setup_text_integration):
        """Test text generation parameter validation"""
        manager = setup_text_integration
        
        # Test with empty text
        empty_request = TextRequest(
            text="",
            model_id="test_model",
            project_id="test_project"
        )
        empty_response = manager.process_text(empty_request)
        assert empty_response.error
        assert "text" in empty_response.error.lower()
        
        # Test with missing model ID
        no_model_request = TextRequest(
            text="Test text",
            model_id="",
            project_id="test_project"
        )
        no_model_response = manager.process_text(no_model_request)
        assert no_model_response.error
        assert "model" in no_model_response.error.lower()
        
        # Test with missing project ID
        no_project_request = TextRequest(
            text="Test text",
            model_id="test_model",
            project_id=""
        )
        no_project_response = manager.process_text(no_project_request)
        assert no_project_response.error
        assert "project" in no_project_response.error.lower()

    def test_text_generation_parameters(self, setup_text_integration):
        """Test text generation with different parameters"""
        manager = setup_text_integration
        
        # Test with custom parameters
        request = TextRequest(
            text="Test with parameters",
            model_id="test_model",
            project_id="test_project",
            temperature=0.8,
            max_tokens=100,
            top_p=0.9,
            top_k=50
        )
        
        response = manager.process_text(request)
        
        # Verify parameters were passed correctly
        assert not response.error
        params = response.parameters_used
        assert params["temperature"] == 0.8
        assert params["max_new_tokens"] == 100
        assert params["top_p"] == 0.9
        assert params["top_k"] == 50

    def test_text_parameter_bounds(self, setup_text_integration):
        """Test parameter bounds validation"""
        manager = setup_text_integration
        
        # Test with out-of-bounds temperature
        invalid_temp_request = TextRequest(
            text="Test text",
            model_id="test_model",
            project_id="test_project",
            temperature=2.5  # Should be between 0 and 2
        )
        temp_response = manager.process_text(invalid_temp_request)
        assert temp_response.error
        assert "temperature" in temp_response.error.lower()
        
        # Test with invalid token range
        invalid_tokens_request = TextRequest(
            text="Test text",
            model_id="test_model",
            project_id="test_project",
            min_tokens=100,
            max_tokens=50  # min should not be greater than max
        )
        tokens_response = manager.process_text(invalid_tokens_request)
        assert tokens_response.error
        assert "token" in tokens_response.error.lower()

    def test_text_error_handling(self, setup_text_integration):
        """Test text generation error handling"""
        manager = setup_text_integration
        
        # Mock service to raise an error
        manager.text_service.process_prompt.side_effect = Exception("Service error")
        
        # Test service error handling
        request = TextRequest(
            text="Test text",
            model_id="test_model",
            project_id="test_project"
        )
        response = manager.process_text(request)
        
        # Verify error handling
        assert response.error
        assert "failed" in response.error.lower()
        assert not response.text
        assert response.parameters_used == {}
