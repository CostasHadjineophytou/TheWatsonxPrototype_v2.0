import tkinter as tk
from tkinter import ttk, messagebox
from logic.models.text_request import TextRequest

class TextFrame(ttk.Frame):
    def __init__(self, parent, text_manager):
        super().__init__(parent)
        self.text_manager = text_manager
        self.setup_ui()
        
    def setup_ui(self):
        # Input area
        input_frame = ttk.LabelFrame(self, text="Input")
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.input_text = tk.Text(input_frame, height=10, wrap='word')
        self.input_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Control frame for button and progress
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', pady=5)
        
        # Generate button
        self.generate_btn = ttk.Button(
            control_frame, 
            text="Generate",
            command=self.on_generate
        )
        self.generate_btn.pack(side='left', padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side='left', fill='x', expand=True, padx=5)
        
        # Output area
        output_frame = ttk.LabelFrame(self, text="Output")
        output_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(output_frame, height=10, wrap='word', state='disabled')
        self.output_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def start_generation(self):
        """Show generation in progress"""
        self.generate_btn.config(state='disabled')
        self.generate_btn.config(text="Generating...")
        self.progress.start(10)  # Start progress animation
        self.master.status_var.set("Generating text...")
        self.update()
        
    def end_generation(self, success=True):
        """End generation state"""
        self.generate_btn.config(state='normal')
        self.generate_btn.config(text="Generate")
        self.progress.stop()  # Stop progress animation
        self.master.status_var.set("Generation complete" if success else "Generation failed")
        
    def on_generate(self):
        if not self.input_text.get('1.0', 'end-1c').strip():
            messagebox.showwarning("Input Required", "Please enter some text to generate")
            return
            
        # Get project ID
        project_id = self.master.project_frame.get_selected_project()
        if not project_id:
            messagebox.showerror("Error", "Please select a project")
            return
            
        self.start_generation()
        
        try:
            # Get model ID and parameters
            model_id = self.master.model_frame.get_selected_model()
            params = self.master.param_frame.get_parameters()
            
            # Create and process request
            request = TextRequest(
                text=self.input_text.get('1.0', 'end-1c'),
                model_id=model_id,
                project_id=project_id,
                **params
            )
            
            result = self.text_manager.process_text(request)
            
            # Update output
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert('1.0', result.get('result', 'Error generating text'))
            self.output_text.config(state='disabled')
            
            if 'error' in result:
                raise Exception(result['error'])
                
            self.end_generation(success=True)
            
        except Exception as e:
            self.end_generation(success=False)
            messagebox.showerror("Error", str(e))
        finally:
            self.end_generation() 