from backend.services.watson_client import WatsonClient

class ModelService:
    """Handles model listing and metadata operations"""
    
    def __init__(self, watson_client: WatsonClient):
        self.watson_client = watson_client

    def list_models(self):
        """Get list of available foundation models"""
        try:
            return self.watson_client.client.foundation_models.get_model_specs()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch models: {str(e)}")

    def get_model_specs(self, model_id: str):
        """Get specifications for a specific model."""
        try:
            return self.watson_client.client.foundation_models.get_model_specs(model_id=model_id)
        except Exception as e:
            raise RuntimeError(f"Failed to get model specs: {str(e)}")