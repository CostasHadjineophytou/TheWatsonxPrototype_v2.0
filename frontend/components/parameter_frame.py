import tkinter as tk
from tkinter import ttk, messagebox
from backend.config.text_config import TextConfig

class ParameterFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Generation Parameters")
        self.parent = parent
        self._init_ui()
        
    def _init_ui(self):
        # Create scrollable frame
        canvas = tk.Canvas(self, height=400)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Temperature
        self.create_parameter_control(
            "Temperature",
            "temperature",
            TextConfig.DEFAULT_PARAMS["temperature"],
            widget_type="scale",
            min_val=0.0,
            max_val=1.0,
            help_text="Controls randomness in the output (0.0 = deterministic, 1.0 = creative)"
        )
        
        # Max tokens
        self.create_parameter_control(
            "Max Tokens",
            "max_tokens",
            TextConfig.DEFAULT_PARAMS["max_new_tokens"],
            widget_type="entry",
            help_text="Maximum number of tokens to generate"
        )
        
        # Min tokens
        self.create_parameter_control(
            "Min Tokens",
            "min_tokens",
            TextConfig.DEFAULT_PARAMS["min_new_tokens"],
            widget_type="entry",
            help_text="Minimum number of tokens to generate"
        )
        
        # Top P
        self.create_parameter_control(
            "Top P",
            "top_p",
            TextConfig.DEFAULT_PARAMS["top_p"],
            widget_type="scale",
            min_val=0.0,
            max_val=1.0,
            help_text="Nucleus sampling: controls diversity via cumulative probability"
        )
        
        # Top K
        self.create_parameter_control(
            "Top K",
            "top_k",
            TextConfig.DEFAULT_PARAMS["top_k"],
            widget_type="entry",
            help_text="Controls diversity by limiting to k most likely tokens"
        )
        
        # Repetition Penalty
        self.create_parameter_control(
            "Repetition Penalty",
            "repetition_penalty",
            TextConfig.DEFAULT_PARAMS["repetition_penalty"],
            widget_type="scale",
            min_val=1.0,
            max_val=2.0,
            help_text="Penalizes repetition in generated text"
        )
        
        # Random Seed
        self.create_parameter_control(
            "Random Seed",
            "random_seed",
            TextConfig.DEFAULT_PARAMS["random_seed"],
            widget_type="entry",
            help_text="Seed for reproducible generation"
        )
        
        # Stop Sequences
        self.create_parameter_control(
            "Stop Sequences",
            "stop_sequences",
            TextConfig.DEFAULT_PARAMS["stop_sequences"],
            widget_type="entry",
            help_text="Sequences where generation should stop (comma-separated)"
        )

        # Pack the scrollable frame
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_parameter_control(self, label, param_name, default_value, 
                               widget_type="entry", min_val=None, max_val=None,
                               help_text=None):
        """Create a parameter control with label and help tooltip"""
        frame = ttk.Frame(self.scrollable_frame)
        frame.pack(fill='x', padx=5, pady=2)
        
        # Create grid layout
        frame.grid_columnconfigure(1, weight=1)  # Control column expands
        frame.grid_columnconfigure(2, minsize=40)  # Fixed minimum width for help column
        
        # Label
        ttk.Label(frame, text=label).grid(row=0, column=0, sticky='w', padx=(0,10))
        
        # Control container
        control_frame = ttk.Frame(frame)
        control_frame.grid(row=0, column=1, sticky='ew')
        
        if widget_type == "scale":
            var = tk.DoubleVar(value=default_value)
            
            # Scale with native look
            style = ttk.Style()
            style.configure('Param.Horizontal.TScale', sliderlength=15)  # Smaller slider
            
            control = ttk.Scale(
                control_frame,
                from_=min_val,
                to=max_val,
                variable=var,
                orient='horizontal',
                style='Param.Horizontal.TScale'
            )
            control.pack(side='left', fill='x', expand=True)
            
            # Value display
            value_label = ttk.Label(control_frame, width=5)
            value_label.pack(side='left', padx=(5,0))
            
            def on_scale_change(*args):
                value_label.config(text=f"{var.get():.2f}")
            var.trace('w', on_scale_change)
            on_scale_change()
        else:
            var = tk.StringVar(value=str(default_value))
            control = ttk.Entry(control_frame, textvariable=var)
            control.pack(side='left', fill='x', expand=True)
        
        # Help icon - aligned right
        if help_text:
            help_btn = ttk.Label(
                frame, 
                text="?", 
                cursor="question_arrow",
                font=('Segoe UI', 12, 'bold'),
                foreground='gray'
            )
            help_btn.grid(row=0, column=2, sticky='e', padx=(5,0))
            self.create_tooltip(help_btn, help_text)
        
        setattr(self, f"{param_name}_var", var)
        setattr(self, f"{param_name}_control", control)

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = ttk.Label(tooltip, text=text, justify='left',
                            background="#ffffe0", relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)

    def update_for_model(self, model_details):
        """Update parameter limits based on selected model"""
        if not model_details:
            return
            
        print(f"Updating parameters for model: {model_details['name']}")
        
        # Reset all parameters to defaults
        self.temperature_var.set(TextConfig.DEFAULT_PARAMS["temperature"])
        self.max_tokens_var.set(TextConfig.DEFAULT_PARAMS["max_new_tokens"])
        self.min_tokens_var.set(TextConfig.DEFAULT_PARAMS["min_new_tokens"])
        self.top_p_var.set(TextConfig.DEFAULT_PARAMS["top_p"])
        self.top_k_var.set(TextConfig.DEFAULT_PARAMS["top_k"])
        self.repetition_penalty_var.set(TextConfig.DEFAULT_PARAMS["repetition_penalty"])
        self.random_seed_var.set(TextConfig.DEFAULT_PARAMS["random_seed"])
        self.stop_sequences_var.set(str(TextConfig.DEFAULT_PARAMS["stop_sequences"]))
        
        # Then apply model-specific limits
        limits = model_details.get('limits', {})
        
        # Update max tokens limit if specified by model
        max_output = limits.get('max_output_tokens')
        if max_output and hasattr(self, 'max_tokens_var'):
            current = int(self.max_tokens_var.get())
            if current > max_output:
                print(f"Adjusting max tokens from {current} to {max_output}")
                self.max_tokens_var.set(max_output)
        
        # Force UI update
        self.update()
        for widget in self.scrollable_frame.winfo_children():
            widget.update()

    def get_parameters(self):
        """Get all parameter values with validation"""
        try:
            # Validate numeric inputs
            max_tokens = int(self.max_tokens_var.get())
            min_tokens = int(self.min_tokens_var.get())
            top_k = int(self.top_k_var.get())
            random_seed = int(self.random_seed_var.get())
            
            # Get stop sequences as list
            stop_seqs = self.stop_sequences_var.get().split(',')
            stop_seqs = [seq.strip() for seq in stop_seqs if seq.strip()]
            
            return {
                "temperature": self.temperature_var.get(),
                "max_tokens": max_tokens,
                "min_tokens": min_tokens,
                "top_p": self.top_p_var.get(),
                "top_k": top_k,
                "repetition_penalty": self.repetition_penalty_var.get(),
                "random_seed": random_seed,
                "stop_sequences": stop_seqs or TextConfig.DEFAULT_PARAMS["stop_sequences"]
            }
        except ValueError as e:
            raise ValueError("Invalid parameter value. Please check all inputs are correct.") 