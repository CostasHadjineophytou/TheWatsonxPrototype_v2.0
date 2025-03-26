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
        

        info_frame = ttk.Frame(self)
        info_frame.pack(fill='x', padx=5, pady=5)
        info_frame.grid_columnconfigure(0, weight=1)
        
        self.info_label = ttk.Label(
            info_frame,
            wraplength=400,
            justify='left',
            anchor='w'
        )
        self.info_label.grid(row=0, column=0, sticky='ew')
        
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
        """Show details for selected model"""
        selected = self.model_var.get()
        model_id = self.model_manager.get_model_id_by_display_name(selected)
        if model_id:
            self.show_details_window(model_id)
                
    def show_details_window(self, model_id: str):
        # Get model details from manager
        model_details = self.model_manager.get_model_details(model_id)
        
        window = tk.Toplevel(self)
        window.title(f"Model Details: {model_details.name}")
        window.geometry("800x600")
        
        # Create a style for white background
        style = ttk.Style()
        style.configure("White.TFrame", background="white")
        style.configure("White.TLabel", background="white", foreground="black")
        style.configure("WhiteBold.TLabel", background="white", foreground="black", font=('Segoe UI', 11, 'bold'))
        
        # Create main frame
        main_frame = ttk.Frame(window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create canvas for scrolling with explicit background color
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Use a standard tkinter Frame for the scrollable content (it accepts bg parameter)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        # Configure scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Get formatted sections from model manager
        sections = self.model_manager.get_formatted_sections(model_details)
        
        # Create labels for each section - this is UI-specific code
        for section_title, section_items in sections:
            # Section header with explicit colors
            header = tk.Label(
                scrollable_frame,
                text=section_title,
                font=('Segoe UI', 11, 'bold'),
                fg="black",
                bg="white",
                anchor="w",
                justify="left"
            )
            header.pack(anchor='w', pady=(15, 5), fill='x')
            
            # Section content with explicit colors
            for item in section_items:
                is_bullet = item.startswith('•')
                padding = (20, 2) if is_bullet else (10, 2)
                
                content = tk.Label(
                    scrollable_frame,
                    text=item,
                    wraplength=700,
                    justify='left',
                    fg="black",
                    bg="white",
                    anchor="w"
                )
                content.pack(anchor='w', padx=padding, pady=2, fill='x')
        
        # Setup scrolling
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=750)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add close button
        close_button = ttk.Button(window, text="Close", command=window.destroy)
        close_button.pack(pady=10)
        
    def get_selected_model(self):
        selected = self.model_var.get()
        return self.model_manager.get_model_id_by_display_name(selected) 