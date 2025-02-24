import tkinter as tk
from tkinter import ttk
from frontend.tabs.llm_tab import LLMTab
from frontend.tabs.nlu_tab import NLUTab
from logic.manager_factory import ManagerFactory

class WatsonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Watson Services")
        self.geometry("1200x800")
        
        # Centralized manager creation
        self.manager_factory = ManagerFactory()
        self.text_manager = self.manager_factory.create_text_manager()
        self.model_manager = self.manager_factory.create_model_manager()
        self.project_manager = self.manager_factory.create_project_manager()
        self.nlu_manager = self.manager_factory.create_nlu_manager()
        
        self._init_ui()
        
    def _init_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Inject managers into tabs
        self.llm_tab = LLMTab(
            self.notebook,
            self.text_manager,
            self.model_manager,
            self.project_manager
        )
        self.notebook.add(self.llm_tab, text="Foundation Models")
        
        self.nlu_tab = NLUTab(
            self.notebook,
            self.nlu_manager
        )
        self.notebook.add(self.nlu_tab, text="Text Analysis")
        
        # Placeholder tabs for future services
        for future_tab in ["NLU", "Speech-to-Text", "Text-to-Speech", "Dataset Management"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=future_tab)
            ttk.Label(frame, text=f"{future_tab} - Coming Soon").pack(pady=20)

    def run(self):
        """Start the application"""
        self.mainloop() 