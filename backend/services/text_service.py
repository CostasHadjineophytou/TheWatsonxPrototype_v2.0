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
        self.validator = validator or TextValidator()
        
    def initialize(self):
        """Validate required resources for text generation"""
        try:
            # Try to validate resources but continue even if validation fails
            try:
                self.validator.validate_resource(
                    required_resources=[
                        "watson-machine-learning",
                        "watson-studio", 
                        "cloud-object-storage"
                    ],
                    api_key=self.watson_client.credentials.get('apikey'),
                    show_all_resources=False  # Only enable temporarily for debugging
                )
                logging.info("Text service resources validated successfully")
            except ValidationError as val_err:
                # Log detailed error information about missing resources
                if hasattr(val_err, 'details') and 'missing_resources' in val_err.details:
                    missing = val_err.details['missing_resources']
                    logging.warning(f"Text service validation failed - Missing resources: {', '.join(missing)}")
                    logging.warning(f"Please create these resources in your IBM Cloud account: {', '.join(missing)}")
                    
                    # Provide information about why each resource is needed
                    if "watson-machine-learning" in missing:
                        logging.info("Watson Machine Learning is required for running AI models")
                    if "watson-studio" in missing:
                        logging.info("Watson Studio is required for project organization")
                    if "cloud-object-storage" in missing:
                        logging.info("Cloud Object Storage is required for data storage")
                else:
                    logging.warning(f"Text service validation error: {str(val_err)}")
                # Continue with initialization anyway
            except Exception as ex:
                # For other exceptions, just log the error message
                logging.warning(f"Text service validation encountered an unexpected error: {str(ex)}")
                
        except Exception as e:
            raise ValidationError(
                message="Missing required resources for text generation",
                code="MISSING_TEXT_RESOURCES",
                details={"error": str(e)}
            )

    def process_prompt(self, model_id: str, project_id: str, prompt: str, params: dict):
        """Process a prompt using a specific model"""
        try:
            # Validate input parameters
            self.validator.validate_prompt(prompt)
            self.validator.validate_watson_text_params(params)
            self.validator.validate_credentials(self.watson_client.credentials)
            
            # Validate required resources
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