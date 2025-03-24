import sys
import os
#import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.app import WatsonApp
from backend.utils.file_manager import FileManager

# Set up logging at the beginning
#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    # Ensure required directories exist
    FileManager.ensure_directories()
    
    # Start application
    app = WatsonApp()
    app.mainloop()