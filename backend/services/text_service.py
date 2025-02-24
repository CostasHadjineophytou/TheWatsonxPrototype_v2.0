from ibm_watsonx_ai.foundation_models import ModelInference
from backend.services.watson_client import WatsonClient
from backend.utils.errors import BackendError, AuthenticationError, ServiceError, APIError
from backend.validators.service_validator import ServiceValidator

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
            self.validator.validate_model_params(params)
            self.validator.validate_credentials(self.watson_client.credentials)

            # Create model instance
            model = ModelInference(
                model_id=model_id,
                credentials=self.watson_client.credentials,
                project_id=project_id
            )

            # Generate text
            return model.generate_text(prompt=prompt, params=params)

        except Exception as e:
            # Convert any IBM Cloud errors to our error types
            if "authentication" in str(e).lower():
                raise AuthenticationError(
                    message=f"Authentication failed: {str(e)}",
                    code="AUTH_FAILED"
                )
            if "rate limit" in str(e).lower():
                raise ServiceError(
                    message=f"Rate limit exceeded: {str(e)}",
                    code="RATE_LIMIT"
                )
            raise APIError(
                message=f"API error: {str(e)}",
                code="API_ERROR"
            ) 