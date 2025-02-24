from ..validators.service_validator import ServiceValidator
from ..utils.errors import BackendError, ServiceError

class BaseService:
    """Base class for all backend services"""
    
    def __init__(self):
        self.validator = ServiceValidator()
    
    def handle_error(self, error: Exception, context: str) -> BackendError:
        """Convert exceptions to BackendError types"""
        if isinstance(error, BackendError):
            return error
            
        return ServiceError(
            message=f"Error in {context}: {str(error)}",
            code="SERVICE_ERROR",
            details={"error": str(error)}
        ) 