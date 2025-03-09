import tkinter as tk
from tkinter import ttk

class AudioHistoryFrame(ttk.Frame):
    """Frame for displaying recent synthesized audio in TTS"""
    
    def __init__(self, parent, audio_manager):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for better visual separation
        self.history_container = ttk.LabelFrame(self, text="Recent Synthesized Audio")
        self.history_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # History list container with scrollbar
        history_container = ttk.Frame(self.history_container)
        history_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(history_container)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(history_container, width=250)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)
        
        # Connect scrollbar to canvas
        scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas to hold history items
        self.history_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.history_frame, anchor='nw')
        
        # Configure the history frame to expand to fill canvas
        self.history_frame.bind('<Configure>', self._on_frame_configure)
        
        # Start periodic updates
        self._update_history()
    
    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
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
            if len(text) > 25:
                text = text[:25] + '...'
                
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