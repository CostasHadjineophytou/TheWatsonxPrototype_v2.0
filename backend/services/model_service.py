from .base_service import BaseService
from .watson_client import WatsonClient
from ..utils.file_manager import FileManager
from ..utils.errors import ValidationError
from ..validators.model_validator import ModelValidator

class ModelService(BaseService):
    """Handles model-related API calls"""
    
    def __init__(self, watson_client: WatsonClient, validator=None):
        super().__init__()
        self.watson_client = watson_client
        self.file_manager = FileManager()
        self.validator = validator or ModelValidator()

    def list_models(self):
        """Get list of all available models"""
        try:

            self.validator.validate_credentials(self.watson_client.credentials)
            
            response = self.watson_client.client.foundation_models.get_model_specs()
            models = response.get('resources', [])
            
            self.file_manager.save_json("data/cloud/models.json", models)
            
            return response
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to list models")

    def get_model_specs(self, model_id: str):
        """Get detailed specs for a specific model"""
        try:
            models = self.list_models()
            for model in models.get('resources', []):
                if model.get('model_id') == model_id:
                    return model
            return None
        except ValidationError as e:
            raise e
        except Exception as e:
            raise self.handle_error(e, "Failed to get model specifications")