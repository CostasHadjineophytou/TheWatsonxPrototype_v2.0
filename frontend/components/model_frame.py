import tkinter as tk
from tkinter import ttk
from logic.models.responses import ModelResponse

class ModelFrame(ttk.LabelFrame):
    def __init__(self, parent, model_manager):
        super().__init__(parent, text="Model Selection")
        self.model_manager = model_manager
        self.setup_ui()
        
    def setup_ui(self):
        # Model selection frame
        selection_frame = ttk.Frame(self)
        selection_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Select Model:").pack(side='left')
        
        # Model dropdown
        self.model_var = tk.StringVar()
        self.models_combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.model_var,
            state="readonly",
            width=40
        )
        self.models_combo.pack(side='left', padx=5)
        
        # Details button
        self.details_btn = ttk.Button(
            selection_frame,
            text="View Details",
            command=self.show_details
        )
        self.details_btn.pack(side='left', padx=5)
        
        # Model info display
        self.info_text = tk.Text(self, height=6, wrap='word')
        self.info_text.pack(fill='x', padx=5, pady=5)
        
        self.load_models()
        self.models_combo.bind('<<ComboboxSelected>>', self.on_model_selected)
        
    def load_models(self):
        models = self.model_manager.get_available_models()
        self.model_list = models
        names = [f"{model.name} ({model.type})" for model in models]
        self.models_combo['values'] = names
        if names:
            self.models_combo.set(names[0])
            self.on_model_selected(None)
            
    def on_model_selected(self, event):
        selected = self.model_var.get()
        for model in self.model_list:
            if f"{model.name} ({model.type})" == selected:
                info = f"ID: {model.id}\nType: {model.type}"
                if model.description:
                    info += f"\nDescription: {model.description}"
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert('1.0', info)
                break
                
    def show_details(self):
        selected = self.model_var.get()
        for model in self.model_list:
            if f"{model.name} ({model.type})" == selected:
                details = self.model_manager.get_model_details(model.id)
                if details:
                    self.show_details_window(details)
                break
                
    def show_details_window(self, details):
        window = tk.Toplevel(self)
        window.title(f"Model Details: {details['name']}")
        window.geometry("600x400")
        
        text = tk.Text(window, wrap='word', padx=10, pady=10)
        text.pack(fill='both', expand=True)
        
        # Format details
        content = f"""Model: {details['name']}
Provider: {details['provider']}
Source: {details['source']}
Parameters: {details['parameters']}

Description:
{details['description']}

Detailed Description:
{details['long_description']}

Tasks: {', '.join(details['tasks'])}

Limits:
Max Sequence Length: {details['limits'].get('max_sequence_length', 'N/A')}
Max Output Tokens: {details['limits'].get('max_output_tokens', 'N/A')}
"""
        text.insert('1.0', content)
        text.config(state='disabled')
        
    def get_selected_model(self):
        selected = self.model_var.get()
        for model in self.model_list:
            if f"{model.name} ({model.type})" == selected:
                return model.id
        return None 