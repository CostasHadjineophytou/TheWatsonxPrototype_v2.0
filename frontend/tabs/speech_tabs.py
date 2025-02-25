import tkinter as tk
from tkinter import ttk
from ..components.tts_frame import TTSFrame
from ..components.stt_frame import STTFrame

class TTSTab(ttk.Frame):
    """Tab for Text-to-Speech functionality"""
    
    def __init__(self, parent, tts_manager):
        super().__init__(parent)
        self.tts_frame = TTSFrame(self, tts_manager)
        self.tts_frame.pack(fill='both', expand=True, padx=5, pady=5)

class STTTab(ttk.Frame):
    """Tab for Speech-to-Text functionality"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_frame = STTFrame(self, stt_manager)
        self.stt_frame.pack(fill='both', expand=True, padx=5, pady=5) 