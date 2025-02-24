import logging
from logic.models.errors import LogicError, ValidationError, BusinessError, DataError

class BaseManager:
    """Base class for all managers with common functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def log_error(self, error: LogicError):
        """Log error with details"""
        self.logger.error(
            f"{error.code}: {error.message}",
            extra={"details": error.details}
        ) 

    def handle_validation_error(self, message: str, details: dict = None) -> ValidationError:
        """Create and log validation error"""
        error = ValidationError(
            message=message,
            code="VALIDATION_ERROR",
            details=details
        )
        self.log_error(error)
        return error

    def handle_business_error(self, message: str, code: str = None, details: dict = None) -> BusinessError:
        """Create and log business error"""
        error = BusinessError(
            message=message,
            code=code or "BUSINESS_ERROR",
            details=details
        )
        self.log_error(error)
        return error

    def handle_data_error(self, message: str, details: dict = None) -> DataError:
        """Create and log data error"""
        error = DataError(
            message=message,
            code="DATA_ERROR",
            details=details
        )
        self.log_error(error)
        return error

    def handle_unknown_error(self, error: Exception, context: str = None) -> LogicError:
        """Convert unknown error to LogicError"""
        logic_error = LogicError(
            message=f"{context}: {str(error)}" if context else str(error),
            code="UNKNOWN_ERROR",
            details={"error_type": error.__class__.__name__}
        )
        self.log_error(logic_error)
        return logic_error 