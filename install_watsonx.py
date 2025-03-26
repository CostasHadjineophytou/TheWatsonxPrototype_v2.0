import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import winreg
import json
from pathlib import Path

def install_requirements(app_path):
    """Install required packages using pip"""
    try:
        # First upgrade pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        except subprocess.CalledProcessError as e:
            messagebox.showwarning("Warning", f"Failed to upgrade pip: {str(e)}\nContinuing with installation...")
        
        # Install base packages
        base_packages = ["setuptools", "wheel"]
        for package in base_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
            except subprocess.CalledProcessError as e:
                messagebox.showwarning("Warning", f"Failed to install {package}: {str(e)}\nContinuing with installation...")
        
        # Install gitpython for repository management
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gitpython"])
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install gitpython: {str(e)}")
            return False
        
        # Install only the necessary packages
        dependencies = [
            # Core IBM packages
            "ibm-watsonx-ai>=1.3.3",
            "ibm-watson>=7.0.0",
            "ibm-cloud-sdk-core>=3.18.0",
            
            # Utility packages
            "requests>=2.31.0",
            "python-dotenv>=1.0.0",
            
            # Audio packages
            "pygame>=2.5.0",
            "pydub>=0.25.1"
        ]
        
        for package in dependencies:
            try:
                print(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except subprocess.CalledProcessError as e:
                error_msg = f"Failed to install {package}: {str(e)}\n"
                error_msg += "This might affect some functionality but installation will continue."
                messagebox.showwarning("Warning", error_msg)
                continue  # Continue with next package even if one fails
            
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to install requirements: {str(e)}")
        return False

def clone_repository():
    """Clone the GitHub repository"""
    try:
        from git import Repo  # Import here after gitpython is installed
        # Get user's documents folder
        documents_path = Path.home() / "Documents"
        app_path = documents_path / "WatsonxPrototype"
        
        if app_path.exists():
            # Repository already exists, pull latest changes
            repo = Repo(app_path)
            origin = repo.remotes.origin
            origin.pull()
        else:
            # Clone new repository
            Repo.clone_from(
                "https://github.com/CostasHadjineophytou/TheWatsonxPrototype_v2.0.git",
                app_path
            )
        return str(app_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clone repository: {str(e)}")
        return None

def create_desktop_shortcut(app_path):
    """Create desktop shortcut for the application"""
    try:
        # Convert app_path to Path if it isn't already
        app_path = Path(app_path).resolve()  # Get absolute path
        desktop_path = Path.home() / "Desktop"
        
        # Verify desktop path exists
        if not desktop_path.exists():
            # Try alternative desktop path
            desktop_path = Path(os.path.expandvars('%USERPROFILE%\\OneDrive\\Desktop'))
            if not desktop_path.exists():
                raise Exception(f"Could not find Desktop directory at {desktop_path}")
        
        shortcut_path = desktop_path / "Watsonx Prototype.lnk"
        
        # Verify app paths exist
        if not app_path.exists():
            raise Exception(f"Application directory not found at {app_path}")
            
        # Get pythonw.exe path (for no-console execution)
        python_exe = Path(sys.executable)
        pythonw_exe = python_exe.parent / "pythonw.exe"
        if not pythonw_exe.exists():
            # Fallback to regular python if pythonw not found
            pythonw_exe = python_exe
            
        icon_path = app_path / "frontend" / "assets" / "images" / "watsonx_icon.ico"
        if not icon_path.exists():
            # If icon doesn't exist, we'll use python's icon instead
            icon_path = pythonw_exe
        
        # Ensure paths are properly formatted for PowerShell
        app_path_str = str(app_path).replace('\\', '\\\\')
        shortcut_path_str = str(shortcut_path).replace('\\', '\\\\')
        pythonw_exe_str = str(pythonw_exe).replace('\\', '\\\\')
        icon_path_str = str(icon_path).replace('\\', '\\\\')
        
        # Create shortcut using PowerShell
        ps_script = f'''
$ErrorActionPreference = "Stop"
try {{
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("{shortcut_path_str}")
    $Shortcut.TargetPath = "{pythonw_exe_str}"
    $Shortcut.Arguments = "-u `"{app_path_str}\\\\main.py`""
    $Shortcut.WorkingDirectory = "{app_path_str}"
    $Shortcut.IconLocation = "{icon_path_str}"
    $Shortcut.Description = "Watsonx Prototype"
    $Shortcut.Save()
}} catch {{
    Write-Error $_.Exception.Message
    exit 1
}}
'''
        
        # Write PowerShell script with UTF-8 encoding
        script_path = Path("create_shortcut.ps1")
        script_path.write_text(ps_script, encoding='utf-8')
        
        # Run PowerShell script with appropriate execution policy
        result = subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)], 
            check=True, 
            capture_output=True,
            text=True
        )
        
        # Clean up
        if script_path.exists():
            script_path.unlink()
            
        # Check if shortcut was created
        if not shortcut_path.exists():
            error_msg = f"Shortcut was not created successfully.\nPowerShell output: {result.stdout}\nError: {result.stderr}"
            raise Exception(error_msg)
            
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create shortcut: {str(e)}")
        return False

def create_env_file(app_path):
    """Create .env file from template"""
    try:
        template_path = app_path / ".env.template"
        env_path = app_path / ".env"
        
        if template_path.exists():
            template_path.rename(env_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create .env file: {str(e)}")
        return False

class InstallerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Watsonx Prototype Installer")
        self.root.geometry("500x400")  # Made window slightly larger
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 400) // 2
        self.root.geometry(f"500x400+{x}+{y}")
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready to install")
        self.detail_var = tk.StringVar(value="")  # For detailed status
        
        # GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Status label
        ttk.Label(self.root, textvariable=self.status_var).pack(pady=20)
        
        # Detailed status label
        ttk.Label(self.root, textvariable=self.detail_var, wraplength=450).pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root, 
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress.pack(pady=20)
        
        # Install button
        self.install_btn = ttk.Button(
            self.root,
            text="Install",
            command=self.install
        )
        self.install_btn.pack(pady=20)
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            self.root,
            text="Cancel",
            command=self.root.quit
        )
        self.cancel_btn.pack(pady=10)
    
    def update_progress(self, value, status, detail=""):
        self.progress_var.set(value)
        self.status_var.set(status)
        self.detail_var.set(detail)
        self.root.update()
    
    def install(self):
        self.install_btn.config(state='disabled')
        
        try:
            # Clone repository first
            self.update_progress(20, "Cloning repository...", "Downloading latest version from GitHub")
            app_path = clone_repository()
            if not app_path:
                self.install_btn.config(state='normal')
                return
            
            # Install requirements
            self.update_progress(40, "Installing requirements...", "This may take a few minutes")
            if not install_requirements(Path(app_path)):
                self.install_btn.config(state='normal')
                return
            
            # Create .env file
            self.update_progress(80, "Creating configuration...", "Setting up environment files")
            if not create_env_file(Path(app_path)):
                self.install_btn.config(state='normal')
                return
            
            # Create desktop shortcut
            self.update_progress(90, "Creating desktop shortcut...", "Making application easily accessible")
            if not create_desktop_shortcut(Path(app_path)):
                self.install_btn.config(state='normal')
                return
            
            # Complete
            self.update_progress(100, "Installation complete!", "You can now run the application from your desktop")
            messagebox.showinfo(
                "Installation Complete",
                "Watsonx Prototype has been installed successfully!\n"
                "You can find it on your desktop."
            )
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"Installation failed: {str(e)}")
            self.install_btn.config(state='normal')
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = InstallerGUI()
    installer.run() 