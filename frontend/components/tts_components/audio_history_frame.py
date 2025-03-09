import tkinter as tk
from tkinter import ttk

class AudioHistoryFrame(ttk.Frame):
    """Frame for displaying recent synthesized audio in TTS"""
    
    def __init__(self, parent, audio_manager):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self._init_ui()
        
    def _init_ui(self):
        # Header
        header = ttk.Label(
            self,
            text="Recent Synthesized Audio",
            font=('Helvetica', 10, 'bold')
        )
        header.pack(anchor='w', pady=(0, 5))
        
        # History list container
        self.history_frame = ttk.Frame(self)
        self.history_frame.pack(fill='both', expand=True)
        
        # Start periodic updates
        self._update_history()
        
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
                command=lambda p=audio_info['path']: self.audio_manager.play_audio(p)
            )
            play_btn.pack(side=tk.LEFT, padx=(0, 5))
            
            # Info label
            timestamp = audio_info['timestamp'].strftime("%H:%M:%S")
            text = audio_info['metadata'].get('text', '')
            if len(text) > 30:
                text = text[:30] + '...'
                
            label = ttk.Label(
                item_frame,
                text=f"{timestamp} - {text}"
            )
            label.pack(side=tk.LEFT, fill='x', expand=True)
            
        # Schedule next update
        self.after(1000, self._update_history)
    
    def refresh(self):
        """Force refresh of the history display"""
        self._update_history() 