class SpeechConfig:
    """Configuration constants for speech services"""
    MAX_TEXT_LENGTH = 5000
    MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB
    SUPPORTED_AUDIO_FORMATS = ['audio/wav', 'audio/mp3', 'audio/ogg']
    DEFAULT_VOICE = 'en-US_MichaelV3Voice'
    PITCH_RANGE = (-100, 100)
    SPEED_RANGE = (-100, 100)
    
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
            "options": SUPPORTED_AUDIO_FORMATS,
            "description": "Audio format of the synthesized speech"
        }
    }
    
    MAX_TEXT_LENGTH = 5000  # Maximum characters for synthesis
    MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB max file size 