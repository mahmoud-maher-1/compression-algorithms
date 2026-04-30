import tkinter as tk
from config.logger import logger
from ui.app import CompressionApp

def main():
    logger.info("Application starting...")
    root = tk.Tk()
    app = CompressionApp(root)
    
    logger.info("Entering main loop")
    root.mainloop()
    logger.info("Application shutting down...")

if __name__ == '__main__':
    main()