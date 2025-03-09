import tkinter as tk
from tkinter import ttk, messagebox
from ...styles.colors import Colors

class TextInputFrame(ttk.Frame):
    """Frame for text input and synthesis control in TTS"""
    
    def __init__(self, parent, tts_manager, audio_manager):
        super().__init__(parent)
        self.tts_manager = tts_manager
        self.audio_manager = audio_manager
        self.parent = parent
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for text input
        input_frame = ttk.LabelFrame(self, text="Text to Speech")
        input_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Text input
        text_label = ttk.Label(input_frame, text="Enter text to synthesize:")
        text_label.pack(anchor='w', padx=10, pady=(10,0))
        
        # Text area with scrollbar
        text_container = ttk.Frame(input_frame)
        text_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        self.text_input = tk.Text(
            text_container, 
            height=15, 
            width=50,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.text_input.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.text_input.yview)
        
        # Button and status frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', padx=10, pady=(5, 10))
        
        # Synthesize button
        self.synthesize_btn = ttk.Button(
            button_frame,
            text="Synthesize",
            command=self.synthesize_text
        )
        self.synthesize_btn.pack(side=tk.LEFT, pady=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            button_frame,
            textvariable=self.status_var,
            foreground=Colors.ACCENT,
            padding=(10, 0)
        )
        self.status_label.pack(side=tk.LEFT, fill='x', expand=True, pady=5)
    
    def get_text(self):
        """Get the current text from the input field"""
        return self.text_input.get("1.0", tk.END).strip()
    
    def synthesize_text(self):
        """Handle synthesis request"""
        try:
            text = self.get_text()
            if not text:
                self.status_var.set("Please enter text to synthesize")
                return
                
            # Start synthesis UI
            self._start_synthesis()
            
            # Get parameters from parent frames
            voice = self.parent.get_voice()
            pitch = self.parent.get_pitch()
            speed = self.parent.get_speed()
            accept = self.parent.get_audio_format()
            
            # Call TTS service
            response = self.tts_manager.synthesize_text(
                text=text,
                voice=voice,
                pitch=pitch,
                speed=speed,
                accept=accept
            )
            
            if response.get('error'):
                raise Exception(response['error'])
            
            # Play the audio
            self.audio_manager.play_audio(
                response['audio_path'],
                metadata={'text': text}
            )
            
            self.status_var.set("Synthesis complete")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Synthesis Error", str(e))
        finally:
            self._end_synthesis()
    
    def _start_synthesis(self):
        """Show synthesis in progress"""
        self.synthesize_btn.config(state=tk.DISABLED)
        self.synthesize_btn.config(text="Synthesizing...")
        self.status_var.set("Synthesizing speech...")
        
    def _end_synthesis(self):
        """End synthesis state"""
        self.synthesize_btn.config(state=tk.NORMAL)
        self.synthesize_btn.config(text="Synthesize") 