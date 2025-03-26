import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class HomeTab(ttk.Frame):
    """Home tab with large image buttons for navigation"""
    
    def __init__(self, parent, notebook, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.notebook = notebook
        self._create_ui()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Create main container frame with padding
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(expand=True, fill="both")
        
        # Create 2x2 grid for buttons
        for i in range(2):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons with images
        self._create_service_button(main_frame, "Text Generation", "LLM.png", 0, 0)
        self._create_service_button(main_frame, "Natural Language Understanding", "NLU.png", 0, 1)
        self._create_service_button(main_frame, "Text to Speech", "TTS.png", 1, 0)
        self._create_service_button(main_frame, "Speech to Text", "STT.png", 1, 1)
        
    def _create_service_button(self, parent, service_name, image_name, row, col):
        """Create a service button with image"""
        # Create outer frame for the entire button section
        outer_frame = ttk.Frame(parent)
        outer_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        
        # Configure outer frame grid
        outer_frame.grid_rowconfigure(0, weight=1)
        outer_frame.grid_columnconfigure(0, weight=1)
        
        # Create container frame for image and border
        container_frame = ttk.Frame(outer_frame)
        container_frame.grid(row=0, column=0)
        
        # Load and resize image
        image_path = os.path.join("frontend", "assets", "images", image_name)
        try:
            # Load image
            image = Image.open(image_path)
            
            # Fixed size for all images (200x200 pixels)
            fixed_size = (200, 200)
            
            # Create a new image with transparent background
            new_image = Image.new('RGBA', fixed_size, (255, 255, 255, 0))
            
            # Resize image maintaining aspect ratio
            image.thumbnail(fixed_size, Image.Resampling.LANCZOS)
            
            # Calculate position to center the image
            x = (fixed_size[0] - image.size[0]) // 2
            y = (fixed_size[1] - image.size[1]) // 2
            
            # Paste the image onto the transparent background
            new_image.paste(image, (x, y))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(new_image)
            
            # Create a frame with black border
            border_frame = tk.Frame(
                container_frame,
                highlightbackground="black",
                highlightthickness=2,
                bd=0
            )
            border_frame.pack(padx=5, pady=5)
            
            # Create button with image
            button = ttk.Button(
                border_frame,
                image=photo,
                command=lambda: self._navigate_to_tab(service_name),
                style='ImageButton.TButton'
            )
            button.image = photo  # Keep a reference to prevent garbage collection
            button.pack()
            
            # Create and configure button style
            style = ttk.Style()
            style.configure('ImageButton.TButton', padding=0)
            
            # Add service name label below the button
            label = ttk.Label(
                outer_frame,
                text=service_name,
                font=("Helvetica", 12, "bold"),
                #wraplength=200,  # Match image width
                justify="center"
            )
            label.grid(row=1, column=0, pady=(10, 0))
            
        except Exception as e:
            # Fallback to text-only button if image loading fails
            ttk.Button(
                outer_frame,
                text=service_name,
                command=lambda: self._navigate_to_tab(service_name)
            ).grid(row=0, column=0)
            
    def _navigate_to_tab(self, service_name):
        """Navigate to the selected service tab"""
        # Map service names to tab indices
        tab_indices = {
            "Text Generation": 1,  # Index 0 is Home tab
            "Natural Language Understanding": 2,
            "Text to Speech": 3,
            "Speech to Text": 4
        }
        
        # Select the appropriate tab
        self.notebook.select(tab_indices[service_name]) 