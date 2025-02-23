import tkinter as tk
from tkinter import ttk
from frontend.tabs.llm_tab import LLMTab

class WatsonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Watson Services")
        self.geometry("1200x800")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create LLM tab
        self.llm_tab = LLMTab(self.notebook)
        self.notebook.add(self.llm_tab, text="Foundation Models")
        
        # Placeholder tabs for future services
        for future_tab in ["NLU", "Speech-to-Text", "Text-to-Speech", "Dataset Management"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=future_tab)
            ttk.Label(frame, text=f"{future_tab} - Coming Soon").pack(pady=20) 