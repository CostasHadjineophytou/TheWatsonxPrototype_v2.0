class SpeechConfig:
    """Configuration constants for speech services TTS and STT"""
    # STT Configuration
    MAX_AUDIO_SIZE = 100 * 1024 * 1024  # 100MB
    STT_SUPPORTED_FORMATS = ['.wav']  # For now just WAV, can expand later
    
    # TTS Configuration
    MAX_TEXT_LENGTH = 5000
    SUPPORTED_AUDIO_FORMATS = ['audio/wav', 'audio/mp3', 'audio/ogg']
    DEFAULT_VOICE = 'en-US_MichaelV3Voice'
    
    # TTS Parameter Ranges
    PITCH_RANGE = (-100, 100)
    SPEED_RANGE = (-100, 100)
    
    TTS_PARAMS = {
        "pitch": {
            "min": PITCH_RANGE[0],
            "max": PITCH_RANGE[1],
            "default": 0,
            "description": "Voice pitch adjustment in percentage"
        },
        "speed": {
            "min": SPEED_RANGE[0],
            "max": SPEED_RANGE[1],
            "default": 0,
            "description": "Speech rate adjustment in percentage"
        },
        "accept": {
            "default": "audio/wav",
            "options": SUPPORTED_AUDIO_FORMATS,
            "description": "Audio format of the synthesized speech"
        }
    }