import tkinter as tk
from tkinter import ttk, messagebox
from frontend.styles.colors import Colors

class TextFrame(ttk.Frame):
    def __init__(self, parent, text_manager, model_frame, project_frame, parameter_frame):
        super().__init__(parent)
        self.text_manager = text_manager
        self.model_frame = model_frame
        self.project_frame = project_frame
        self.parameter_frame = parameter_frame
        self._init_ui()
        
    def _init_ui(self):
        # Input area
        input_frame = ttk.LabelFrame(self, text="Input")
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.input_text = tk.Text(input_frame, height=10, wrap='word')
        self.input_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Control frame for button and status
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', pady=5)
        
        # Generate button
        self.generate_btn = ttk.Button(
            control_frame, 
            text="Generate",
            command=self.on_generate
        )
        self.generate_btn.pack(side='left', padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            control_frame,
            text="Ready",
            foreground=Colors.ACCENT
        )
        self.status_label.pack(side='left', padx=10)
        
        # Output area
        output_frame = ttk.LabelFrame(self, text="Output")
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(output_frame, height=10, wrap='word', state='disabled')
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def start_generation(self):
        """Show generation in progress"""
        self.generate_btn.config(state='disabled')
        self.generate_btn.config(text="Generating...")
        self.status_label.config(text="Generating text...", foreground="blue")
        self.update()
        
    def end_generation(self, success=True):
        """End generation state"""
        self.generate_btn.config(state='normal')
        self.generate_btn.config(text="Generate")
        
        status_text = "Generation complete" if success else "Generation failed"
        status_color = Colors.SUCCESS if success else Colors.ERROR
        
        self.status_label.config(text=status_text, foreground=status_color)
        
    def on_generate(self):
        try:
            text = self.input_text.get('1.0', 'end-1c')
            model_id = self.model_frame.get_selected_model()
            project_id = self.project_frame.get_selected_project()
            params = self.parameter_frame.get_parameters()
            
            self.start_generation()
            
            result = self.text_manager.generate_text(
                text=text,
                model_id=model_id,
                project_id=project_id,
                **params
            )
            
            if result.get('error'):
                raise Exception(result['error'])
                
            self.update_output(result['text'])
            self.end_generation(success=True)
            
        except Exception as e:
            self.end_generation(success=False)
            messagebox.showerror("Error", str(e))

    def update_output(self, text: str):
        """Update output text area"""
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', text)
        self.output_text.config(state='disabled') 