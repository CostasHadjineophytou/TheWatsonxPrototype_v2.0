from ..validators.service_validator import ServiceValidator
from ..utils.error_handling import handle_api_error

class BaseService:
    """Base class for all backend services"""
    
    def __init__(self):
        self.validator = ServiceValidator()
    
    def handle_error(self, error: Exception, context: str):
        """Convert exceptions to a consistent format. Optionally use handle_api_error."""
        if hasattr(error, 'code'):
            return error
        
        return handle_api_error(error) 