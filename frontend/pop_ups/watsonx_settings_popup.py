import tkinter as tk
from tkinter import ttk, messagebox
from backend.utils.env_manager import EnvManager
from backend.config.config import Config

class WatsonxSettingsPopup(tk.Toplevel):
    """Popup window for Watsonx settings"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Watsonx Settings")
        self.geometry("500x150")
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Initialize environment manager
        self.env_manager = EnvManager()
        
        # Create UI
        self._create_ui()
        
        # Center the window
        self._center_window()
        
    def _create_ui(self):
        """Create the UI elements"""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # API Key section
        ttk.Label(main_frame, text="IBM Cloud API Key:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.api_key_var = tk.StringVar(value=self.env_manager.get_current_api_key() or "")
        api_key_entry = ttk.Entry(main_frame, textvariable=self.api_key_var, width=60)
        api_key_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Region section
        ttk.Label(main_frame, text="Region:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.region_var = tk.StringVar(value=self.env_manager.get_current_region() or "eu-gb")
        region_combo = ttk.Combobox(main_frame, textvariable=self.region_var, width=20, state="readonly")
        region_combo['values'] = ('eu-gb', 'eu-de', 'jp-tok', 'us-south')
        region_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self._save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
    def _center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
    def _save_settings(self):
        """Save the settings to the .env file"""
        try:
            # Update API key
            new_api_key = self.api_key_var.get().strip()
            if not new_api_key:
                messagebox.showerror("Error", "API key cannot be empty")
                return
            self.env_manager.update_api_key(new_api_key)
            
            # Update region
            new_region = self.region_var.get()
            self.env_manager.update_region(new_region)
            
            # Reload environment variables
            self.env_manager.reload_env()
            
            # Update Config class
            Config.reload()
            
            messagebox.showinfo("Success", "Settings saved successfully. Please restart the application for changes to take effect.")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
