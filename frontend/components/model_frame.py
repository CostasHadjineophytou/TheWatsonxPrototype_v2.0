import tkinter as tk
from tkinter import ttk

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
        names = [self.model_manager.format_model_display(model) for model in models]
        self.models_combo['values'] = names
        if names:
            self.models_combo.set(names[0])
            self.on_model_selected(None)
            
    def on_model_selected(self, event):
        selected = self.model_var.get()
        for model in self.model_list:
            if self.model_manager.format_model_display(model) == selected:
                # Update info text
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert('1.0', self.model_manager.format_model_info(model))
                
                # Always generate event (even on initial load)
                self.event_generate('<<ModelChanged>>')
                break
                
    def show_details(self):
        selected = self.model_var.get()
        for model in self.model_list:
            if self.model_manager.format_model_display(model) == selected:
                details = self.model_manager.get_model_details(model.id)
                if details:
                    self.show_details_window(details)
                break
                
    def show_details_window(self, details):
        window = tk.Toplevel(self)
        window.title(f"Model Details: {details['name']}")
        window.geometry("600x400")
        
        # Create a frame with scrollbar
        frame = ttk.Frame(window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side='right', fill='y')
        
        # Use Text widget in read-only mode for scrolling capability
        # (ttk.Label doesn't support scrolling)
        text = tk.Text(frame, 
                       wrap='word',
                       yscrollcommand=scrollbar.set,
                       borderwidth=0,  # Remove border
                       highlightthickness=0,  # Remove highlight border
                       cursor="arrow")  # Use normal cursor instead of text cursor
        text.pack(side='left', fill='both', expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=text.yview)
        
        # Get formatted details from manager
        content = self.model_manager.format_model_details(details)
        text.insert('1.0', content)
        
        # Make it read-only
        text.config(state='disabled')
        
        # Add close button at bottom
        close_btn = ttk.Button(window, text="Close", command=window.destroy)
        close_btn.pack(pady=5)
        
    def get_selected_model(self):
        selected = self.model_var.get()
        for model in self.model_list:
            if self.model_manager.format_model_display(model) == selected:
                return model.id
        return None 