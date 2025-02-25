from typing import Tuple, TypeVar, Optional
from ..models.errors import LogicError

T = TypeVar('T')  # For generic input type

class BaseValidator:
    """Base class for all validators"""
    
    def validate(self, data: T) -> Tuple[bool, Optional[LogicError]]:
        """
        Base validation method
        Args:
            data: Data to validate
        Returns:
            Tuple of (is_valid, error_if_any)
        """
        raise NotImplementedError()

    def create_error(self, message: str, code: str, details: dict = None) -> LogicError:
        """
        Create standardized error
        Args:
            message: Error message
            code: Error code
            details: Additional error details
        """
        return LogicError(
            message=message,
            code=code,
            details=details
        ) 