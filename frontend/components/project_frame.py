import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic.managers.project_manager import ProjectManager

class ProjectFrame(ttk.LabelFrame):
    def __init__(self, parent, project_manager):
        super().__init__(parent, text="Project Selection")
        self.project_manager = project_manager
        self.setup_ui()
        
    def setup_ui(self):
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
            names = [p.get('name', 'Unnamed') for p in projects]
            self.projects_combo['values'] = names
            if names:
                self.projects_combo.set(names[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")
            
    def get_selected_project(self):
        """Get the ID of the selected project"""
        selected = self.project_var.get()
        for project in self.project_list:
            if project.get('name') == selected:
                return project.get('id')
        return None 