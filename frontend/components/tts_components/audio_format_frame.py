import tkinter as tk
from tkinter import ttk

class AudioFormatFrame(ttk.Frame):
    """Frame for audio format selection in TTS"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for format settings
        format_container = ttk.LabelFrame(self, text="Audio Format")
        format_container.pack(fill='x', padx=5, pady=5)
        
        # Format selection
        format_frame = ttk.Frame(format_container)
        format_frame.pack(fill='x', padx=10, pady=10)
        
        self.format_var = tk.StringVar(value="audio/wav")
        
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