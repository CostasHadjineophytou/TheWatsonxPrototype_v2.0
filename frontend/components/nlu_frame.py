import tkinter as tk
from tkinter import ttk, messagebox

class NLUFrame(ttk.Frame):
    """UI frame for NLU analysis"""
    
    def __init__(self, parent, nlu_manager):
        super().__init__(parent)
        self.nlu_manager = nlu_manager
        self._init_ui()

    def _init_ui(self):
        # Input section
        input_frame = ttk.LabelFrame(self, text="Input Text")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.text_input = tk.Text(input_frame, height=5, width=50, wrap=tk.WORD)
        self.text_input.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Analysis options
        options_frame = ttk.LabelFrame(self, text="Analysis Features")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.selected_features = []
        self.checkboxes = {}
        
        features = [
            ("Sentiment", "sentiment"),
            ("Emotion", "emotion"),
            ("Entities", "entities"),
            ("Keywords", "keywords"),
            ("Categories", "categories"),
            ("Concepts", "concepts"),
            ("Relations", "relations"),
            ("Semantic Roles", "semantic_roles")
        ]
        
        for label, feature in features:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                options_frame, 
                text=label,
                variable=var,
                command=lambda f=feature, v=var: self._update_features(f, v)
            )
            cb.pack(anchor=tk.W, padx=5)
            self.checkboxes[feature] = var

        # Control frame
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.analyze_btn = ttk.Button(
            control_frame, 
            text="Analyze Text",
            command=self._analyze_text
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Results section
        results_frame = ttk.LabelFrame(self, text="Analysis Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(
            results_frame, 
            height=10, 
            width=50, 
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def _update_features(self, feature: str, var: tk.BooleanVar):
        if var.get():
            self.selected_features.append(feature)
        else:
            if feature in self.selected_features:
                self.selected_features.remove(feature)

    def _analyze_text(self):
        """Handle analysis request"""
        text = self.text_input.get("1.0", tk.END).strip()
        
        try:
            self._start_analysis()
            result = self.nlu_manager.analyze_text(text, self.selected_features)
            self._format_and_display_results(result)
            
        except Exception as e:
            messagebox.showerror("Analysis Error", str(e))
            
        finally:
            self._end_analysis()

    def _start_analysis(self):
        """Show analysis in progress"""
        self.analyze_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(text="Analyzing...")
        self.progress.start(10)
        
    def _end_analysis(self):
        """End analysis state"""
        self.analyze_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(text="Analyze Text")
        self.progress.stop()

    def _format_and_display_results(self, results: dict):
        """Format results for display"""
        if not results:
            self._show_result("No analysis results available")
            return

        output = []
        
        # Format sentiment
        if 'sentiment' in results:
            sentiment = results['sentiment']
            output.append(f"Sentiment: {sentiment['label']} ({sentiment['score']:.2f})")
            
        # Format emotion
        if 'emotion' in results:
            emotions = results['emotion']
            emotion_text = ", ".join(f"{k}: {v:.2f}" for k, v in emotions.items())
            output.append(f"Emotions:\n{emotion_text}")
            
        # Format entities
        if 'entities' in results:
            entities = results['entities']
            entity_text = "\n• ".join(
                f"{e['text']} ({e['type']}) - {e['confidence']:.2f}"
                for e in entities
            )
            output.append(f"Entities:\n• {entity_text}")
            
        # ... similar formatting for other features

        self._show_result("\n\n".join(output))

    def _show_result(self, text: str):
        """Update results text widget"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", text)
        self.results_text.config(state=tk.DISABLED) 