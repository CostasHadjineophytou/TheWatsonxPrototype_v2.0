from backend.services.model_service import ModelService
from logic.models.responses import ModelResponse

class ModelManager:
    """Business logic for model operations"""
    
    def __init__(self, model_service: ModelService):
        self.model_service = model_service

    def get_available_models(self):
        """Get formatted list of available models"""
        try:
            raw_models = self.model_service.list_models()
            if isinstance(raw_models, dict):
                models_list = raw_models.get('resources', [])
            else:
                models_list = raw_models if isinstance(raw_models, list) else []
                
            return [
                ModelResponse(
                    id=model.get('model_id', ''),
                    name=model.get('name', 'Unnamed'),
                    type=model.get('type', 'Unknown'),
                    description=model.get('description', '')
                )
                for model in models_list
            ]
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