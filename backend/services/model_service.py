from .base_service import BaseService
from .watson_client import WatsonClient

class ModelService(BaseService):
    """Handles model listing and metadata operations"""
    
    def __init__(self, watson_client: WatsonClient):
        super().__init__()
        self.watson_client = watson_client

    def list_models(self):
        """Get raw model list from Watson"""
        try:
            return self.watson_client.client.foundation_models.get_model_specs()
        except Exception as e:
            raise self.handle_error(e, "Failed to list models")

    def get_model_specs(self, model_id: str):
        """Get detailed specs for a specific model"""
        try:
            self.validator.validate_model_id(model_id)
            models = self.list_models()
            for model in models.get('resources', []):
                if model.get('model_id') == model_id:
                    return model
            return None
        except Exception as e:
            raise self.handle_error(e, "Failed to get model specifications")