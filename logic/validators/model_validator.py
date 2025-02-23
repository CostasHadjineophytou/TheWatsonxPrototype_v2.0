from logic.models.text_request import TextRequest

class ModelValidator:
    """Validates model-related requests"""
    
    @staticmethod
    def validate_text_request(request: TextRequest) -> bool:
        """Validate text generation request"""
        if not request.text or not request.model_id or not request.project_id:
            return False
        return True 