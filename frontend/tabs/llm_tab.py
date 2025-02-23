import tkinter as tk
from tkinter import ttk, messagebox
from frontend.components.model_frame import ModelFrame
from frontend.components.parameter_frame import ParameterFrame
from frontend.components.project_frame import ProjectFrame
from frontend.components.text_frame import TextFrame
from logic.manager_factory import ManagerFactory
from frontend.styles.colors import Colors

class LLMTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.factory = ManagerFactory()
        self.model_manager = self.factory.create_model_manager()
        self.project_manager = self.factory.create_project_manager()
        self.text_manager = self.factory.create_text_manager()
        
        self.setup_ui()
        
    def setup_ui(self):
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
        self.param_frame = ParameterFrame(left_frame)
        self.param_frame.pack(fill='x', pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            left_frame, 
            textvariable=self.status_var,
            foreground=Colors.ACCENT
        )
        self.status_bar.pack(fill='x', pady=5)
        
        # Right side - Text input/output
        self.text_frame = TextFrame(self, self.text_manager)
        self.text_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
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