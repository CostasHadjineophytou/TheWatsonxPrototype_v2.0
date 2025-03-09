import tkinter as tk
from tkinter import ttk

class TranscriptionResultFrame(ttk.Frame):
    """Frame for displaying transcription results in STT"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for transcription results
        result_container = ttk.LabelFrame(self, text="Transcription Results")
        result_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Text area with scrollbar
        text_container = ttk.Frame(result_container)
        text_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.result_text = tk.Text(
            text_container,
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED,
            yscrollcommand=scrollbar.set
        )
        self.result_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.result_text.yview)
    
    def set_result(self, text):
        """Set the transcription result text"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)
    
    def clear_result(self):
        """Clear the transcription result"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED) 