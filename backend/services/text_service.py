from ibm_watsonx_ai.foundation_models import ModelInference
from backend.services.watson_client import WatsonClient
from backend.utils.errors import BackendError, AuthenticationError, ServiceError, APIError, ValidationError
from backend.validators.service_validator import ServiceValidator
from backend.utils.error_handling import handle_api_error

class TextService:
    """Handles text generation operations"""
    
    def __init__(self, watson_client: WatsonClient):
        self.watson_client = watson_client
        self.validator = ServiceValidator()

    def process_prompt(self, model_id: str, project_id: str, prompt: str, params: dict):
        """Process a prompt using a specific model"""
        try:
            # Validate inputs
            self.validator.validate_model_id(model_id)
            self.validator.validate_project_id(project_id)
            # self.validator.validate_text_params(params)
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
            # Re-raise validation errors or handle them
            print(f"Validation error: {e}")
            raise e
        except Exception as e:
            # Optionally unify to custom errors:
            raise handle_api_error(e) 