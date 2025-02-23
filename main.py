import tkinter as tk
from frontend.frontend import AIApp

def start_frontend():
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Start the frontend application
    start_frontend()