import tkinter as tk
from tkinter import ttk, messagebox
from frontend.tabs.llm_tab import LLMTab
from frontend.tabs.nlu_tab import NLUTab
from frontend.tabs.tts_tab import TTSTab
from frontend.tabs.stt_tab import STTTab
from logic.manager_factory import ManagerFactory

class WatsonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Watson Services")
        self.geometry("1200x800")
        
        # Centralized manager creation
        self.manager_factory = ManagerFactory()
        self.text_manager = self.manager_factory.create_text_manager()
        self.model_manager = self.manager_factory.create_model_manager()
        self.project_manager = self.manager_factory.create_project_manager()
        self.nlu_manager = self.manager_factory.create_nlu_manager()
        self.tts_manager = self.manager_factory.create_tts_manager()
        self.stt_manager = self.manager_factory.create_stt_manager()
        self.audio_manager = self.manager_factory.create_audio_manager()
        
        # Create menu bar
        self._create_menu_bar()
        
        # Initialize UI
        self._init_ui()
        
    def _create_menu_bar(self):
        """Create the application menu bar"""
        self.menu_bar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Account menu
        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="Projects", command=self._show_projects_popup)
        account_menu.add_command(label="Services", command=self._show_services_popup)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)
        
        # Settings menu (empty for now)
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu (empty for now)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        # Set the menu bar
        self.config(menu=self.menu_bar)
        
    def _show_projects_popup(self):
        """Show the projects popup window"""
        try:
            # Import here to avoid circular imports
            from frontend.pop_ups.projects_popup import ProjectsPopup
            ProjectsPopup(self, self.project_manager)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Projects window: {str(e)}")
            
    def _show_services_popup(self):
        """Show the services popup window"""
        try:
            # Import here to avoid circular imports
            from frontend.pop_ups.services_popup import ServicesPopup
            ServicesPopup(self, self.manager_factory.create_service_checker())
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Services window: {str(e)}")

    def _init_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            self, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create tabs
        self.llm_tab = LLMTab(
            self.notebook, 
            text_manager=self.text_manager,
            model_manager=self.model_manager,
            project_manager=self.project_manager,
            status_var=self.status_var
        )
        self.nlu_tab = NLUTab(
            self.notebook,
            nlu_manager=self.nlu_manager,
            status_var=self.status_var
        )
        self.tts_tab = TTSTab(
            self.notebook,
            tts_manager=self.tts_manager,
            audio_manager=self.audio_manager,
            status_var=self.status_var
        )
        self.stt_tab = STTTab(
            self.notebook,
            stt_manager=self.stt_manager,
            status_var=self.status_var
        )
        
        # Add tabs to notebook
        self.notebook.add(self.llm_tab, text="Text Generation")
        self.notebook.add(self.nlu_tab, text="Natural Language Understanding")
        self.notebook.add(self.tts_tab, text="Text to Speech")
        self.notebook.add(self.stt_tab, text="Speech to Text")
        
    def run(self):
        """Start the application"""
        self.mainloop() 