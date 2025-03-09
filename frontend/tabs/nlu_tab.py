import tkinter as tk
from tkinter import ttk
from ..components.nlu_components.nlu_frame import NLUFrame

class NLUTab(ttk.Frame):
    """Tab for NLU analysis"""
    
    def __init__(self, parent, nlu_manager, status_var=None):
        super().__init__(parent)
        self.nlu_frame = NLUFrame(self, nlu_manager)
        self.nlu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5) 