import tkinter as tk
from tkinter import ttk

class AudioFormatFrame(ttk.Frame):
    """Frame for audio format selection in TTS"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        # Format selection
        format_label = ttk.Label(self, text="Audio format:")
        format_label.pack(anchor='w', padx=10, pady=(10,0))
        
        self.format_var = tk.StringVar(value="audio/wav")
        
        format_frame = ttk.Frame(self)
        format_frame.pack(fill='x', padx=10, pady=5)
        
        # Radio buttons for format selection
        formats = [
            ("WAV", "audio/wav"),
            ("MP3", "audio/mp3"),
            ("OGG", "audio/ogg")
        ]
        
        for text, value in formats:
            ttk.Radiobutton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value
            ).pack(side=tk.LEFT, padx=5)
    
    def get_audio_format(self):
        """Get the selected audio format"""
        return self.format_var.get() 