from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class LogicError:
    """Base error class for logic layer"""
    message: str
    code: str
    details: Optional[Dict] = None