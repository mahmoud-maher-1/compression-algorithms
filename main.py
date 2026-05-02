import tkinter as tk
import sv_ttk
from config.logger import logger
from ui.app import CompressionApp

def main():
    logger.info("Application starting...")
    root = tk.Tk()
    
    # Apply modern dark theme
    sv_ttk.set_theme("dark")
    
    app = CompressionApp(root)
    
    logger.info("Entering main loop")
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    root.mainloop()
    logger.info("Application shutting down...")

if __name__ == '__main__':
    main()