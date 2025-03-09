import pytest
from logic.managers.text_manager import TextManager
from logic.models.text_request import TextRequest
from logic.validators.text_validator import TextValidator
from backend.services.text_service import TextService
from backend.services.watson_client import WatsonClient
from backend.services.project_service import ProjectService
from backend.config.text_config import TextConfig
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

class TestTextGenerationEndToEnd:
    """End-to-end tests for text generation functionality"""

    @pytest.fixture
    def setup_text_system(self):
        """Setup text generation components with real service"""
        # Create Watson client first
        watson_client = WatsonClient()
        
        # Get a real project ID
        project_service = ProjectService(watson_client=watson_client)
        projects = project_service.list_projects()
        if not projects:
            raise ValueError("No projects found in IBM Cloud account")
        
        # Get project ID from metadata.guid
        project_id = projects[0]['metadata']['guid']
        
        # Create real service and components
        service = TextService(watson_client=watson_client)
        validator = TextValidator()
        manager = TextManager(text_service=service, validator=validator)
        return manager, project_id

    def test_basic_generation(self, setup_text_system):
        """Test basic text generation with default parameters"""
        manager, project_id = setup_text_system
        
        request = TextRequest(
            text="What is artificial intelligence?",
            model_id="ibm/granite-13b-instruct-v2",  # Using IBM Watson model
            project_id=project_id
        )
        
        response = manager.process_text(request)
        
        # Verify response structure
        assert not response.error
        assert response.text
        assert len(response.text) > 0
        assert response.model_id == request.model_id
        assert response.prompt
        assert response.parameters_used
        
        # Verify default parameters were used
        params = response.parameters_used
        assert params["temperature"] == TextConfig.DEFAULT_PARAMS["temperature"]
        assert params["top_p"] == TextConfig.DEFAULT_PARAMS["top_p"]
        assert params["top_k"] == TextConfig.DEFAULT_PARAMS["top_k"]
        assert params["max_new_tokens"] == TextConfig.DEFAULT_PARAMS["max_new_tokens"]

    def test_generation_with_parameters(self, setup_text_system):
        """Test text generation with custom parameters"""
        manager, project_id = setup_text_system
        
        request = TextRequest(
            text="Explain quantum computing",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            # Testing all available parameters with IBM Watson specific names
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_tokens=200,  # Changed from max_new_tokens to match implementation
            min_tokens=50,   # Changed from min_new_tokens to match implementation
            repetition_penalty=1.2,
            random_seed=123,
            stop_sequences=["Human:", "AI:", "Question:"],
            system_prompt=TextConfig.SYSTEM_PROMPT
        )
        
        response = manager.process_text(request)
        
        # Verify response
        assert not response.error
        assert response.text
        assert len(response.text) > 0
        
        # Verify all custom parameters were used
        params = response.parameters_used
        assert params[GenParams.TEMPERATURE] == 0.7  # Using GenParams enum
        assert params[GenParams.TOP_P] == 0.8
        assert params[GenParams.TOP_K] == 40
        assert params[GenParams.MAX_NEW_TOKENS] == 200
        assert params[GenParams.MIN_NEW_TOKENS] == 50
        assert params[GenParams.REPETITION_PENALTY] == 1.2
        assert params[GenParams.RANDOM_SEED] == 123
        assert params[GenParams.STOP_SEQUENCES] == ["Human:", "AI:", "Question:"]
        assert params[GenParams.DECODING_METHOD] == DecodingMethods.SAMPLE.value  # Compare with string value
        assert TextConfig.SYSTEM_PROMPT in response.prompt

    def test_parameter_boundaries(self, setup_text_system):
        """Test parameter validation at their boundary values"""
        manager, project_id = setup_text_system

        # Test maximum allowed values
        max_request = TextRequest(
            text="Test with maximum parameters",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            temperature=TextConfig.PARAM_RULES["temperature"]["max"],
            top_p=TextConfig.PARAM_RULES["top_p"]["max"],
            top_k=TextConfig.PARAM_RULES["top_k"]["max"],
            max_tokens=TextConfig.PARAM_RULES["max_new_tokens"]["max"],  # Changed parameter name
            min_tokens=TextConfig.PARAM_RULES["min_new_tokens"]["max"],  # Changed parameter name
            repetition_penalty=TextConfig.PARAM_RULES["repetition_penalty"]["max"]
        )
        max_response = manager.process_text(max_request)
        assert not max_response.error
        assert max_response.text

        # Test minimum allowed values
        min_request = TextRequest(
            text="Test with minimum parameters",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            temperature=TextConfig.PARAM_RULES["temperature"]["min"],
            top_p=TextConfig.PARAM_RULES["top_p"]["min"],
            top_k=TextConfig.PARAM_RULES["top_k"]["min"],
            max_tokens=TextConfig.PARAM_RULES["max_new_tokens"]["min"],  # Changed parameter name
            min_tokens=TextConfig.PARAM_RULES["min_new_tokens"]["min"],  # Changed parameter name
            repetition_penalty=TextConfig.PARAM_RULES["repetition_penalty"]["min"]
        )
        min_response = manager.process_text(min_request)
        assert not min_response.error
        assert min_response.text

        # Verify parameters at boundaries are correctly used
        max_params = max_response.parameters_used
        assert max_params[GenParams.TEMPERATURE] == TextConfig.PARAM_RULES["temperature"]["max"]
        assert max_params[GenParams.TOP_P] == TextConfig.PARAM_RULES["top_p"]["max"]
        assert max_params[GenParams.TOP_K] == TextConfig.PARAM_RULES["top_k"]["max"]
        assert max_params[GenParams.MAX_NEW_TOKENS] == TextConfig.PARAM_RULES["max_new_tokens"]["max"]
        assert max_params[GenParams.MIN_NEW_TOKENS] == TextConfig.PARAM_RULES["min_new_tokens"]["max"]
        assert max_params[GenParams.REPETITION_PENALTY] == TextConfig.PARAM_RULES["repetition_penalty"]["max"]

        min_params = min_response.parameters_used
        assert min_params[GenParams.TEMPERATURE] == TextConfig.PARAM_RULES["temperature"]["min"]
        assert min_params[GenParams.TOP_P] == TextConfig.PARAM_RULES["top_p"]["min"]
        assert min_params[GenParams.TOP_K] == TextConfig.PARAM_RULES["top_k"]["min"]
        assert min_params[GenParams.MAX_NEW_TOKENS] == TextConfig.PARAM_RULES["max_new_tokens"]["min"]
        assert min_params[GenParams.MIN_NEW_TOKENS] == TextConfig.PARAM_RULES["min_new_tokens"]["min"]
        assert min_params[GenParams.REPETITION_PENALTY] == TextConfig.PARAM_RULES["repetition_penalty"]["min"]

    def test_system_prompt(self, setup_text_system):
        """Test generation with system prompt"""
        manager, project_id = setup_text_system
        
        request = TextRequest(
            text="What is machine learning?",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            system_prompt="You are an expert in artificial intelligence and machine learning."
        )
        
        response = manager.process_text(request)
        
        # Verify response
        assert not response.error
        assert response.text
        assert len(response.text) > 0
        assert "machine learning" in response.prompt  # Verify prompt includes the question
        assert "artificial intelligence" in response.prompt  # Verify system prompt was included

    def test_different_models(self, setup_text_system):
        """Test generation with different models"""
        manager, project_id = setup_text_system
        
        # Test with first model
        request1 = TextRequest(
            text="What is deep learning?",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id
        )
        response1 = manager.process_text(request1)
        assert not response1.error
        assert response1.text
        
        # Test with second model
        request2 = TextRequest(
            text="What is deep learning?",
            model_id="ibm/granite-3-2b-instruct",
            project_id=project_id
        )
        response2 = manager.process_text(request2)
        assert not response2.error
        assert response2.text

    def test_error_handling(self, setup_text_system):
        """Test error handling with invalid inputs"""
        manager, project_id = setup_text_system
        
        # Test with empty text
        empty_request = TextRequest(
            text="",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id
        )
        empty_response = manager.process_text(empty_request)
        assert empty_response.error
        assert "text" in empty_response.error.lower()
        
        # Test with invalid model ID
        invalid_model_request = TextRequest(
            text="Test text",
            model_id="invalid_model",
            project_id=project_id
        )
        invalid_model_response = manager.process_text(invalid_model_request)
        assert invalid_model_response.error
        
        # Test with invalid parameters
        invalid_params_request = TextRequest(
            text="Test text",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            temperature=3.0  # Invalid temperature
        )
        invalid_params_response = manager.process_text(invalid_params_request)
        assert invalid_params_response.error
        assert "temperature" in invalid_params_response.error.lower()

    def test_response_cleaning(self, setup_text_system):
        """Test response cleaning and formatting"""
        manager, project_id = setup_text_system
        
        request = TextRequest(
            text="Write a short greeting.",
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id
        )
        
        response = manager.process_text(request)
        
        # Verify response cleaning
        assert not response.error
        assert response.text
        assert not response.text.startswith(" ")  # No leading whitespace
        assert not response.text.endswith(" ")  # No trailing whitespace
        assert "Human:" not in response.text  # No conversation markers
        assert "AI:" not in response.text  # No conversation markers

    def test_prompt_format(self, setup_text_system):
        """Test the specific prompt format used by the manager"""
        manager, project_id = setup_text_system
        
        test_text = "What is AI?"
        test_system_prompt = "You are a helpful AI assistant."
        
        request = TextRequest(
            text=test_text,
            model_id="ibm/granite-13b-instruct-v2",
            project_id=project_id,
            system_prompt=test_system_prompt
        )
        
        response = manager.process_text(request)
        
        # Verify prompt format
        assert not response.error
        assert test_system_prompt in response.prompt
        assert f"Human: {test_text}\n\nAI:" in response.prompt