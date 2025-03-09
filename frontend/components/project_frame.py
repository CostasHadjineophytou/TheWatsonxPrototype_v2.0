import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProjectFrame(ttk.LabelFrame):
    def __init__(self, parent, project_manager):
        super().__init__(parent, text="Project Selection")
        self.project_manager = project_manager  # Injected from app.py
        self._init_ui()
        
    def _init_ui(self):
        self.project_var = tk.StringVar()
        self.projects_combo = ttk.Combobox(
            self, 
            textvariable=self.project_var,
            state="readonly"
        )
        self.projects_combo.pack(fill='x', padx=5, pady=5)
        self.load_projects()
        
    def load_projects(self):
        try:
            projects = self.project_manager.get_projects()
            self.project_list = projects
            names = [self.project_manager.format_project_display(p) for p in projects]
            self.projects_combo['values'] = names
            if names:
                self.projects_combo.set(names[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")
            
    def get_selected_project(self):
        """Get the ID of the selected project"""
        selected = self.project_var.get()
        project = self.project_manager.get_project_by_name(selected)
        # Let project_manager handle the data structure
        return project.id if project else None 