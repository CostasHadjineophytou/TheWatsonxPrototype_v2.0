import tkinter as tk
from tkinter import ttk
from ..components.tts_components.tts_frame import TTSFrame

class TTSTab(ttk.Frame):
    """Tab for Text-to-Speech functionality"""
    
    def __init__(self, parent, tts_manager, audio_manager, status_var=None):
        super().__init__(parent)
        self.tts_frame = TTSFrame(self, tts_manager, audio_manager)
        self.tts_frame.pack(fill='both', expand=True, padx=5, pady=5)
