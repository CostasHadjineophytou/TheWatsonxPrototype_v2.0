from typing import Tuple
from logic.models.text_request import TextRequest
from logic.models.errors import LogicError

class ModelValidator:
    """Validates model-related requests"""
    
    @staticmethod
    def validate_text_request(request: TextRequest) -> Tuple[bool, LogicError]:
        """Validate text generation request"""
        if not request.text.strip():
            return False, LogicError(
                message="Please enter some text to generate",
                code="EMPTY_TEXT"
            )
        if not request.model_id:
            return False, LogicError(
                message="Please select a model",
                code="NO_MODEL"
            )
        if not request.project_id:
            return False, LogicError(
                message="Please select a project",
                code="NO_PROJECT"
            )
        return True, None

    @staticmethod
    def validate_project_request(project_id: str) -> Tuple[bool, LogicError]:
        """Validate project operations"""
        if not project_id:
            return False, LogicError(
                message="Invalid project ID",
                code="INVALID_PROJECT_ID"
            )
        return True, None

    @staticmethod
    def validate_model_request(model_id: str) -> Tuple[bool, LogicError]:
        """Validate model operations"""
        if not model_id:
            return False, LogicError(
                message="Invalid model ID",
                code="INVALID_MODEL_ID"
            )
        return True, None 