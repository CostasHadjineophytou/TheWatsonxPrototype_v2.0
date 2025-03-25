from ibm_watsonx_ai.foundation_models import ModelInference
from .watson_client import WatsonClient
from .base_service import BaseService
from ..utils.errors import ValidationError
from ..validators.text_validator import TextValidator
import logging

class TextService(BaseService):
    """Handles text generation operations"""
    
    def __init__(self, watson_client: WatsonClient, validator=None):
        super().__init__()
        self.watson_client = watson_client

        # Override the base validator with the Text-specific validator
        # This gives us both common validation methods and Text-specific ones
        self.validator = validator or TextValidator()
        
    def initialize(self):
        """Validate required resources for text generation"""
        try:
            # Validate required resources
            self.validator.validate_resource(
                required_resources=[
                    "watson-machine-learning",
                    "watson-studio", 
                    "cloud-object-storage"
                ],
                api_key=self.watson_client.credentials.get('apikey'),
                show_all_resources=False
            )
            logging.info("Text service resources validated successfully")
                
        except ValidationError as val_err:
            if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                missing = val_err.details['missing_resources']
                raise ValidationError(
                    message=f"Text generation service not available. Missing resources: {', '.join(missing)}",
                    code="MISSING_TEXT_RESOURCES",
                    details={
                        "missing_resources": missing,
                        "resource_requirements": {
                            "watson-machine-learning": "Required for running AI models",
                            "watson-studio": "Required for project organization",
                            "cloud-object-storage": "Required for data storage"
                        }
                    }
                )
            raise val_err
        except Exception as e:
            raise ValidationError(
                message="Failed to validate text generation resources",
                code="TEXT_RESOURCE_VALIDATION_ERROR",
                details={"error": str(e)}
            )

    def process_prompt(self, model_id: str, project_id: str, prompt: str, params: dict):
        """Process a prompt using a specific model"""
        try:
            # Validate input parameters
            self.validator.validate_prompt(prompt)
            self.validator.validate_watson_text_params(params)
            self.validator.validate_credentials(self.watson_client.credentials)
            
            self.initialize()

            model = ModelInference(
                model_id=model_id,
                credentials=self.watson_client.credentials,
                project_id=project_id
            )

            return model.generate_text(prompt=prompt, params=params)

        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to process text prompt") 