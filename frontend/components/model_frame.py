import tkinter as tk
from tkinter import ttk

class ModelFrame(ttk.LabelFrame):
    def __init__(self, parent, model_manager):
        super().__init__(parent, text="Model Selection")
        self.model_manager = model_manager
        self._init_ui()
        
    def _init_ui(self):
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
        
        # Model info display - make it fill width
        info_frame = ttk.Frame(self)
        info_frame.pack(fill='x', padx=5, pady=5)
        info_frame.grid_columnconfigure(0, weight=1)  # Make column expandable
        
        self.info_label = ttk.Label(
            info_frame,
            wraplength=400,  # Allow text to wrap
            justify='left',  # Left-align text
            anchor='w'       # Align to west/left
        )
        self.info_label.grid(row=0, column=0, sticky='ew')  # Expand east-west
        
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
        model = self.model_manager.get_model_by_display_name(selected)
        if model:
            self.info_label.config(text=self.model_manager.format_model_info(model))
            self.event_generate('<<ModelChanged>>')

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
        window.title(f"Model Details: {details.name}")
        window.geometry("600x400")
        
        # Create scrollable frame
        container = ttk.Frame(window)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add content using ttk.Labels - using dot notation
        sections = [
            ("Basic Information", [
                f"Model: {details.name}",
                f"Provider: {details.type}",
                f"Source: {details.source if hasattr(details, 'source') else 'N/A'}",
                f"Parameters: {details.parameters if hasattr(details, 'parameters') else 'N/A'}"
            ]),
            ("Description", [details.description or 'N/A']),
            ("Detailed Description", [details.long_description if hasattr(details, 'long_description') else 'N/A']),
            ("Tasks", [', '.join(details.tasks) if hasattr(details, 'tasks') else 'N/A']),
            ("Limits", [
                f"Max Sequence Length: {details.limits.get('max_sequence_length', 'N/A') if hasattr(details, 'limits') else 'N/A'}",
                f"Max Output Tokens: {details.limits.get('max_output_tokens', 'N/A') if hasattr(details, 'limits') else 'N/A'}"
            ])
        ]
        
        # Create labels for each section
        for section_title, section_items in sections:
            # Section header
            header = ttk.Label(scrollable_frame, 
                              text=section_title,
                              style='Header.TLabel',
                              font=('Segoe UI', 10, 'bold'))
            header.pack(anchor='w', pady=(10, 5))
            
            # Section content
            for item in section_items:
                content = ttk.Label(scrollable_frame,
                                  text=item,
                                  wraplength=550,
                                  justify='left')
                content.pack(anchor='w', padx=10)
        
        # Configure scrolling
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw', width=550)
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Pack scrollbar and canvas
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        
        # Add close button
        close_btn = ttk.Button(window, text="Close", command=window.destroy)
        close_btn.pack(pady=5)
        
    def get_selected_model(self):
        selected = self.model_var.get()
        return self.model_manager.get_model_id_by_display_name(selected) 