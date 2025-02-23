import tkinter as tk
from tkinter import ttk
from backend.config.text_config import TextConfig

class ParameterFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Model Parameters")
        self.setup_ui()
        
    def setup_ui(self):
        # Temperature
        ttk.Label(self, text="Temperature:").pack(anchor='w', padx=5)
        self.temp_var = tk.DoubleVar(value=TextConfig.DEFAULT_PARAMS["temperature"])
        self.temp_scale = ttk.Scale(
            self, from_=0.0, to=1.0,
            variable=self.temp_var,
            orient='horizontal'
        )
        self.temp_scale.pack(fill='x', padx=5, pady=2)
        
        # Max tokens
        ttk.Label(self, text="Max Tokens:").pack(anchor='w', padx=5)
        self.max_tokens_var = tk.IntVar(value=TextConfig.DEFAULT_PARAMS["max_new_tokens"])
        self.max_tokens_entry = ttk.Entry(self, textvariable=self.max_tokens_var)
        self.max_tokens_entry.pack(fill='x', padx=5, pady=2)
        
        # Top P
        ttk.Label(self, text="Top P:").pack(anchor='w', padx=5)
        self.top_p_var = tk.DoubleVar(value=TextConfig.DEFAULT_PARAMS["top_p"])
        self.top_p_scale = ttk.Scale(
            self, from_=0.0, to=1.0,
            variable=self.top_p_var,
            orient='horizontal'
        )
        self.top_p_scale.pack(fill='x', padx=5, pady=2)
        
        # Top K
        ttk.Label(self, text="Top K:").pack(anchor='w', padx=5)
        self.top_k_var = tk.IntVar(value=TextConfig.DEFAULT_PARAMS["top_k"])
        self.top_k_entry = ttk.Entry(self, textvariable=self.top_k_var)
        self.top_k_entry.pack(fill='x', padx=5, pady=2)
        
    def validate_parameters(self):
        try:
            max_tokens = self.max_tokens_var.get()
            if max_tokens < 1 or max_tokens > 2048:
                return "Max tokens must be between 1 and 2048"
                
            top_k = self.top_k_var.get()
            if top_k < 1:
                return "Top K must be positive"
                
            return None
        except:
            return "Invalid parameter values"
            
    def get_parameters(self):
        error = self.validate_parameters()
        if error:
            raise ValueError(error)
            
        return {
            "temperature": self.temp_var.get(),
            "max_tokens": self.max_tokens_var.get(),
            "top_p": self.top_p_var.get(),
            "top_k": self.top_k_var.get(),
            "min_tokens": TextConfig.DEFAULT_PARAMS["min_new_tokens"],
            "repetition_penalty": TextConfig.DEFAULT_PARAMS["repetition_penalty"],
            "random_seed": TextConfig.DEFAULT_PARAMS["random_seed"],
            "stop_sequences": TextConfig.DEFAULT_PARAMS["stop_sequences"]
        } 