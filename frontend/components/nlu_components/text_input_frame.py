import tkinter as tk
from tkinter import ttk, messagebox
from frontend.styles.colors import Colors

class TextInputFrame(ttk.LabelFrame):
    """Frame for entering text to analyze"""
    
    def __init__(self, parent, nlu_manager, feature_frame):
        super().__init__(parent, text="Input Text")
        self.nlu_manager = nlu_manager
        self.feature_frame = feature_frame
        self.last_results = None
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Text input area
        self.text_input = tk.Text(
            self, 
            height=6,
            width=50, 
            wrap=tk.WORD
        )
        self.text_input.pack(padx=5, pady=5, fill='both', expand=True)
        
        # Control frame for button and status
        control_frame = ttk.Frame(self)
        control_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        # Analyze button
        self.analyze_btn = ttk.Button(
            control_frame, 
            text="Analyze Text",
            command=self._analyze_text
        )
        self.analyze_btn.pack(side=tk.LEFT)
        
        # Status label
        self.status_label = ttk.Label(
            control_frame,
            text="Ready",
            foreground=Colors.ACCENT
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
    def _analyze_text(self):
        """Handle analysis request"""
        text = self.text_input.get("1.0", tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to analyze.")
            return
            
        selected_features = self.feature_frame.get_selected_features()
        if not selected_features:
            messagebox.showwarning("Warning", "Please select at least one feature to analyze.")
            return
        
        try:
            self._start_analysis()
            
            # Perform the actual analysis
            result = self.nlu_manager.analyze_text(text, selected_features)
            
            if isinstance(result, dict) and "error" in result:
                raise Exception(result["error"])
                
            # Store the results for the parent to access
            self.last_results = result
            
            # Generate a virtual event to notify the parent
            # We need to use winfo_toplevel() to get the root window
            # and then generate the event on the tab
            self.winfo_toplevel().event_generate("<<NLUAnalysisComplete>>")
            
            self._end_analysis(success=True)
            
            # Return the results to the parent tab
            return result
            
        except Exception as e:
            self._end_analysis(success=False)
            messagebox.showerror("Analysis Error", str(e))
            return None
            
    def _start_analysis(self):
        """Show analysis in progress"""
        self.analyze_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(text="Analyzing...")
        self.status_label.config(text="Analyzing text...", foreground="blue")
        self.update()
        
    def _end_analysis(self, success=True):
        """End analysis state"""
        self.analyze_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(text="Analyze Text")
        
        status_text = "Analysis complete" if success else "Analysis failed"
        status_color = Colors.SUCCESS if success else Colors.ERROR
        
        self.status_label.config(text=status_text, foreground=status_color)
        
    def get_text(self):
        """Get the current text input"""
        return self.text_input.get("1.0", tk.END).strip()
        
    def get_last_results(self):
        """Get the results of the last analysis"""
        return self.last_results 