class SpeechConfig:
    """Configuration for speech services"""
    
    SUPPORTED_AUDIO_FORMATS = ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.wma']
    
    TTS_PARAMS = {
        "pitch": {
            "min": -100,
            "max": 100,
            "default": 0,
            "description": "Voice pitch adjustment in percentage"
        },
        "speed": {
            "min": -100,
            "max": 100,
            "default": 0,
            "description": "Speech rate adjustment in percentage"
        },
        "accept": {
            "default": "audio/wav",
            "options": ["audio/wav", "audio/mp3", "audio/ogg"],
            "description": "Audio format of the synthesized speech"
        }
    }
    
    DEFAULT_VOICE = "en-US_AllisonV3Voice"
    
    MAX_TEXT_LENGTH = 5000  # Maximum characters for synthesis
    MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB max file size 