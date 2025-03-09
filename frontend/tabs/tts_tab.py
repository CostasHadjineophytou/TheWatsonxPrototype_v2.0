import tkinter as tk
from tkinter import ttk
from ..components.tts_components.text_input_frame import TextInputFrame
from ..components.tts_components.voice_selection_frame import VoiceSelectionFrame
from ..components.tts_components.audio_format_frame import AudioFormatFrame
from ..components.tts_components.audio_history_frame import AudioHistoryFrame

class TTSTab(ttk.Frame):
    """Tab for Text-to-Speech functionality"""
    
    def __init__(self, parent, tts_manager, audio_manager):
        super().__init__(parent)
        self.tts_manager = tts_manager
        self.audio_manager = audio_manager
        self._init_ui()
    
    def _init_ui(self):
        # Create main panels
        left_panel = ttk.Frame(self)
        left_panel.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        
        right_panel = ttk.Frame(self)
        right_panel.pack(side=tk.RIGHT, fill='y', padx=5, pady=5)
        
        # Left panel components
        self.voice_selection_frame = VoiceSelectionFrame(left_panel, self.tts_manager)
        self.voice_selection_frame.pack(fill='x', pady=5)
        
        self.audio_format_frame = AudioFormatFrame(left_panel)
        self.audio_format_frame.pack(fill='x', pady=5)
        
        self.text_input_frame = TextInputFrame(self, self.tts_manager, self.audio_manager)
        self.text_input_frame.pack(fill='both', expand=True, pady=5)
        
        # Right panel - Audio history
        self.audio_history_frame = AudioHistoryFrame(right_panel, self.audio_manager)
        self.audio_history_frame.pack(fill='both', expand=True)
    
    def get_voice(self):
        """Get the selected voice"""
        return self.voice_selection_frame.get_voice()
    
    def get_pitch(self):
        """Get the pitch adjustment value"""
        return self.voice_selection_frame.get_pitch()
    
    def get_speed(self):
        """Get the speed adjustment value"""
        return self.voice_selection_frame.get_speed()
    
    def get_audio_format(self):
        """Get the selected audio format"""
        return self.audio_format_frame.get_audio_format()
