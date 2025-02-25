from typing import List, Dict
from datetime import datetime
from backend.utils.audio_player import AudioPlayer

class AudioManager:
    """Manages audio playback and history"""
    
    def __init__(self, max_history: int = 5):
        self.player = AudioPlayer()
        self.max_history = max_history
        self.audio_history: List[Dict] = []
        
    def play_audio(self, audio_path: str, metadata: dict = None):
        """Play audio and add to history"""
        self.player.play(audio_path)
        
        # Add to history
        audio_info = {
            'path': audio_path,
            'timestamp': datetime.now(),
            'metadata': metadata or {}
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