import tkinter as tk
from tkinter import ttk

class AboutPopup(tk.Toplevel):
    """Popup window showing information about the application"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("About Watson Services")
        self.geometry("500x400")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_ui()
        
        # Center the window
        self._center_window()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Watson Services Application",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Description
        description = """
        This application provides a user-friendly interface to interact with various IBM Watson services. 
        It allows users to perform text generation, natural language understanding, text-to-speech, and 
        speech-to-text operations using IBM's powerful AI capabilities.
        
        The application is designed to be intuitive and efficient, making it easy to work with Watson 
        services without needing to write complex code or handle API interactions directly.
        """
        
        desc_label = ttk.Label(
            main_frame,
            text=description,
            wraplength=400,
            justify="center"
        )
        desc_label.grid(row=1, column=0, pady=(0, 20))
        
        # Creator information
        creator_frame = ttk.Frame(main_frame)
        creator_frame.grid(row=2, column=0, pady=(0, 20))
        
        creator_label = ttk.Label(
            creator_frame,
            text="Created by:",
            font=("Helvetica", 10, "bold")
        )
        creator_label.pack()
        
        name_label = ttk.Label(
            creator_frame,
            text="Costas Hadjineophytou",
            font=("Helvetica", 12)
        )
        name_label.pack()
        
        # Version
        version_label = ttk.Label(
            main_frame,
            text="Version 2.0",
            font=("Helvetica", 10)
        )
        version_label.grid(row=3, column=0, pady=(0, 20))
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=self.destroy
        ).grid(row=4, column=0)
        
    def _center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
