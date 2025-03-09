import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

class ServicesPopup(tk.Toplevel):
    """Popup window for displaying IBM Cloud services"""
    
    def __init__(self, parent, service_checker):
        super().__init__(parent)
        self.service_checker = service_checker
        
        # Configure window
        self.title("IBM Cloud Services")
        self.geometry("900x600")
        self.minsize(700, 500)
        
        # Make window modal
        self.transient(parent)
        self.grab_set()
        
        # Initialize UI
        self._init_ui()
        
        # Load services
        self._load_services()
        
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
            text="Your IBM Cloud Services", 
            font=("Segoe UI", 14, "bold")
        ).pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            header_frame,
            text="Refresh",
            command=self._load_services
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
            columns=("name", "type", "region", "status", "created"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        # Configure scrollbars
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("name", text="Service Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("region", text="Region")
        self.tree.heading("status", text="Status")
        self.tree.heading("created", text="Created")
        
        self.tree.column("name", width=200, minwidth=150)
        self.tree.column("type", width=150, minwidth=100)
        self.tree.column("region", width=100, minwidth=80)
        self.tree.column("status", width=100, minwidth=80)
        self.tree.column("created", width=150, minwidth=100)
        
        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self._on_service_double_click)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # View details button
        view_btn = ttk.Button(
            button_frame,
            text="View Details",
            command=self._view_selected_service
        )
        view_btn.pack(side=tk.LEFT)
        
        # View credentials button
        creds_btn = ttk.Button(
            button_frame,
            text="View Credentials",
            command=self._view_credentials
        )
        creds_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Open dashboard button
        dashboard_btn = ttk.Button(
            button_frame,
            text="Open Dashboard",
            command=self._open_dashboard
        )
        dashboard_btn.pack(side=tk.LEFT, padx=(10, 0))
        
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
            button_frame,
            text="Close",
            command=self.destroy
        )
        close_btn.pack(side=tk.RIGHT)
        
    def _load_services(self):
        """Load services from the service checker"""
        try:
            self.status_var.set("Loading services...")
            self.update_idletasks()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get services
            services = self.service_checker.get_services()
            
            if not services:
                self.status_var.set("No services found")
                return
            
            # Add services to treeview
            for service in services:
                self.tree.insert(
                    "",
                    tk.END,
                    iid=service['id'],  # Use service ID as item ID
                    values=(
                        service['name'],
                        service['type'],
                        service['region'],
                        service['status'],
                        service['created_at']
                    )
                )
            
            self.status_var.set(f"Loaded {len(services)} services")
            
        except Exception as e:
            self.status_var.set("Error loading services")
            messagebox.showerror("Error", f"Failed to load services: {str(e)}")
            
    def _on_service_double_click(self, event):
        """Handle double-click on a service"""
        self._view_selected_service()
            
    def _view_selected_service(self):
        """View details of the selected service"""
        selected_id = self.tree.focus()
        if not selected_id:
            messagebox.showinfo("Info", "Please select a service first")
            return
            
        try:
            # Get service details
            service = self.service_checker.get_service_details(selected_id)
            
            # Create details window
            self._show_service_details(service)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get service details: {str(e)}")
            
    def _show_service_details(self, service):
        """Show service details in a new window"""
        details_window = tk.Toplevel(self)
        details_window.title(f"Service Details: {service['name']}")
        details_window.geometry("600x400")
        details_window.minsize(500, 300)
        
        # Make window modal
        details_window.transient(self)
        details_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(details_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            main_frame, 
            text=f"Service: {service['name']}", 
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create scrollable text widget
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(text_frame, orient="vertical")
        text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=vsb.set,
            height=20,
            width=70
        )
        
        vsb.config(command=text.yview)
        
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert service details
        text.insert(tk.END, f"ID: {service['id']}\n")
        text.insert(tk.END, f"Name: {service['name']}\n")
        text.insert(tk.END, f"Type: {service['type']}\n")
        text.insert(tk.END, f"Region: {service['region']}\n")
        text.insert(tk.END, f"Status: {service['status']}\n")
        text.insert(tk.END, f"Created: {service['created_at']}\n")
        text.insert(tk.END, f"Resource Group: {service['resource_group']}\n")
        
        if service.get('dashboard_url'):
            text.insert(tk.END, f"Dashboard URL: {service['dashboard_url']}\n")
            
        # Add credentials section if available
        if service.get('credentials'):
            text.insert(tk.END, "\nCredentials:\n")
            for cred in service['credentials']:
                text.insert(tk.END, f"  - {cred['name']} (Created: {cred['created_at']})\n")
                
        # Make text read-only
        text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=details_window.destroy
        ).pack(side=tk.RIGHT, pady=(10, 0))
            
    def _view_credentials(self):
        """View credentials for the selected service"""
        selected_id = self.tree.focus()
        if not selected_id:
            messagebox.showinfo("Info", "Please select a service first")
            return
            
        try:
            # Get credentials
            credentials = self.service_checker.get_service_credentials(selected_id)
            
            if not credentials:
                messagebox.showinfo("Info", "No credentials found for this service")
                return
                
            # Show credentials window
            self._show_credentials_window(credentials)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get credentials: {str(e)}")
            
    def _show_credentials_window(self, credentials):
        """Show credentials in a new window"""
        creds_window = tk.Toplevel(self)
        creds_window.title("Service Credentials")
        creds_window.geometry("700x500")
        creds_window.minsize(600, 400)
        
        # Make window modal
        creds_window.transient(self)
        creds_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(creds_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            main_frame, 
            text="Service Credentials", 
            font=("Segoe UI", 12, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Create notebook for multiple credentials
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add a tab for each credential
        for cred in credentials:
            cred_frame = ttk.Frame(notebook, padding="10")
            notebook.add(cred_frame, text=cred['name'])
            
            # Create scrollable text widget
            text_frame = ttk.Frame(cred_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            vsb = ttk.Scrollbar(text_frame, orient="vertical")
            text = tk.Text(
                text_frame,
                wrap=tk.WORD,
                yscrollcommand=vsb.set,
                height=20,
                width=70
            )
            
            vsb.config(command=text.yview)
            
            text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Insert credential details
            text.insert(tk.END, f"Name: {cred['name']}\n")
            text.insert(tk.END, f"Created: {cred['created_at']}\n")
            text.insert(tk.END, f"Status: {cred['status']}\n\n")
            
            # Insert credential values
            text.insert(tk.END, "Credential Values:\n\n")
            
            if cred.get('credentials'):
                for key, value in cred['credentials'].items():
                    text.insert(tk.END, f"{key}: {value}\n")
            else:
                text.insert(tk.END, "No credential values available")
                
            # Make text read-only
            text.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=creds_window.destroy
        ).pack(side=tk.RIGHT, pady=(10, 0))
            
    def _open_dashboard(self):
        """Open the service dashboard in a web browser"""
        selected_id = self.tree.focus()
        if not selected_id:
            messagebox.showinfo("Info", "Please select a service first")
            return
            
        try:
            # Get service details
            service = self.service_checker.get_service_details(selected_id)
            
            if not service.get('dashboard_url'):
                messagebox.showinfo("Info", "No dashboard URL available for this service")
                return
                
            # Open URL in browser
            webbrowser.open(service['dashboard_url'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}") 