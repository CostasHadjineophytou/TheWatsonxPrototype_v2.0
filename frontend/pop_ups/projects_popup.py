import tkinter as tk
from tkinter import ttk, messagebox

class ProjectsPopup(tk.Toplevel):
    """Popup window for displaying user projects"""
    
    def __init__(self, parent, project_manager):
        super().__init__(parent)
        self.project_manager = project_manager
        
        # Configure window
        self.title("IBM Cloud Projects")
        self.geometry("800x500")
        self.minsize(600, 400)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Initialize UI
        self._init_ui()
        
        # Load projects
        self._load_projects()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame, 
            text="Your IBM Cloud Projects", 
            font=("Segoe UI", 14, "bold")
        ).pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            header_frame,
            text="Refresh",
            command=self._load_projects
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "description", "created"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configure scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("name", text="Project Name")
        self.tree.heading("description", text="Description")
        self.tree.heading("created", text="Created")
        
        self.tree.column("name", width=200, minwidth=150)
        self.tree.column("description", width=400, minwidth=200)
        self.tree.column("created", width=150, minwidth=100)
        
        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Close button
        close_btn = ttk.Button(
            main_frame,
            text="Close",
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT, pady=(10, 0))
        
    def _load_projects(self):
        """Load projects from the project manager"""
        try:
            self.status_var.set("Loading projects...")
            self.update_idletasks()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get projects
            projects = self.project_manager.get_projects()
            
            if not projects:
                self.status_var.set("No projects found")
                return
            
            # Add projects to treeview
            for project in projects:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        project.name,
                        project.description or "No description",
                        project.created_at or "Unknown"
                    )
                )
            
            self.status_var.set(f"Loaded {len(projects)} projects")
            
        except Exception as e:
            self.status_var.set("Error loading projects")
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}") 