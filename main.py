import tkinter as tk
from ui.app import CompressionApp

def main():
    root = tk.Tk()
    # Attempt to set taskbar icon/theme
    try: 
        root.iconbitmap("icon.ico")
    except Exception: 
        pass
    
    app = CompressionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()