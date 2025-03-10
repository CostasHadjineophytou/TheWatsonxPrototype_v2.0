from typing import List
from backend.services.model_service import ModelService
from logic.models.responses import ModelResponse
from logic.validators.model_validator import ModelValidator
from .base_manager import BaseManager

class ModelManager(BaseManager):
    """Business logic for model operations"""
    
    def __init__(self, model_service: ModelService, validator: ModelValidator):
        super().__init__()
        self.model_service = model_service
        self.validator = validator

    def get_available_models(self) -> List[ModelResponse]:
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
            error = self.handle_business_error(
                message="Failed to fetch models",
                code="MODEL_FETCH_ERROR",
                details={"error": str(e)}
            )
            return [ModelResponse(
                id="ERROR",
                name="Error",
                type="Unknown",
                error=error.message
            )]

    def get_model_details(self, model_id: str) -> ModelResponse:
        """Get detailed model information"""
        try:
            # Validation
            is_valid, error = self.validator.validate(model_id)
            if not is_valid:
                raise self.handle_validation_error(
                    message=error.message,
                    details=error.details
                )
            
            # Business logic
            specs = self.model_service.get_model_specs(model_id)
            if not specs:
                raise self.handle_business_error(
                    message=f"Model {model_id} not found",
                    code="MODEL_NOT_FOUND",
                    details={"model_id": model_id}
                )
            
            return ModelResponse(
                id=specs.get('model_id'),
                name=specs.get('label'),
                type=specs.get('provider'),
                description=specs.get('short_description'),
                long_description=specs.get('long_description'),
                source=specs.get('source'),
                number_params=specs.get('number_params'),
                functions=specs.get('functions'),
                tasks=specs.get('tasks'),
                model_limits=specs.get('model_limits'),
                limits=specs.get('limits'),
                lifecycle=specs.get('lifecycle'),
                versions=specs.get('versions'),
                supported_languages=specs.get('supported_languages')
            )
            
        except Exception as e:
            error = self.handle_unknown_error(e, "Failed to get model details")
            return ModelResponse(
                id="ERROR",
                name="Error",
                type="Unknown",
                error=error.message
            )

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
            'by_provider': {},
            'by_size': {},
            'by_task': {},
            'stats': {
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
            formatted['stats']['providers'].add(model.type)
            
            # Group by size if available
            if model.number_params:
                if model.number_params not in formatted['by_size']:
                    formatted['by_size'][model.number_params] = []
                formatted['by_size'][model.number_params].append(model)
            
            # Group by tasks if available
            if model.tasks:
                for task in model.tasks:
                    task_id = task.get('id')
                    if task_id:
                        if task_id not in formatted['by_task']:
                            formatted['by_task'][task_id] = []
                        formatted['by_task'][task_id].append(model)
                        formatted['stats']['tasks'].add(task_id)
        
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

    def format_model_details(self, details: ModelResponse) -> str:
        """Format complete model details for display"""
        formatted = []
        
        # Basic Information
        formatted.extend([
            f"Model: {details.name}",
            f"Provider: {details.type}",
            f"Source: {details.source or 'N/A'}",
            f"Parameters: {details.number_params or 'N/A'}\n"
        ])
        
        # Description
        if details.description:
            formatted.extend([
                "Description:",
                details.description,
                ""
            ])
        
        if details.long_description:
            formatted.extend([
                "Detailed Description:",
                details.long_description,
                ""
            ])
        
        # Tasks
        if details.tasks:
            formatted.append("Tasks:")
            for task in details.tasks:
                task_id = task.get('id', 'Unknown')
                rating = task.get('ratings', {}).get('quality', 'N/A')
                if rating != 'N/A':
                    formatted.append(f"• {task_id} (Quality Rating: {rating})")
                else:
                    formatted.append(f"• {task_id}")
            formatted.append("")
        
        # Limits
        if details.model_limits:
            formatted.extend([
                "Model Limits:",
                f"• Max Sequence Length: {details.model_limits.get('max_sequence_length', 'N/A')}",
                f"• Max Output Tokens: {details.model_limits.get('max_output_tokens', 'N/A')}\n"
            ])
        
        return "\n".join(formatted)

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

    def get_formatted_sections(self, details: ModelResponse) -> list:
        """Format model details into sections for UI display
        
        Returns a list of tuples (section_title, section_items) where:
        - section_title is a string with the section name
        - section_items is a list of strings with the section content
        """
        sections = []
        
        # Basic Information section
        basic_info_title = "Basic Information"
        basic_info_items = [
            f"Model ID: {details.id}",
            f"Provider: {details.type}",
            f"Source: {details.source or 'N/A'}",
            f"Parameters: {details.number_params or 'N/A'}"
        ]
        sections.append((basic_info_title, basic_info_items))
        
        # Description section
        if details.description or details.long_description:
            description_title = "Description"
            description_items = []
            
            if details.description:
                description_items.append(details.description)
            
            if details.long_description:
                if details.description:  # Add separator if we have both descriptions
                    description_items.append("")
                description_items.append(details.long_description)
                
            sections.append((description_title, description_items))
        
        # Tasks section
        if details.tasks:
            tasks_title = "Supported Tasks"
            tasks_items = []
            
            for task in details.tasks:
                task_id = task.get('id', 'Unknown')
                rating = task.get('ratings', {}).get('quality', 'N/A')
                if rating != 'N/A':
                    tasks_items.append(f"• {task_id} (Quality Rating: {rating})")
                else:
                    tasks_items.append(f"• {task_id}")
                    
            sections.append((tasks_title, tasks_items))
        
        # Model Limits section
        if details.model_limits:
            limits_title = "Model Limits"
            limits_items = [
                f"• Max Sequence Length: {details.model_limits.get('max_sequence_length', 'N/A')}",
                f"• Max Output Tokens: {details.model_limits.get('max_output_tokens', 'N/A')}"
            ]
            sections.append((limits_title, limits_items))
        
        # Supported Languages section
        if details.supported_languages:
            languages_title = "Supported Languages"
            languages_items = [f"• {lang}" for lang in details.supported_languages]
            sections.append((languages_title, languages_items))
        
        # Lifecycle section
        if details.lifecycle:
            lifecycle_title = "Lifecycle"
            lifecycle_items = []
            
            for stage in details.lifecycle:
                stage_id = stage.get('id', 'Unknown')
                start_date = stage.get('start_date', 'N/A')
                lifecycle_items.append(f"• {stage_id} (Start Date: {start_date})")
                
            sections.append((lifecycle_title, lifecycle_items))
            
        return sections 