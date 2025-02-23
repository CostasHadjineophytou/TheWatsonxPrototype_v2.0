import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.app import WatsonApp

if __name__ == "__main__":
    app = WatsonApp()
    app.mainloop()