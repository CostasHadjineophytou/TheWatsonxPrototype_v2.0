import pytest
from unittest.mock import MagicMock
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from logic.managers.text_manager import TextManager
from logic.models.errors import ValidationError, LogicError
from logic.validators.text_validator import TextValidator
from logic.models.requests import TextRequest
from logic.models.responses import TextResponse
from backend.config.text_config import TextConfig


class TestTextManager:
    """Unit tests for TextManager class"""

    def test_process_text_success(self, setup_text_manager, mock_text_service):
        """Test successful text processing"""
        # Setup mock response
        generated_text = "This is a generated response"
        mock_text_service.process_prompt.return_value = generated_text

        # Execute
        manager = setup_text_manager
        request = TextRequest(
            text="Test prompt",
            model_id="test-model",
            project_id="test-project",
            temperature=0.7,
            max_tokens=100,
            min_tokens=1,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.1,
            random_seed=42,
            stop_sequences=["Human:", "AI:"]
        )
        result = manager.process_text(request)

        # Assert
        assert result.text == generated_text
        assert result.model_id == request.model_id
        assert not result.error
        mock_text_service.process_prompt.assert_called_once()

    def test_process_text_validation_error_empty_text(self, setup_text_manager, mock_text_service):
        """Test text processing with empty text"""
        # Execute
        manager = setup_text_manager
        request = TextRequest(
            text="",  # Invalid empty text
            model_id="test-model",
            project_id="test-project"
        )
        result = manager.process_text(request)

        # Assert
        assert result.text == ""
        assert result.error is not None
        assert "please enter some text to generate" in result.error.lower()
        mock_text_service.process_prompt.assert_not_called()

    def test_process_text_validation_error_missing_model(self, setup_text_manager, mock_text_service):
        """Test text processing with missing model ID"""
        # Execute
        manager = setup_text_manager
        request = TextRequest(
            text="Test prompt",
            model_id="",  # Invalid empty model_id
            project_id="test-project"
        )
        result = manager.process_text(request)

        # Assert
        assert result.text == ""
        assert result.error is not None
        assert "please select a model" in result.error.lower()
        mock_text_service.process_prompt.assert_not_called()

    def test_process_text_service_error(self, setup_text_manager, mock_text_service):
        """Test handling of service error"""
        # Setup error
        mock_text_service.process_prompt.side_effect = Exception("Service error")

        # Execute
        manager = setup_text_manager
        request = TextRequest(
            text="Test prompt",
            model_id="test-model",
            project_id="test-project"
        )
        result = manager.process_text(request)

        # Assert
        assert result.text == ""
        assert result.error is not None
        assert "Failed to process text" in result.error
        mock_text_service.process_prompt.assert_called_once()

    def test_build_prompt_with_system_prompt(self, setup_text_manager):
        """Test prompt building with system prompt"""
        # Setup
        request = TextRequest(
            text="User input",
            system_prompt="System instruction",
            model_id="test-model",
            project_id="test-project"
        )

        # Execute
        manager = setup_text_manager
        result = manager._build_prompt(request)

        # Assert
        assert "System instruction" in result
        assert "Human: User input" in result
        assert "AI:" in result

    def test_build_prompt_without_system_prompt(self, setup_text_manager):
        """Test prompt building without system prompt"""
        # Setup
        request = TextRequest(
            text="User input",
            model_id="test-model",
            project_id="test-project"
        )

        # Execute
        manager = setup_text_manager
        result = manager._build_prompt(request)

        # Assert
        assert "Human: User input" in result
        assert "AI:" in result

    def test_prepare_params(self, setup_text_manager):
        """Test parameter preparation"""
        # Setup
        request = TextRequest(
            text="Test prompt",
            model_id="test-model",
            project_id="test-project",
            temperature=0.7,
            max_tokens=100,
            min_tokens=1,
            top_k=50,
            top_p=0.9,
            repetition_penalty=1.1,
            random_seed=42,
            stop_sequences=["Stop1", "Stop2"]
        )

        # Execute
        manager = setup_text_manager
        params = manager._prepare_params(request)

        # Assert
        assert params[GenParams.DECODING_METHOD] == DecodingMethods.SAMPLE
        assert params[GenParams.TEMPERATURE] == 0.7
        assert params[GenParams.MAX_NEW_TOKENS] == 100
        assert params[GenParams.MIN_NEW_TOKENS] == 1
        assert params[GenParams.TOP_K] == 50
        assert params[GenParams.TOP_P] == 0.9
        assert params[GenParams.REPETITION_PENALTY] == 1.1
        assert params[GenParams.RANDOM_SEED] == 42
        assert params[GenParams.STOP_SEQUENCES] == ["Stop1", "Stop2"]

    def test_clean_response(self, setup_text_manager):
        """Test response cleaning"""
        # Setup
        response = "  Generated text with stop sequence Human: more text  "

        # Execute
        manager = setup_text_manager
        result = manager._clean_response(response)

        # Assert
        assert result == "Generated text with stop sequence"
        assert "Human:" not in result
        assert result == result.strip() 