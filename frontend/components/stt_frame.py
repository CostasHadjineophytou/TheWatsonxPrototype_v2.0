import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..styles.colors import Colors

class STTFrame(ttk.Frame):
    """UI frame for Speech-to-Text"""
    
    def __init__(self, parent, stt_manager):
        super().__init__(parent)
        self.stt_manager = stt_manager
        self._init_ui()
        
    def _init_ui(self):
        # File selection
        file_frame = ttk.Frame(self)
        file_frame.pack(fill='x', padx=10, pady=10)
        
        file_label = ttk.Label(file_frame, text="Audio file:")
        file_label.pack(side=tk.LEFT, padx=(0,5))
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(
            file_frame, 
            textvariable=self.file_path_var,
            width=50
        )
        self.file_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=5)
        
        browse_btn = ttk.Button(
            file_frame,
            text="Browse",
            command=self._browse_file
        )
        browse_btn.pack(side=tk.LEFT, padx=(5,0))
        
        # Transcribe button
        self.transcribe_btn = ttk.Button(
            self,
            text="Transcribe",
            command=self._transcribe_audio
        )
        self.transcribe_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(pady=5)
        
        # Results area
        result_frame = ttk.LabelFrame(self, text="Transcription")
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.result_text = tk.Text(
            result_frame,
            wrap=tk.WORD,
            height=10,
            state=tk.DISABLED
        )
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            anchor=tk.W,
            padding=(5, 2)
        )
        status_bar.pack(fill='x', side=tk.BOTTOM)
        
    def _browse_file(self):
        """Open file dialog to select audio file"""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.flac *.ogg *.m4a *.wma"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def _transcribe_audio(self):
        """Handle transcription request"""
        file_path = self.file_path_var.get()
        if not file_path:
            messagebox.showwarning("No File", "Please select an audio file first.")
            return
            
        try:
            self._start_transcription()
            
            response = self.stt_manager.transcribe_audio(file_path)
            
            if not response.get('success'):
                raise Exception(response.get('error') or "Transcription failed")
                
            # Display result
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, response['text'])
            self.result_text.config(state=tk.DISABLED)
            
            # Show statistics if available
            stats = []
            if response.get('duration'):
                stats.append(f"Duration: {response['duration']:.1f}s")
            if response.get('word_count'):
                stats.append(f"Words: {response['word_count']}")
                
            status = "Transcription complete"
            if stats:
                status += f" ({' | '.join(stats)})"
            self.status_var.set(status)
            
        except Exception as e:
            messagebox.showerror("Transcription Error", str(e))
            self.status_var.set("Transcription failed")
        finally:
            self._end_transcription()

    def _start_transcription(self):
        """Show transcription in progress"""
        self.transcribe_btn.config(state=tk.DISABLED)
        self.transcribe_btn.config(text="Transcribing...")
        self.progress.start(10)
        self.status_var.set("Transcribing audio...")
        self.update()
        
    def _end_transcription(self):
        """End transcription state"""
        self.transcribe_btn.config(state=tk.NORMAL)
        self.transcribe_btn.config(text="Transcribe")
        self.progress.stop() 