import tkinter as tk
from tkinter import ttk, messagebox

class VoiceSelectionFrame(ttk.Frame):
    """Frame for voice selection and parameter adjustments in TTS"""
    
    def __init__(self, parent, tts_manager):
        super().__init__(parent)
        self.tts_manager = tts_manager
        self._init_ui()
        
    def _init_ui(self):
        # Voice selection
        voice_label = ttk.Label(self, text="Voice:")
        voice_label.pack(anchor='w', padx=10, pady=(10,0))
        
        self.voice_var = tk.StringVar()
        self.voice_dropdown = ttk.Combobox(
            self, 
            textvariable=self.voice_var,
            state="readonly",
            width=47
        )
        self.voice_dropdown.pack(fill='x', padx=10, pady=5)
        
        # Pitch control
        pitch_label = ttk.Label(self, text="Pitch adjustment (%):")
        pitch_label.pack(anchor='w', padx=10, pady=(10,0))
        
        self.pitch_var = tk.IntVar(value=0)
        self.pitch_scale = ttk.Scale(
            self,
            from_=-100,
            to=100,
            variable=self.pitch_var,
            orient=tk.HORIZONTAL
        )
        self.pitch_scale.pack(fill='x', padx=10, pady=5)
        
        # Speed control
        speed_label = ttk.Label(self, text="Speed adjustment (%):")
        speed_label.pack(anchor='w', padx=10, pady=(10,0))
        
        self.speed_var = tk.IntVar(value=0)
        self.speed_scale = ttk.Scale(
            self,
            from_=-100,
            to=100,
            variable=self.speed_var,
            orient=tk.HORIZONTAL
        )
        self.speed_scale.pack(fill='x', padx=10, pady=5)
        
        # Populate voices
        self._populate_voices()
    
    def _populate_voices(self):
        """Populate voice dropdown with available voices"""
        try:
            voices = self.tts_manager.get_available_voices()
            voice_names = [voice['name'] for voice in voices]
            self.voice_dropdown['values'] = voice_names
            self.voice_dropdown.set(voice_names[0] if voice_names else '')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load voices: {str(e)}")
    
    def get_voice(self):
        """Get the selected voice"""
        return self.voice_var.get()
    
    def get_pitch(self):
        """Get the pitch adjustment value"""
        return int(self.pitch_var.get())
    
    def get_speed(self):
        """Get the speed adjustment value"""
        return int(self.speed_var.get())
    
    def refresh_voices(self):
        """Refresh the list of available voices"""
        self._populate_voices() 