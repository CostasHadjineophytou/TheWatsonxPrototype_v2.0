import tkinter as tk
from tkinter import ttk
from frontend.components.nlu_components.feature_selection_frame import FeatureSelectionFrame
from frontend.components.nlu_components.text_input_frame import TextInputFrame
from frontend.components.nlu_components.results_frame import ResultsFrame

class NLUTab(ttk.Frame):
    """Tab for NLU analysis"""
    
    def __init__(self, parent, nlu_manager):
        super().__init__(parent)
        self.nlu_manager = nlu_manager
        self._init_ui()
        self._bind_events()
        
    def _init_ui(self):
        # Left side - Analysis options and controls
        left_frame = ttk.Frame(self)
        left_frame.pack(side='left', fill='y', padx=5, pady=5)

        # Feature selection
        self.feature_frame = FeatureSelectionFrame(left_frame)
        self.feature_frame.pack(fill='x', pady=5)

        # Right side - Text input and results
        right_frame = ttk.Frame(self)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        # Create a vertical paned window to allow resizing
        paned_window = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        paned_window.pack(fill='both', expand=True)

        # Text input with analyze button - smaller portion
        self.text_input_frame = TextInputFrame(paned_window, self.nlu_manager, self.feature_frame)
        
        # Results display - larger portion
        self.results_frame = ResultsFrame(paned_window)
        
        # Add both frames to the paned window with initial positions
        paned_window.add(self.text_input_frame, weight=1)
        paned_window.add(self.results_frame, weight=2)  # Give results frame twice the weight
        
    def _bind_events(self):
        """Bind event handlers"""
        # Bind to the root window since that's where the event is generated
        self.winfo_toplevel().bind("<<NLUAnalysisComplete>>", self._on_analysis_complete)
        
    def _on_analysis_complete(self, event):
        """Handle analysis complete event"""
        # Get the results from the text_input_frame
        results = self.text_input_frame.get_last_results()
        
        if results:
            # Display results
            self.results_frame.display_results(results) 