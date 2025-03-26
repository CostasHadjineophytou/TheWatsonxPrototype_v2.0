from .utils.error_handler import BaseErrorHandler
from .validators.base_validator import BaseValidator

class BaseComponent:
    """
    Base component for all backend classes
    
    This class composes:
    1. Error handling through BaseErrorHandler
    2. Basic validation through BaseValidator
    
    This design follows composition over inheritance for cleaner separation of concerns.
    """
    
    def __init__(self):
        # Composition: use instances of utility classes rather than inheriting
        self._error_handler = BaseErrorHandler()  # Private, accessed through delegation
        self.validator = BaseValidator()  # Public, accessed directly
    
    def handle_error(self, error: Exception, context: str = None):
        """Delegate error handling to the error handler"""
        return self._error_handler.handle_error(error, context) 