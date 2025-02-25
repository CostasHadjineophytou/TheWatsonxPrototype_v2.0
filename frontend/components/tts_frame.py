import tkinter as tk
from tkinter import ttk, messagebox
from ..styles.colors import Colors
from logic.models.speech_request import TTSRequest
import os
import subprocess
import platform

class TTSFrame(ttk.Frame):
    """UI frame for Text-to-Speech"""
    
    def __init__(self, parent, tts_manager, audio_manager):
        super().__init__(parent)
        self.tts_manager = tts_manager
        self.audio_manager = audio_manager
        self._init_ui()
        
    def _init_ui(self):
        # Create main panels
        left_panel = ttk.Frame(self)
        left_panel.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        
        right_panel = ttk.Frame(self)
        right_panel.pack(side=tk.RIGHT, fill='y', padx=5, pady=5)
        
        # Left panel - TTS controls
        self._init_tts_controls(left_panel)
        
        # Right panel - Audio history
        self._init_audio_history(right_panel)
        
    def _init_tts_controls(self, parent):
        # Text input
        text_label = ttk.Label(parent, text="Enter text to synthesize:")
        self.text_input = tk.Text(parent, height=5, width=50)
        
        # Voice selection
        voice_label = ttk.Label(parent, text="Voice:")
        self.voice_var = tk.StringVar()
        self.voice_dropdown = ttk.Combobox(
            parent, 
            textvariable=self.voice_var,
            state="readonly",
            width=47
        )
        self._populate_voices()
        
        # Pitch control
        pitch_label = ttk.Label(parent, text="Pitch adjustment (%):")
        self.pitch_var = tk.IntVar(value=0)
        pitch_scale = ttk.Scale(
            parent,
            from_=-100,
            to=100,
            variable=self.pitch_var,
            orient=tk.HORIZONTAL
        )
        
        # Speed control
        speed_label = ttk.Label(parent, text="Speed adjustment (%):")
        self.speed_var = tk.IntVar(value=0)
        speed_scale = ttk.Scale(
            parent,
            from_=-100,
            to=100,
            variable=self.speed_var,
            orient=tk.HORIZONTAL
        )
        
        # Format selection
        format_label = ttk.Label(parent, text="Audio format:")
        self.format_var = tk.StringVar(value="audio/wav")
        format_frame = ttk.Frame(parent)
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
            parent,
            text="Synthesize",
            command=self._synthesize_text
        )
        
        # Progress bar
        self.progress = ttk.Progressbar(
            parent,
            mode='indeterminate',
            length=200
        )
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            parent,
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

    def _play_audio(self, audio_path: str):
        """Play audio file using the appropriate method for the OS"""
        if platform.system() == 'Windows':
            try:
                # Use the default system association to play the file
                os.startfile(os.path.abspath(audio_path))
            except Exception as e:
                try:
                    # Fallback to winsound
                    import winsound
                    winsound.PlaySound(audio_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                except Exception as e:
                    # Last resort
                    subprocess.run(['start', audio_path], shell=True)
        else:
            # For Unix-like systems
            try:
                if platform.system() == 'Darwin':  # macOS
                    subprocess.run(['afplay', audio_path])
                else:  # Linux
                    subprocess.run(['aplay', audio_path])
            except:
                # Fallback for other systems
                subprocess.run(['xdg-open', audio_path])

    def _init_audio_history(self, parent):
        """Initialize audio history panel"""
        # Header
        header = ttk.Label(
            parent,
            text="Recent Synthesized Audio",
            font=('Helvetica', 10, 'bold')
        )
        header.pack(anchor='w', pady=(0, 5))
        
        # History list
        self.history_frame = ttk.Frame(parent)
        self.history_frame.pack(fill='both', expand=True)
        
        # Update history periodically
        self.after(1000, self._update_history)
        
    def _update_history(self):
        """Update audio history display"""
        # Clear existing items
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        # Add current history items
        for audio_info in self.audio_manager.get_history():
            item_frame = ttk.Frame(self.history_frame)
            item_frame.pack(fill='x', pady=2)
            
            # Play button
            play_btn = ttk.Button(
                item_frame,
                text="▶",
                width=3,
                command=lambda p=audio_info['path']: self._play_audio(p)
            )
            play_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Info label
            timestamp = audio_info['timestamp'].strftime("%H:%M:%S")
            text = audio_info['metadata'].get('text', '')[:30] + '...'
            label = ttk.Label(
                item_frame,
                text=f"{timestamp} - {text}"
            )
            label.pack(side=tk.LEFT, fill='x', expand=True)
            
        # Schedule next update
        self.after(1000, self._update_history)
        
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
                pitch=int(self.pitch_var.get()),
                speed=int(self.speed_var.get()),
                accept=self.format_var.get()
            )
            
            response = self.tts_manager.synthesize_speech(request)
            
            if response.error:
                raise Exception(response.error)
            
            # Play audio and add to history
            self.audio_manager.play_audio(
                response.audio_path,
                metadata={'text': text}
            )
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