import tkinter as tk
from tkinter import ttk, filedialog

class FileSelectionFrame(ttk.Frame):
    """Frame for audio file selection in STT"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for file selection
        file_container = ttk.LabelFrame(self, text="Audio File Selection")
        file_container.pack(fill='x', padx=5, pady=5)
        
        # File selection
        file_frame = ttk.Frame(file_container)
        file_frame.pack(fill='x', padx=10, pady=10)
        
        file_label = ttk.Label(file_frame, text="Audio file:")
        file_label.pack(side=tk.LEFT, padx=(0,5))
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(
            file_frame, 
            textvariable=self.file_path_var,
            width=30
        )
        self.file_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        
        browse_btn = ttk.Button(
            file_frame,
            text="Browse",
            command=self._browse_file
        )
        browse_btn.pack(side=tk.LEFT, padx=(5,0))
        
    def _browse_file(self):
        """Open file dialog to select audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac *.ogg *.m4a *.wma"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def get_file_path(self):
        """Get the selected file path"""
        return self.file_path_var.get() 