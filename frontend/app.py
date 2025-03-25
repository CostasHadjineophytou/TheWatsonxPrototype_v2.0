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
        
        # Set initial window size to full screen
        self.state('zoomed')
        
        # Track full screen state
        self.is_fullscreen = True
        
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
        
        # Settings menu
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        settings_menu.add_command(label="watsonx", command=self._show_watsonx_settings_popup)
        self.menu_bar.add_cascade(label="Settings", menu=settings_menu)
        
        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Toggle Full Screen", command=self._toggle_fullscreen)
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about_popup)
        help_menu.add_command(label="Help", command=self._show_help_popup)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        # Set the menu bar
        self.config(menu=self.menu_bar)
        
    def _toggle_fullscreen(self):
        """Toggle between full screen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.state('zoomed')
        else:
            self.state('normal')
            self.geometry("1000x600")
        
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
    
    def _show_watsonx_settings_popup(self):
        """Show the settings popup window"""
        try:
            from frontend.pop_ups.watsonx_settings_popup import WatsonxSettingsPopup
            WatsonxSettingsPopup(self)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Settings window: {str(e)}")
    
    def _show_about_popup(self):
        """Show the about popup window"""
        try:
            from frontend.pop_ups.about_popup import AboutPopup
            AboutPopup(self)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open About window: {str(e)}")
    
    def _show_help_popup(self):
        """Show the help popup window"""
        try:
            from frontend.pop_ups.help_popup import HelpPopup
            HelpPopup(self)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open Help window: {str(e)}")

    def _init_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.llm_tab = LLMTab(
            self.notebook, 
            text_manager=self.text_manager,
            model_manager=self.model_manager,
            project_manager=self.project_manager,
            
        )
        self.nlu_tab = NLUTab(
            self.notebook,
            nlu_manager=self.nlu_manager,
            
        )
        self.tts_tab = TTSTab(
            self.notebook,
            tts_manager=self.tts_manager,
            audio_manager=self.audio_manager,
            
        )
        self.stt_tab = STTTab(
            self.notebook,
            stt_manager=self.stt_manager,
            
        )
        
        # Add tabs to notebook
        self.notebook.add(self.llm_tab, text="Text Generation")
        self.notebook.add(self.nlu_tab, text="Natural Language Understanding")
        self.notebook.add(self.tts_tab, text="Text to Speech")
        self.notebook.add(self.stt_tab, text="Speech to Text")
        
    def run(self):
        """Start the application"""
        self.mainloop() 