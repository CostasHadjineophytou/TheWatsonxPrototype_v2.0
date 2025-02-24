import tkinter as tk

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self._show)
        self.widget.bind("<Leave>", self._hide)

    def _show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        # Create top level window
        self.tooltip = tk.Toplevel(self.widget)
        # Remove window decorations
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip, 
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0", 
            relief=tk.SOLID,
            borderwidth=1,
            padx=5,
            pady=2
        )
        label.pack()

    def _hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None 