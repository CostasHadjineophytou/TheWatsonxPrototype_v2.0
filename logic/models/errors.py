from dataclasses import dataclass
from typing import Optional

@dataclass
class LogicError:
    """Standard error format for logic layer"""
    message: str
    code: str
    details: Optional[dict] = None 