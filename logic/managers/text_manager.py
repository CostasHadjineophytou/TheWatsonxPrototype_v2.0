import logging
from dataclasses import dataclass
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from backend.services.text_service import TextService
from backend.config.text_config import TextConfig
from logic.models.text_request import TextRequest
from logic.models.errors import LogicError
from logic.models.responses import TextResponse

@dataclass
class TextRequest:
    """Data class for text generation requests"""
    text: str
    model_id: str
    project_id: str
    temperature: float = TextConfig.DEFAULT_PARAMS["temperature"]
    max_tokens: int = TextConfig.DEFAULT_PARAMS["max_new_tokens"]
    min_tokens: int = TextConfig.DEFAULT_PARAMS["min_new_tokens"]
    top_k: int = TextConfig.DEFAULT_PARAMS["top_k"]
    top_p: float = TextConfig.DEFAULT_PARAMS["top_p"]
    repetition_penalty: float = TextConfig.DEFAULT_PARAMS["repetition_penalty"]
    random_seed: int = TextConfig.DEFAULT_PARAMS["random_seed"]
    stop_sequences: list = None
    system_prompt: str = TextConfig.SYSTEM_PROMPT

class TextManager:
    """Business logic for text processing"""
    
    def __init__(self, text_service: TextService):
        self.text_service = text_service

    def validate_request(self, text: str, model_id: str, project_id: str) -> tuple[bool, str]:
        """Validate text generation request"""
        if not text.strip():
            return False, "Please enter some text to generate"
        if not model_id:
            return False, "Please select a model"
        if not project_id:
            return False, "Please select a project"
        return True, ""

    def process_text(self, request: TextRequest) -> TextResponse:
        """Process text generation request"""
        try:
            # Validate request
            is_valid, error = self.validate_request(
                request.text, 
                request.model_id, 
                request.project_id
            )
            if not is_valid:
                return TextResponse(
                    text="",
                    model_id=request.model_id,
                    prompt=request.text,
                    parameters_used={},
                    error=error
                )

            full_prompt = self._build_prompt(request)
            params = self._prepare_params(request)
            
            result = self.text_service.process_prompt(
                model_id=request.model_id,
                project_id=request.project_id,
                prompt=full_prompt,
                params=params
            )
            
            cleaned_result = self._clean_response(result)
            return TextResponse(
                text=cleaned_result,
                model_id=request.model_id,
                prompt=full_prompt,
                parameters_used=params
            )
        except Exception as e:
            return TextResponse(
                text="",
                model_id=request.model_id,
                prompt=request.text,
                parameters_used={},
                error=str(e)
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