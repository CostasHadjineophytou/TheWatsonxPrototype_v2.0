from dataclasses import dataclass
from backend.config.text_config import TextConfig

@dataclass
class TextRequest:
    """Data class for text generation requests"""
    text: str
    model_id: str
    project_id: str
    temperature: float = TextConfig.DEFAULT_PARAMS["temperature"]
    max_tokens: int = TextConfig.DEFAULT_PARAMS["max_new_tokens"]
    stop_sequences: list = None
    system_prompt: str = TextConfig.SYSTEM_PROMPT 