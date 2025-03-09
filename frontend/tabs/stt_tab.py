import tkinter as tk
from tkinter import ttk
from ..components.stt_components.stt_frame import STTFrame

class STTTab(ttk.Frame):
    """Tab for Speech-to-Text functionality"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_frame = STTFrame(self, stt_manager)
        self.stt_frame.pack(fill='both', expand=True, padx=5, pady=5) 