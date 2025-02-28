import tkinter as tk
from tkinter import ttk
from frontend.tabs.llm_tab import LLMTab
from frontend.tabs.nlu_tab import NLUTab
from frontend.tabs.speech_tabs import TTSTab, STTTab
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
        self.tts_manager = self.manager_factory.create_tts_manager()
        self.stt_manager = self.manager_factory.create_stt_manager()
        self.audio_manager = self.manager_factory.create_audio_manager()
        
        self._init_ui()
        
    def _init_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Foundation Models tab
        self.llm_tab = LLMTab(
            self.notebook,
            self.text_manager,
            self.model_manager,
            self.project_manager
        )
        self.notebook.add(self.llm_tab, text="Foundation Models")
        
        # Text Analysis tab
        self.nlu_tab = NLUTab(
            self.notebook,
            self.nlu_manager
        )
        self.notebook.add(self.nlu_tab, text="Text Analysis")
        
        # Text-to-Speech tab
        self.tts_tab = TTSTab(
            self.notebook,
            self.tts_manager,
            self.audio_manager
        )
        self.notebook.add(self.tts_tab, text="Text to Speech")
        
        # Speech-to-Text tab
        self.stt_tab = STTTab(
            self.notebook,
            self.stt_manager
        )
        self.notebook.add(self.stt_tab, text="Speech to Text")

    def run(self):
        """Start the application"""
        self.mainloop() 