from dataclasses import dataclass
from typing import Optional
from backend.config.speech_config import SpeechConfig

@dataclass
class TTSRequest:
    """Text-to-Speech request parameters"""
    text: str
    voice: str = SpeechConfig.DEFAULT_VOICE
    pitch: int = SpeechConfig.TTS_PARAMS["pitch"]["default"]
    speed: int = SpeechConfig.TTS_PARAMS["speed"]["default"]
    accept: str = SpeechConfig.TTS_PARAMS["accept"]["default"]

@dataclass
class STTRequest:
    """Speech-to-Text request parameters"""
    audio_path: str 