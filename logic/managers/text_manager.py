import logging
from typing import Dict, Any
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from backend.services.text_service import TextService
from backend.config.text_config import TextConfig
from ..models.requests import TextRequest
from ..models.responses import TextResponse
from .base_manager import BaseManager
from ..validators.text_validator import TextValidator

class TextManager(BaseManager):
    """Business logic for text processing"""
    
    def __init__(self, text_service: TextService, validator: TextValidator):
        super().__init__()
        self.text_service = text_service
        self.validator = validator

    def generate_text(self, text: str, model_id: str, project_id: str, **params) -> Dict[str, Any]:
        """
        Generate text using simple parameters
        
        Args:
            text: The input text to process
            model_id: The model ID to use
            project_id: The project ID to use
            **params: Additional parameters for text generation
            
        Returns:
            Dictionary with generation results
        """
        # Create TextRequest object from parameters
        request = TextRequest(
            text=text,
            model_id=model_id,
            project_id=project_id,
            **params
        )
        
        # Process the request using the existing method
        response = self.process_text(request)
        
        # Return a dictionary that matches the structure of TextResponse
        result = {
            "text": response.text,
            "model_id": response.model_id,
            "prompt": response.prompt,
            "parameters_used": response.parameters_used
        }
        
        if hasattr(response, "error") and response.error:
            result["error"] = response.error
            
        return result

    def process_text(self, request: TextRequest) -> TextResponse:
        """Process text generation request"""
        try:
            # Validation
            is_valid, error = self.validator.validate(request)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )

            # Prepare request
            full_prompt = self._build_prompt(request)
            params = self._prepare_params(request)
            
            try:
                result = self.text_service.process_prompt(
                    model_id=request.model_id,
                    project_id=request.project_id,
                    prompt=full_prompt,
                    params=params
                )
            except Exception as e:
                raise self.handle_business_error(
                    message="Text generation failed",
                    code="GENERATION_ERROR",
                    details={"error": str(e)}
                )
            
            cleaned_result = self._clean_response(result)
            return TextResponse(
                text=cleaned_result,
                model_id=request.model_id,
                prompt=full_prompt,
                parameters_used=params
            )
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to process text")
            return TextResponse(
                text="",
                model_id=request.model_id,
                prompt=request.text,
                parameters_used={},
                error=error.message
            )

    def _build_prompt(self, request: TextRequest) -> str:
        """Build the complete prompt with system prompt"""
        prompt_parts = []
        if request.system_prompt:
            # Format the system prompt to remove excessive indentation
            system_prompt = self._format_system_prompt(request.system_prompt)
            prompt_parts.append(system_prompt)
        prompt_parts.append(f"Human: {request.text}\n\nAI:")
        return "\n\n".join(prompt_parts)
        
    def _format_system_prompt(self, prompt: str) -> str:
        """Format the system prompt to remove excessive indentation"""
        # Split into lines and remove leading/trailing whitespace
        lines = prompt.strip().split('\n')
        
        # Remove leading spaces from each line
        cleaned_lines = [line.lstrip() for line in lines]
        
        # Join back with newlines
        return '\n'.join(cleaned_lines)

    def _prepare_params(self, request: TextRequest) -> Dict:
        """Prepare model parameters"""
        return {
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.TEMPERATURE: request.temperature,
            GenParams.MAX_NEW_TOKENS: request.max_tokens,
            GenParams.MIN_NEW_TOKENS: request.min_tokens,
            GenParams.TOP_K: request.top_k,
            GenParams.TOP_P: request.top_p,
            GenParams.REPETITION_PENALTY: request.repetition_penalty,
            GenParams.RANDOM_SEED: request.random_seed,
            GenParams.STOP_SEQUENCES: request.stop_sequences or TextConfig.DEFAULT_PARAMS["stop_sequences"]
        }

    def _clean_response(self, response: str) -> str:
        """Clean up the model response"""
        response = response.strip()
        for stop_seq in TextConfig.DEFAULT_PARAMS["stop_sequences"]:
            if stop_seq in response:
                response = response.split(stop_seq)[0]
        return response.strip() 