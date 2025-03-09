import tkinter as tk
from tkinter import ttk, messagebox
from frontend.components.llm_components.model_frame import ModelFrame
from frontend.components.llm_components.parameter_frame import ParameterFrame
from frontend.components.llm_components.project_frame import ProjectFrame
from frontend.components.llm_components.text_frame import TextFrame
from frontend.styles.colors import Colors

class LLMTab(ttk.Frame):
    def __init__(self, parent, text_manager, model_manager, project_manager, status_var=None):
        super().__init__(parent)
        
        # Receive managers from parent
        self.text_manager = text_manager
        self.model_manager = model_manager
        self.project_manager = project_manager
        
        self._init_ui()
    
    def _init_ui(self):
        # Left side - Model selection and parameters
        left_frame = ttk.Frame(self)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)
        
        # Project selection
        self.project_frame = ProjectFrame(left_frame, self.project_manager)
        self.project_frame.pack(fill='x', pady=5)
        
        # Model selection area
        self.model_frame = ModelFrame(left_frame, self.model_manager)
        self.model_frame.pack(fill='x', pady=5)
        
        # Parameter controls
        self.parameter_frame = ParameterFrame(left_frame)
        self.parameter_frame.pack(fill='x', pady=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(left_frame, text="Status")
        status_frame.pack(fill='x', pady=5)
        
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            status_frame, 
            textvariable=self.status_var,
            foreground=Colors.ACCENT,
            padding=5
        )
        self.status_bar.pack(fill='x')
        
        # Right side - Text input/output
        self.text_frame = TextFrame(
            self, 
            self.text_manager,
            self.model_frame,
            self.project_frame,
            self.parameter_frame
        )
        self.text_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
        # Connect model selection to parameter updates
        self.model_frame.bind('<<ModelChanged>>', self.on_model_changed)
        
    def bind_shortcuts(self):
        self.bind_all('<Control-Return>', lambda e: self.text_frame.on_generate())
        self.bind_all('<Control-r>', lambda e: self.refresh_all())
        
    def refresh_all(self):
        """Refresh all components"""
        try:
            self.project_frame.load_projects()
            self.model_frame.load_models()
            self.status_var.set("Refreshed successfully")
        except Exception as e:
            messagebox.showerror("Refresh Error", str(e))
            self.status_var.set("Refresh failed")
        
    def on_model_changed(self, event):
        """Update parameters when model changes"""
        model_id = self.model_frame.get_selected_model()
        if model_id:
            details = self.model_manager.get_model_details(model_id)
            self.parameter_frame.update_for_model(details) 