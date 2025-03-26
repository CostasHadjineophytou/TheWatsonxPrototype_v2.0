from .error_handling import handle_api_error
import logging

class BaseErrorHandler:
    """
    Handles standardized error processing and logging
    
    This class provides error handling functionality to be composed with
    other components rather than inherited from. It builds upon the utility
    functions in error_handling.py by adding:
    
    1. Logging of errors with context
    2. Object-oriented interface for integration with components
    3. Special handling for errors that already have error codes
    
    Use this class when you need error handling within a component.
    For standalone error conversion, use handle_api_error() directly.
    """
    
    def handle_error(self, error: Exception, context: str = None):
        """
        Standardized error handling with logging
        
        Args:
            error: The exception to handle
            context: Optional context information for logging
            
        Returns:
            A standardized BackendError instance
        """
        logging.error(f"{context or 'Error'}: {str(error)}")
        if hasattr(error, 'code'):
            return error
        return handle_api_error(error) 