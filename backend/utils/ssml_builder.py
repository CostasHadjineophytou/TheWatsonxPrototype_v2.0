class SSMLBuilder:
    """Utility for building SSML markup"""
    
    @staticmethod
    def build_prosody(text: str, pitch: int = 0, speed: int = 0) -> str:
        """
        Build SSML with prosody controls
        
        Args:
            text: Text to synthesize
            pitch: Voice pitch adjustment (-100 to 100)
            speed: Speech rate adjustment (-100 to 100)
            
        Returns:
            SSML formatted text with prosody tags
        """
        pitch_value = f"{pitch}%".replace('%%', '%')
        speed_value = f"{speed}%".replace('%%', '%')
        return f"<prosody pitch='{pitch_value}' rate='{speed_value}'>{text}</prosody>" 