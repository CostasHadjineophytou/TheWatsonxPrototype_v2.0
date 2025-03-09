import tkinter as tk
from tkinter import ttk
from backend.config.nlu_config import NLUConfig
from ..tooltip import ToolTip

class FeatureSelectionFrame(ttk.LabelFrame):
    """Frame for selecting NLU analysis features"""
    
    def __init__(self, parent):
        super().__init__(parent, text="Analysis Features")
        self.selected_features = []
        self.checkboxes = {}
        self._init_ui()
        
    def _init_ui(self):
        """Initialize UI components"""
        # Button frame for Select All and Clear All
        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=5, pady=(5, 0))
        
        # Select All button
        select_all_btn = ttk.Button(
            button_frame,
            text="Select All",
            command=self._select_all,
            width=10
        )
        select_all_btn.pack(side='left', padx=(0, 5))
        
        # Clear All button
        clear_all_btn = ttk.Button(
            button_frame,
            text="Clear All",
            command=self._clear_all,
            width=10
        )
        clear_all_btn.pack(side='left')
        
        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=5, pady=5)
        
        # Features checkboxes
        features_frame = ttk.Frame(self)
        features_frame.pack(fill='both', expand=True, padx=5, pady=0)
        
        # Get features from config
        for display_name, feature_id in NLUConfig.get_ui_features():
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                features_frame, 
                text=display_name,
                variable=var,
                command=lambda f=feature_id, v=var: self._update_features(f, v)
            )
            # Add tooltip with description
            tooltip = NLUConfig.get_feature_description(feature_id)
            ToolTip(cb, tooltip)
            
            cb.pack(anchor=tk.W, padx=5, pady=2)
            self.checkboxes[feature_id] = var
            
    def _update_features(self, feature: str, var: tk.BooleanVar):
        """Update selected features when checkbox state changes"""
        if var.get():
            self.selected_features.append(feature)
        else:
            if feature in self.selected_features:
                self.selected_features.remove(feature)
                
    def _select_all(self):
        """Select all features"""
        for feature_id, var in self.checkboxes.items():
            var.set(True)
            if feature_id not in self.selected_features:
                self.selected_features.append(feature_id)
                
    def _clear_all(self):
        """Clear all feature selections"""
        for var in self.checkboxes.values():
            var.set(False)
        self.selected_features.clear()
                
    def get_selected_features(self):
        """Get list of selected feature IDs"""
        return self.selected_features 