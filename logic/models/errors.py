from dataclasses import dataclass
from typing import Optional, Dict

class LogicError(Exception):
    """Base error for logic layer"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)

class ValidationError(LogicError):
    """Raised when input validation fails"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message, code=code, details=details)

class BusinessError(LogicError):
    """Raised when business rules are violated"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message, code=code, details=details)

class DataError(LogicError):
    """Raised when data operations fail"""
    pass