from ibm_watsonx_ai.foundation_models import ModelInference
from .watson_client import WatsonClient
from .base_service import BaseService
from ..utils.errors import ValidationError

class TextService(BaseService):
    """Handles text generation operations"""
    
    def __init__(self, watson_client: WatsonClient):
        super().__init__()
        self.watson_client = watson_client

    def process_prompt(self, model_id: str, project_id: str, prompt: str, params: dict):
        """Process a prompt using a specific model"""
        try:
            # Validate inputs
            self.validator.validate_model_id(model_id)
            self.validator.validate_project_id(project_id)
            # Use the Watson-specific parameter validator
            self.validator.validate_watson_text_params(params)
            self.validator.validate_credentials(self.watson_client.credentials)

            # Create model instance
            model = ModelInference(
                model_id=model_id,
                credentials=self.watson_client.credentials,
                project_id=project_id
            )

            # Generate text
            return model.generate_text(prompt=prompt, params=params)

        except ValidationError as e:
            # Re-raise validation errors
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to process text prompt") 