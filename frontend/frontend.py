import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os

class AIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Islands Watsonx Prototype v2.0")

         # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        # Settings menu so user can edit the API key and location
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="API Key", command=self.edit_api_key)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        # Fetch available datasets
        self.datasets = self.fetch_datasets()

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.prompt_tuning_tab = ttk.Frame(self.notebook)
        self.params_tab = ttk.Frame(self.notebook)
        self.selection_tab = ttk.Frame(self.notebook)
        # Add in all of the tabs from the imports!
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.prompt_tuning_tab, text="Prompt Tuning")
        self.notebook.add(self.params_tab, text="Parameters")
        self.notebook.add(self.selection_tab, text="Selection")

        # Main tab
        self.project_label = tk.Label(self.main_tab, text="Project: Not Selected")
        self.project_label.pack(pady=5)
        self.model_label = tk.Label(self.main_tab, text="Model: Not Selected")
        self.model_label.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()