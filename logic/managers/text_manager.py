import logging
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from backend.services.text_service import TextService
from backend.config.text_config import TextConfig
from ..models.text_request import TextRequest  # Import from models
from ..models.errors import ValidationError
from ..models.responses import TextResponse
from .base_manager import BaseManager
from ..validators.text_validator import TextValidator

class TextManager(BaseManager):
    """Business logic for text processing"""
    
    def __init__(self, text_service: TextService, validator: TextValidator):
        super().__init__()
        self.text_service = text_service
        self.validator = validator

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
            
        except ValidationError as e:
            self.log_error(e)
            return TextResponse(
                text="",
                model_id=request.model_id,
                prompt=request.text,
                parameters_used={},
                error=e.message
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
            prompt_parts.append(request.system_prompt)
        prompt_parts.append(f"Human: {request.text}\n\nAI:")
        return "\n\n".join(prompt_parts)

    def _prepare_params(self, request: TextRequest) -> dict:
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