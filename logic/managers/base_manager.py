import logging
from typing import Optional
from ..models.errors import LogicError, ValidationError, BusinessError

class BaseManager:
    """Base class for all managers with common functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def log_error(self, error: LogicError) -> None:
        """Log error with consistent format"""
        self.logger.error(
            f"{error.code}: {error.message}",
            extra={"details": error.details}
        )

    def handle_validation_error(self, message: str, details: Optional[dict] = None) -> ValidationError:
        """Handle validation failures"""
        error = ValidationError(message=message, code="VALIDATION_ERROR", details=details)
        self.log_error(error)
        return error

    def handle_business_error(self, message: str, code: str, details: Optional[dict] = None) -> BusinessError:
        """Handle business logic failures"""
        error = BusinessError(message=message, code=code, details=details)
        self.log_error(error)
        return error

    def handle_unknown_error(self, error: Exception, context: str = None) -> LogicError:
        """Handle unexpected errors"""
        message = f"{context}: {str(error)}" if context else str(error)
        logic_error = LogicError(
            message=message,
            code="UNKNOWN_ERROR",
            details={"error_type": error.__class__.__name__}
        )
        self.log_error(logic_error)
        return logic_error 