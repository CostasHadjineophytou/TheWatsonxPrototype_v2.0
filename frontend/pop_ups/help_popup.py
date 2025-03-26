import tkinter as tk
from tkinter import ttk

class HelpPopup(tk.Toplevel):
    """Popup window showing help information about the services"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Help - Watson Services")
        self.geometry("600x700")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Create UI
        self._create_ui()
        
        # Center the window
        self._center_window()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Content frame with padding
        content_frame = ttk.Frame(scrollable_frame, padding="20")
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            content_frame,
            text="Watson Services Help",
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Service descriptions
        services = [
            {
                "title": "Text Generation (LLM)",
                "description": """
                The Text Generation service uses IBM's foundation models to generate human-like text based on your prompts.
                
                Features:
                • Generate text from simple prompts
                • Control output parameters (temperature, max tokens, etc.)
                • Support for multiple foundation models
                • Project-based organization
                
                Use this service when you need to:
                • Generate creative content
                • Get AI-powered text responses
                • Create automated text generation workflows
                """,
                "requirements": "Requires Watson Machine Learning and Watson Studio resources"
            },
            {
                "title": "Natural Language Understanding (NLU)",
                "description": """
                The Natural Language Understanding service analyzes text to extract meaning and insights.
                
                Features:
                • Entity recognition
                • Sentiment analysis
                • Keyword extraction
                • Concept tagging
                • Emotion detection
                
                Use this service when you need to:
                • Analyze customer feedback
                • Extract key information from text
                • Understand text sentiment and emotions
                • Identify important entities and concepts
                """,
                "requirements": "Requires Natural Language Understanding resource"
            },
            {
                "title": "Text to Speech (TTS)",
                "description": """
                The Text to Speech service converts written text into natural-sounding speech.
                
                Features:
                • Multiple voice options
                • Adjustable speech parameters (pitch, speed)
                • Support for multiple languages
                • SSML (Speech Synthesis Markup Language) support
                
                Use this service when you need to:
                • Create audio from text
                • Generate voice prompts
                • Create audio content
                • Build voice-enabled applications
                """,
                "requirements": "Requires Text to Speech resource"
            },
            {
                "title": "Speech to Text (STT)",
                "description": """
                The Speech to Text service converts spoken audio into written text.
                
                Features:
                • Real-time transcription
                • Multiple language support
                • Custom language models
                • Speaker diarization
                
                Use this service when you need to:
                • Transcribe audio recordings
                • Create text from speech
                • Build voice command applications
                • Generate transcripts
                """,
                "requirements": "Requires Speech to Text resource"
            }
        ]
        
        # Add each service section
        for i, service in enumerate(services, start=1):
            # Service title
            service_title = ttk.Label(
                content_frame,
                text=service["title"],
                font=("Helvetica", 12, "bold")
            )
            service_title.grid(row=i*3-2, column=0, sticky=tk.W, pady=(20, 5))
            
            # Service description
            service_desc = ttk.Label(
                content_frame,
                text=service["description"],
                wraplength=550,
                justify="left"
            )
            service_desc.grid(row=i*3-1, column=0, sticky=tk.W, pady=(0, 5))
            
            # Requirements
            requirements = ttk.Label(
                content_frame,
                text=service["requirements"],
                font=("Helvetica", 9, "italic")
            )
            requirements.grid(row=i*3, column=0, sticky=tk.W, pady=(0, 10))
        
        # Close button
        ttk.Button(
            content_frame,
            text="Close",
            command=self.destroy
        ).grid(row=len(services)*3+1, column=0, pady=(20, 0))
        
    def _center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
