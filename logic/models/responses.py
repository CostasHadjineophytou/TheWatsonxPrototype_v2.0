from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ModelResponse:
    """Formatted model information for frontend"""
    id: str
    name: str
    type: str
    description: Optional[str] = None
    parameters: Optional[Dict] = None
    error: Optional[str] = None

@dataclass
class TextResponse:
    """Formatted text generation response"""
    text: str
    model_id: str
    prompt: str
    parameters_used: Dict
    error: Optional[str] = None

@dataclass
class ProjectResponse:
    """Formatted project information"""
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    error: Optional[str] = None

@dataclass
class TTSResponse:
    """Text-to-Speech response"""
    audio_path: str
    text: str
    voice: str
    parameters_used: Dict
    error: Optional[str] = None

@dataclass
class STTResponse:
    """Speech-to-Text response"""
    text: str
    audio_path: str
    error: Optional[str] = None 