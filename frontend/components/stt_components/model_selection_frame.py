import tkinter as tk
from tkinter import ttk, messagebox

class ModelSelectionFrame(ttk.Frame):
    """Frame for STT model selection"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_manager = stt_manager
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for model selection
        model_container = ttk.LabelFrame(self, text="Speech Recognition Model")
        model_container.pack(fill='x', padx=5, pady=5)
        
        # Model selection
        model_frame = ttk.Frame(model_container)
        model_frame.pack(fill='x', padx=10, pady=10)
        
        model_label = ttk.Label(model_frame, text="Model:")
        model_label.pack(anchor='w', pady=(0, 5))
        
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(
            model_frame, 
            textvariable=self.model_var,
            state="readonly",
            width=30
        )
        self.model_dropdown.pack(fill='x')
        
        # Refresh button
        refresh_btn = ttk.Button(
            model_frame,
            text="Refresh Models",
            command=self._populate_models
        )
        refresh_btn.pack(anchor='e', pady=(5, 0))
        
        # Populate models
        self._populate_models()
    
    def _populate_models(self):
        """Populate model dropdown with available models"""
        try:
            self.model_dropdown.set("Loading models...")
            self.update()
            
            models = self.stt_manager.get_available_models()
            if models:
                self.model_dropdown['values'] = models
                self.model_dropdown.set(models[0] if models else '')
            else:
                self.model_dropdown['values'] = ["No models available"]
                self.model_dropdown.set("No models available")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load models: {str(e)}")
            self.model_dropdown['values'] = ["Error loading models"]
            self.model_dropdown.set("Error loading models")
    
    def get_selected_model(self):
        """Get the selected model"""
        model = self.model_var.get()
        if model in ["Loading models...", "No models available", "Error loading models"]:
            return None
        return model 