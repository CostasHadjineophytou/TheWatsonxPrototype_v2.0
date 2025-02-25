import pygame
from pathlib import Path
from typing import Callable, Optional
from .errors import AudioError

class AudioPlayer:
    """Handles audio playback functionality"""
    
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Failed to initialize audio: {e}")
        self._current_sound: Optional[pygame.mixer.Sound] = None
        self._is_playing = False
        self._on_complete_callback: Optional[Callable] = None
        
    def play(self, audio_path: str, on_complete: Optional[Callable] = None):
        """Play audio file"""
        try:
            if self._current_sound:
                self.stop()
                
            self._current_sound = pygame.mixer.Sound(audio_path)
            self._current_sound.play()
            self._is_playing = True
            self._on_complete_callback = on_complete
            
        except Exception as e:
            raise AudioError(
                message="Failed to play audio",
                code="AUDIO_PLAYBACK_ERROR",
                details={"error": str(e)}
            )
            
    def stop(self):
        """Stop current playback"""
        if self._current_sound:
            self._current_sound.stop()
            self._is_playing = False
            
    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        return self._is_playing 