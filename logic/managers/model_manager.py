from backend.services.model_service import ModelService

class ModelManager:
    """Business logic for model operations"""
    
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def get_available_models(self):
        """Get formatted list of available models"""
        try:
            models = self.model_service.list_models()
            return self._format_models(models)
        except Exception as e:
            return {"error": str(e)}

    def get_model_details(self, model_id: str):
        """Get details for a specific model"""
        try:
            specs = self.model_service.get_model_specs(model_id)
            return self._format_model_specs(specs)
        except Exception as e:
            return {"error": str(e)}

    def _format_models(self, models):
        """Format model list for frontend use"""
        # Format logic here
        pass

    def _format_model_specs(self, specs):
        """Format model specifications for frontend use"""
        # Format logic here
        pass 