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
        model_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Model selection
        model_frame = ttk.Frame(model_container)
        model_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        model_label = ttk.Label(model_frame, text="Select a model:")
        model_label.pack(anchor='w', pady=(0, 5))
        
        # Create a frame for the listbox and scrollbar
        list_frame = ttk.Frame(model_frame)
        list_frame.pack(fill='both', expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Create listbox
        self.model_listbox = tk.Listbox(
            list_frame,
            height=8,
            width=30,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE,
            exportselection=0
        )
        self.model_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Connect scrollbar to listbox
        scrollbar.config(command=self.model_listbox.yview)
        
        # Status label for loading
        self.status_var = tk.StringVar(value="Loading models...")
        status_label = ttk.Label(
            model_frame, 
            textvariable=self.status_var,
            foreground='blue'
        )
        status_label.pack(anchor='w', pady=(5, 0))
        
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
        """Populate listbox with available models"""
        try:
            self.status_var.set("Loading models...")
            self.update()
            
            # Clear current items
            self.model_listbox.delete(0, tk.END)
            
            models = self.stt_manager.get_available_models()
            if models:
                # Add models to listbox
                for model in models:
                    self.model_listbox.insert(tk.END, model)
                
                # Select the first model
                self.model_listbox.selection_set(0)
                self.status_var.set(f"{len(models)} models available")
            else:
                self.model_listbox.insert(tk.END, "No models available")
                self.status_var.set("No models available")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load models: {str(e)}")
            self.model_listbox.insert(tk.END, "Error loading models")
            self.status_var.set("Error loading models")
    
    def get_selected_model(self):
        """Get the selected model"""
        selection = self.model_listbox.curselection()
        if not selection:
            return None
            
        model = self.model_listbox.get(selection[0])
        if model in ["No models available", "Error loading models"]:
            return None
            
        return model 