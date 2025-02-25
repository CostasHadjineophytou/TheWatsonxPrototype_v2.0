from dataclasses import dataclass
from typing import Optional, List
from backend.config.text_config import TextConfig

@dataclass
class TextRequest:
    """Text generation request parameters"""
    text: str
    model_id: str
    project_id: str
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    min_tokens: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    random_seed: Optional[int] = None
    stop_sequences: Optional[List[str]] = None

    # Optional fields with defaults from TextConfig
    temperature: float = TextConfig.DEFAULT_PARAMS["temperature"]
    max_tokens: int = TextConfig.DEFAULT_PARAMS["max_new_tokens"]
    top_p: float = TextConfig.DEFAULT_PARAMS["top_p"]
    top_k: int = TextConfig.DEFAULT_PARAMS["top_k"]
    min_tokens: int = TextConfig.DEFAULT_PARAMS["min_new_tokens"]
    repetition_penalty: float = TextConfig.DEFAULT_PARAMS["repetition_penalty"]
    random_seed: int = TextConfig.DEFAULT_PARAMS["random_seed"]
    stop_sequences: Optional[List[str]] = None
    system_prompt: str = TextConfig.SYSTEM_PROMPT 