import tkinter as tk
from tkinter import ttk, messagebox
from ..styles.colors import Colors
from logic.models.speech_request import TTSRequest

class TTSFrame(ttk.Frame):
    """UI frame for Text-to-Speech"""
    
    def __init__(self, parent, tts_manager):
        super().__init__(parent)
        self.tts_manager = tts_manager
        self._init_ui()
        
    def _init_ui(self):
        # Text input
        text_label = ttk.Label(self, text="Enter text to synthesize:")
        self.text_input = tk.Text(self, height=5, width=50)
        
        # Voice selection
        voice_label = ttk.Label(self, text="Voice:")
        self.voice_var = tk.StringVar()
        self.voice_dropdown = ttk.Combobox(
            self, 
            textvariable=self.voice_var,
            state="readonly",
            width=47
        )
        self._populate_voices()
        
        # Pitch control
        pitch_label = ttk.Label(self, text="Pitch adjustment (%):")
        self.pitch_var = tk.IntVar(value=0)
        pitch_scale = ttk.Scale(
            self,
            from_=-100,
            to=100,
            variable=self.pitch_var,
            orient=tk.HORIZONTAL
        )
        
        # Speed control
        speed_label = ttk.Label(self, text="Speed adjustment (%):")
        self.speed_var = tk.IntVar(value=0)
        speed_scale = ttk.Scale(
            self,
            from_=-100,
            to=100,
            variable=self.speed_var,
            orient=tk.HORIZONTAL
        )
        
        # Format selection
        format_label = ttk.Label(self, text="Audio format:")
        self.format_var = tk.StringVar(value="audio/wav")
        format_frame = ttk.Frame(self)
        formats = ["audio/wav", "audio/mp3", "audio/ogg"]
        for fmt in formats:
            ttk.Radiobutton(
                format_frame,
                text=fmt.split('/')[-1].upper(),
                variable=self.format_var,
                value=fmt
            ).pack(side=tk.LEFT, padx=5)
        
        # Synthesize button
        self.synthesize_btn = ttk.Button(
            self,
            text="Synthesize",
            command=self._synthesize_text
        )
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=200
        )
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            foreground=Colors.ACCENT
        )
        
        # Layout
        text_label.pack(anchor='w', padx=10, pady=(10,0))
        self.text_input.pack(fill='x', padx=10, pady=5)
        voice_label.pack(anchor='w', padx=10, pady=(10,0))
        self.voice_dropdown.pack(fill='x', padx=10, pady=5)
        pitch_label.pack(anchor='w', padx=10, pady=(10,0))
        pitch_scale.pack(fill='x', padx=10, pady=5)
        speed_label.pack(anchor='w', padx=10, pady=(10,0))
        speed_scale.pack(fill='x', padx=10, pady=5)
        format_label.pack(anchor='w', padx=10, pady=(10,0))
        format_frame.pack(fill='x', padx=10, pady=5)
        self.synthesize_btn.pack(pady=10)
        self.progress.pack(pady=5)
        self.status_label.pack(pady=5)

    def _populate_voices(self):
        """Populate voice dropdown with available voices"""
        try:
            voices = self.tts_manager.get_available_voices()
            voice_names = [voice['name'] for voice in voices]
            self.voice_dropdown['values'] = voice_names
            self.voice_dropdown.set(voice_names[0] if voice_names else '')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load voices: {str(e)}")

    def _synthesize_text(self):
        """Handle synthesis request"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to synthesize.")
            return
            
        try:
            self._start_synthesis()
            
            request = TTSRequest(
                text=text,
                voice=self.voice_var.get(),
                pitch=self.pitch_var.get(),
                speed=self.speed_var.get(),
                accept=self.format_var.get()
            )
            
            response = self.tts_manager.synthesize_speech(request)
            
            if response.error:
                raise Exception(response.error)
                
            # Play the audio
            import os
            os.system(f"start {response.audio_path}")
            self.status_var.set("Synthesis complete")
            
        except Exception as e:
            messagebox.showerror("Synthesis Error", str(e))
            self.status_var.set("Synthesis failed")
        finally:
            self._end_synthesis()

    def _start_synthesis(self):
        """Show synthesis in progress"""
        self.synthesize_btn.config(state=tk.DISABLED)
        self.synthesize_btn.config(text="Synthesizing...")
        self.progress.start(10)
        self.status_var.set("Synthesizing speech...")
        
    def _end_synthesis(self):
        """End synthesis state"""
        self.synthesize_btn.config(state=tk.NORMAL)
        self.synthesize_btn.config(text="Synthesize")
        self.progress.stop() 