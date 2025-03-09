from typing import List, Dict
from datetime import datetime
from backend.utils.audio_player import AudioPlayer

class AudioManager:
    """Business logic for audio playback and history"""
    
    def __init__(self, max_history: int = 5):
        self.player = AudioPlayer()
        self.audio_history: List[Dict] = []
        self.max_history = max_history
        
    def play_audio(self, audio_path: str, metadata: dict = None):
        """Play audio and optionally add to history"""
        self.player.play(audio_path)
        if metadata:  # Only add new syntheses to history
            self._add_to_history(audio_path, metadata)
            
    def _add_to_history(self, audio_path: str, metadata: dict):
        """Add audio to history"""
        audio_info = {
            'path': audio_path,
            'timestamp': datetime.now(),
            'metadata': metadata
        }
        self.audio_history.insert(0, audio_info)
        
        # Maintain history limit
        if len(self.audio_history) > self.max_history:
            self.audio_history.pop()
            
    def stop_playback(self):
        """Stop current playback"""
        self.player.stop()
        
    def get_history(self) -> List[Dict]:
        """Get audio playback history"""
        return self.audio_history 