import tkinter as tk
from tkinter import ttk, messagebox
from backend.config.text_config import TextConfig

class SystemPromptFrame(ttk.LabelFrame):
    """Frame for editing the system prompt"""
    
    def __init__(self, parent):
        super().__init__(parent, text="System Prompt")
        self.parent = parent
        self._init_ui()
        
    def _init_ui(self):
        # Container frame
        content_frame = ttk.Frame(self)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Help text
        help_text = "The system prompt defines the AI's behavior and personality."
        help_label = ttk.Label(content_frame, text=help_text, wraplength=250)
        help_label.pack(fill='x', pady=(0, 5))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(content_frame)
        text_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.prompt_text = tk.Text(
            text_frame, 
            height=8, 
            wrap='word',
            yscrollcommand=scrollbar.set
        )
        self.prompt_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.prompt_text.yview)
        
        # Set default system prompt
        self.prompt_text.insert('1.0', TextConfig.SYSTEM_PROMPT)
        
        # Button frame
        button_frame = ttk.Frame(content_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        # Reset button
        reset_btn = ttk.Button(
            button_frame,
            text="Reset to Default",
            command=self._reset_to_default
        )
        reset_btn.pack(side=tk.RIGHT)
    
    def _reset_to_default(self):
        """Reset the system prompt to default"""
        self.prompt_text.delete('1.0', tk.END)
        self.prompt_text.insert('1.0', TextConfig.SYSTEM_PROMPT)
    
    def get_system_prompt(self):
        """Get the current system prompt"""
        return self.prompt_text.get('1.0', 'end-1c').strip()
    
    def set_system_prompt(self, prompt):
        """Set the system prompt"""
        self.prompt_text.delete('1.0', tk.END)
        self.prompt_text.insert('1.0', prompt) 