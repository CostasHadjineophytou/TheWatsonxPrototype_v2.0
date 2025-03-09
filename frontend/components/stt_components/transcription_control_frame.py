import tkinter as tk
from tkinter import ttk, messagebox
from ...styles.colors import Colors

class TranscriptionControlFrame(ttk.Frame):
    """Frame for transcription controls in STT"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_manager = stt_manager
        self.parent = parent
        self._init_ui()
        
    def _init_ui(self):
        # Create a labeled frame for transcription controls
        control_frame = ttk.LabelFrame(self, text="Transcription Controls")
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Button and status frame
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        # Transcribe button
        self.transcribe_btn = ttk.Button(
            button_frame,
            text="Transcribe",
            command=self.transcribe_audio
        )
        self.transcribe_btn.pack(side=tk.LEFT, pady=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = ttk.Label(
            button_frame,
            textvariable=self.status_var,
            foreground=Colors.ACCENT,
            padding=(10, 0)
        )
        self.status_label.pack(side=tk.LEFT, fill='x', expand=True, pady=5)
    
    def transcribe_audio(self):
        """Handle transcription request"""
        try:
            # Get file path from parent
            file_path = self.parent.get_file_path()
            if not file_path:
                self.status_var.set("Please select an audio file first")
                messagebox.showwarning("No File", "Please select an audio file first.")
                return
            
            # Get selected model
            model = self.parent.get_selected_model()
            model_info = f" using model {model}" if model else ""
                
            # Start transcription UI
            self._start_transcription()
            
            # Call STT service with selected model
            response = self.stt_manager.transcribe_audio(file_path, model)
            
            if not response.get('success'):
                raise Exception(response.get('error') or "Transcription failed")
                
            # Update result in parent
            self.parent.set_transcription_result(response['text'])
            
            # Show statistics if available
            stats = []
            if response.get('duration'):
                stats.append(f"Duration: {response['duration']:.1f}s")
            if response.get('word_count'):
                stats.append(f"Words: {response['word_count']}")
            if response.get('model'):
                stats.append(f"Model: {response['model']}")
                
            status = "Transcription complete"
            if stats:
                status += f" ({' | '.join(stats)})"
            self.status_var.set(status)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Transcription Error", str(e))
        finally:
            self._end_transcription()
    
    def _start_transcription(self):
        """Show transcription in progress"""
        self.transcribe_btn.config(state=tk.DISABLED)
        self.transcribe_btn.config(text="Transcribing...")
        self.status_var.set("Transcribing audio...")
        self.update()
        
    def _end_transcription(self):
        """End transcription state"""
        self.transcribe_btn.config(state=tk.NORMAL)
        self.transcribe_btn.config(text="Transcribe") 