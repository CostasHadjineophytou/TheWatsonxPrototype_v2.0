import tkinter as tk
from tkinter import ttk
from logic.models.responses import ModelResponse

class ModelFrame(ttk.LabelFrame):
    def __init__(self, parent, model_manager):
        super().__init__(parent, text="Model Selection")
        self.model_manager = model_manager
        self.setup_ui()
        
    def setup_ui(self):
        # Model dropdown
        self.model_var = tk.StringVar()
        self.models_combo = ttk.Combobox(
            self, 
            textvariable=self.model_var,
            state="readonly"
        )
        self.models_combo.pack(fill='x', padx=5, pady=5)
        
        # Model info display
        self.info_text = tk.Text(self, height=4, wrap='word')
        self.info_text.pack(fill='x', padx=5, pady=5)
        
        self.load_models()
        self.models_combo.bind('<<ComboboxSelected>>', self.on_model_selected)
        
    def load_models(self):
        models = self.model_manager.get_available_models()
        self.model_list = models
        names = [model.name for model in models if isinstance(model, ModelResponse)]
        self.models_combo['values'] = names
        if names:
            self.models_combo.set(names[0])
            self.on_model_selected(None)
            
    def on_model_selected(self, event):
        selected = self.model_var.get()
        for model in self.model_list:
            if model.name == selected:
                info = f"ID: {model.id}\nType: {model.type}"
                if model.description:
                    info += f"\nDescription: {model.description}"
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert('1.0', info)
                break
                
    def get_selected_model(self):
        selected = self.model_var.get()
        for model in self.model_list:
            if model.name == selected:
                return model.id
        return None 