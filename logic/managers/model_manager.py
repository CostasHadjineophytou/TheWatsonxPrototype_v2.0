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
            models_list = raw_models.get('resources', [])
            
            return [
                ModelResponse(
                    id=model.get('model_id'),
                    name=model.get('label', 'Unnamed'),
                    type=model.get('provider', 'Unknown'),
                    description=model.get('short_description', '')
                )
                for model in models_list
            ]
        except Exception as e:
            return []

    def get_model_details(self, model_id: str):
        """Get detailed model information"""
        specs = self.model_service.get_model_specs(model_id)
        if not specs:
            return None
            
        return {
            'id': specs.get('model_id'),
            'name': specs.get('label'),
            'provider': specs.get('provider'),
            'source': specs.get('source'),
            'description': specs.get('short_description'),
            'long_description': specs.get('long_description'),
            'parameters': specs.get('number_params'),
            'tasks': [task.get('id') for task in specs.get('tasks', [])],
            'limits': specs.get('model_limits', {})
        }

    def _format_models(self, models):
        """Format model list for frontend use"""
        # Format logic here
        pass

    def _format_model_specs(self, specs):
        """Format model specifications for frontend use"""
        # Format logic here
        pass 