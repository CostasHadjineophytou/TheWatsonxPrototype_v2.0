from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class ModelResponse:
    """Formatted model information for frontend"""
    id: str
    name: str
    type: str
    description: Optional[str] = None
    long_description: Optional[str] = None
    source: Optional[str] = None
    number_params: Optional[str] = None
    functions: Optional[List[Dict]] = None
    tasks: Optional[List[Dict]] = None
    model_limits: Optional[Dict] = None
    limits: Optional[Dict] = None
    lifecycle: Optional[List[Dict]] = None
    versions: Optional[List[Dict]] = None
    supported_languages: Optional[List[str]] = None
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
class TextResponse:
    """Formatted text generation response"""
    text: str
    model_id: str
    prompt: str
    parameters_used: Dict
    error: Optional[str] = None

@dataclass
class TTSResponse:
    """Data model for TTS responses"""
    audio_path: str
    error: Optional[str] = None

@dataclass
class STTResponse:
    """Speech-to-Text response"""
    text: str
    audio_path: str
    success: bool = False
    error: Optional[str] = None
    duration: Optional[float] = None  # Audio duration in seconds
    word_count: Optional[int] = None  # Number of transcribed words

@dataclass
class NLUResponse:
    """Natural Language Understanding response"""
    text: str  # Original text analyzed
    features_analyzed: List[str]  # Features that were analyzed
    sentiment: Optional[Dict] = None  # Document-level sentiment
    emotion: Optional[Dict] = None    # Document-level emotions
    entities: Optional[List[Dict]] = None  # Named entities found
    keywords: Optional[List[Dict]] = None  # Key terms extracted
    categories: Optional[List[Dict]] = None  # Content categories
    concepts: Optional[List[Dict]] = None   # High-level concepts
    relations: Optional[List[Dict]] = None  # Semantic relationships
    semantic_roles: Optional[List[Dict]] = None  # Subject-action-object
    error: Optional[str] = None 