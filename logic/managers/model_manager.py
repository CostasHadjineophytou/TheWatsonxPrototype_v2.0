from backend.services.model_service import ModelService
from logic.models.responses import ModelResponse
from logic.models.errors import LogicError
from logic.validators.model_validator import ModelValidator
from .base_manager import BaseManager

class ModelManager(BaseManager):
    """Business logic for model operations"""
    
    def __init__(self, model_service: ModelService, validator: ModelValidator):
        super().__init__()
        self.model_service = model_service
        self.validator = validator

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
            self.log_error(LogicError(
                message="Failed to fetch models",
                code="MODEL_FETCH_ERROR",
                details={"error": str(e)}
            ))
            return [ModelResponse(
                id="ERROR",
                name="",
                type="",
                error=f"Failed to fetch models: {str(e)}"
            )]

    def get_model_details(self, model_id: str):
        """Get detailed model information"""
        try:
            is_valid, error = self.validator.validate(model_id)
            if not is_valid:
                raise error
                
            specs = self.model_service.get_model_specs(model_id)
            if not specs:
                raise LogicError(
                    message=f"Model {model_id} not found",
                    code="MODEL_NOT_FOUND"
                )
                
            return {
                'id': specs.get('model_id'),
                'name': specs.get('label'),
                'provider': specs.get('provider'),
                'source': specs.get('source'),
                'description': specs.get('short_description'),
                'long_description': specs.get('long_description'),
                'parameters': specs.get('number_params'),
                'tasks': [task.get('id') for task in specs.get('tasks', [])],
                'limits': specs.get('model_limits', {}),
                'display_name': f"{specs.get('label', 'Unnamed')} ({specs.get('provider', 'Unknown')})"
            }
        except LogicError as e:
            self.log_error(e)
            return None
        except Exception as e:
            self.log_error(LogicError(
                message="Failed to get model details",
                code="MODEL_DETAILS_ERROR",
                details={"model_id": model_id, "error": str(e)}
            ))
            return None

    def format_model_display(self, model: ModelResponse) -> str:
        """Format model for display in UI"""
        return f"{model.name} ({model.type})"

    def format_model_info(self, model: ModelResponse) -> str:
        """Format model info for display"""
        info = [
            f"ID: {model.id}",
            f"Type: {model.type}"
        ]
        if model.description:
            info.append(f"Description: {model.description}")
        return "\n".join(info)

    def _format_models(self, models: list) -> dict:
        """Format model list for advanced use cases"""
        formatted = {
            'by_provider': {},  # Group models by provider
            'by_size': {},      # Group by parameter size
            'by_task': {},      # Group by task type
            'stats': {          # Basic statistics
                'total_count': len(models),
                'providers': set(),
                'tasks': set()
            }
        }
        
        for model in models:
            # Group by provider
            if model.type not in formatted['by_provider']:
                formatted['by_provider'][model.type] = []
            formatted['by_provider'][model.type].append(model)
            
            # Track statistics
            formatted['stats']['providers'].add(model.type)
            
            # Get full details for additional grouping
            details = self.get_model_details(model.id)
            if details:
                # Group by size
                size = details['parameters']
                if size not in formatted['by_size']:
                    formatted['by_size'][size] = []
                formatted['by_size'][size].append(model)
                
                # Group by task
                for task in details['tasks']:
                    if task not in formatted['by_task']:
                        formatted['by_task'][task] = []
                    formatted['by_task'][task].append(model)
                    formatted['stats']['tasks'].add(task)
        
        return formatted

    def _format_model_specs(self, specs: dict) -> dict:
        """Format model specifications with additional metadata"""
        return {
            'basic_info': {
                'name': specs.get('label'),
                'provider': specs.get('provider'),
                'size': specs.get('number_params')
            },
            'capabilities': {
                'tasks': [task.get('id') for task in specs.get('tasks', [])],
                'functions': [fn.get('id') for fn in specs.get('functions', [])]
            },
            'performance': {
                'max_sequence_length': specs.get('model_limits', {}).get('max_sequence_length'),
                'max_output_tokens': specs.get('model_limits', {}).get('max_output_tokens')
            },
            'lifecycle': {
                'status': specs.get('lifecycle', [{}])[0].get('id'),
                'start_date': specs.get('lifecycle', [{}])[0].get('start_date')
            },
            'quotas': {
                'lite': specs.get('limits', {}).get('lite', {}),
                'professional': specs.get('limits', {}).get('v2-professional', {}),
                'standard': specs.get('limits', {}).get('v2-standard', {})
            }
        }

    def format_model_details(self, details: dict) -> str:
        """Format complete model details for display"""
        return f"""Model: {details['name']}
Provider: {details['provider']}
Source: {details['source']}
Parameters: {details['parameters']}

Description:
{details['description']}

Detailed Description:
{details['long_description']}

Tasks: {', '.join(details['tasks'])}

Limits:
Max Sequence Length: {details['limits'].get('max_sequence_length', 'N/A')}
Max Output Tokens: {details['limits'].get('max_output_tokens', 'N/A')}"""

    def get_model_by_display_name(self, display_name: str) -> ModelResponse:
        """Get model by its display name"""
        models = self.get_available_models()
        for model in models:
            if self.format_model_display(model) == display_name:
                return model
        return None

    def get_model_id_by_display_name(self, display_name: str) -> str:
        """Get model ID from display name"""
        model = self.get_model_by_display_name(display_name)
        return model.id if model else None 