import tkinter as tk
from tkinter import ttk
from ..components.stt_components.file_selection_frame import FileSelectionFrame
from ..components.stt_components.transcription_control_frame import TranscriptionControlFrame
from ..components.stt_components.transcription_result_frame import TranscriptionResultFrame
from ..components.stt_components.model_selection_frame import ModelSelectionFrame

class STTTab(ttk.Frame):
    """Tab for Speech-to-Text functionality"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_manager = stt_manager
        self._init_ui()
    
    def _init_ui(self):
        # Left panel - File selection, model selection, and controls
        left_panel = ttk.Frame(self)
        left_panel.pack(side=tk.LEFT, fill='y', padx=5, pady=5)
        
        # File selection at the top
        self.file_selection_frame = FileSelectionFrame(left_panel)
        self.file_selection_frame.pack(fill='x', pady=5)
        
        # Transcription controls below file selection
        self.control_frame = TranscriptionControlFrame(self, self.stt_manager)
        self.control_frame.pack(fill='x', pady=5)
        
        # Model selection takes remaining space
        self.model_selection_frame = ModelSelectionFrame(left_panel, self.stt_manager)
        self.model_selection_frame.pack(fill='both', expand=True, pady=5)
        
        # Right panel - Transcription results
        self.result_frame = TranscriptionResultFrame(self)
        self.result_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=5, pady=5)
    
    def get_file_path(self):
        """Get the selected file path"""
        return self.file_selection_frame.get_file_path()
    
    def get_selected_model(self):
        """Get the selected model"""
        return self.model_selection_frame.get_selected_model()
    
    def set_transcription_result(self, text):
        """Set the transcription result text"""
        self.result_frame.set_result(text) 