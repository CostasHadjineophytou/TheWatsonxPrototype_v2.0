from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class ModelResponse:
    """Formatted model information for frontend"""
    id: str
    name: str
    type: str
    description: Optional[str] = None
    parameters: Optional[Dict] = None

@dataclass
class TextResponse:
    """Formatted text generation response"""
    text: str
    model_id: str
    prompt: str
    parameters_used: Dict 

@dataclass
class ProjectResponse:
    """Formatted project information"""
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    error: Optional[str] = None 