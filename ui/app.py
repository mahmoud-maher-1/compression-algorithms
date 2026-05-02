import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config.logger import logger
from algorithms import rle_compress, huffman_compress, lzw_compress

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multimedia Compression Lab")
        self.root.geometry("1000x750")
        
        # Make the main window resizable
        self.root.rowconfigure(3, weight=1) # Allow the chart frame to expand
        self.root.columnconfigure(0, weight=1)

        self.file_path = ""
        self.results = []
        
        # State variables for background thread communication
        self.status_var = tk.StringVar(value="Ready")

        logger.info("Initializing UI Components")
        self.setup_ui()

    def setup_ui(self):
        # Header (Row 0)
        header = ttk.Label(self.root, text="Multimedia File Compression System", font=("Segoe UI", 20, "bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        # --- Controls Area ---
        controls_container = ttk.Frame(self.root)
        controls_container.grid(row=1, column=0, sticky="ew", padx=30, pady=10)
        controls_container.columnconfigure(1, weight=1)

        # File Selection Frame
        file_frame = ttk.LabelFrame(controls_container, text=" 1. Select Multimedia File ")
        file_frame.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)
        
        self.btn_browse = ttk.Button(file_frame, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(side="left", padx=15, pady=15)

        self.lbl_file_details = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.lbl_file_details.pack(side="left", padx=10)

        # Benchmark Action Frame
        action_frame = ttk.Frame(controls_container)
        action_frame.grid(row=0, column=1, sticky="e", pady=10)

        self.btn_run = ttk.Button(action_frame, text="Run Compression Benchmark", state="disabled",
                                  command=self.start_benchmark_thread, style="Accent.TButton")
        self.btn_run.pack(pady=(15, 0))

        # --- Progress and Status ---
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)

        self.lbl_status = ttk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 10, "italic"))
        self.lbl_status.grid(row=0, column=0, sticky="w")

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=0, column=1, sticky="ew", padx=(20, 0))

        # --- Main Content Area ---
        content_container = ttk.Frame(self.root)
        content_container.grid(row=3, column=0, sticky="nsew", padx=30, pady=(10, 20))
        content_container.rowconfigure(1, weight=1)
        content_container.columnconfigure(0, weight=1)

        # Comparison Table (Row 0)
        table_frame = ttk.LabelFrame(content_container, text=" 2. Performance Comparison ")
        table_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        cols = ("Algorithm", "Original (B)", "Compressed (B)", "Ratio", "Time (ms)")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=4)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="x", padx=15, pady=15)

        # Chart Frame (Row 1)
        self.chart_frame = ttk.Frame(content_container)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")
        
        # Apply modern style accent to primary button if supported
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Multimedia Files", "*.txt *.pdf *.png *.jpg"), ("All Files", "*.*")])
        if self.file_path:
            f_name = os.path.basename(self.file_path)
            f_size = os.path.getsize(self.file_path)
            self.lbl_file_details.config(text=f"{f_name}  |  {f_size:,} Bytes")
            self.btn_run.config(state="normal")
            self.status_var.set("Ready to compress.")
            logger.info(f"File selected: {self.file_path} (Size: {f_size} bytes)")

    def start_benchmark_thread(self):
        """Disables UI elements and spawns a background thread to prevent UI freezing."""
        # Update UI state
        self.btn_run.config(state="disabled")
        self.btn_browse.config(state="disabled")
        self.progress.start(10) # Start indeterminate progress spinner
        
        # Clear previous results
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Start background thread
        thread = threading.Thread(target=self.run_benchmark_worker, daemon=True)
        thread.start()

    def run_benchmark_worker(self):
        """Executes the compression algorithms. Runs entirely in a background thread."""
        logger.info(f"Running benchmark on {self.file_path}")
        self._update_status_threadsafe("Reading file...")

        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            self.root.after(0, lambda err=e: messagebox.showerror("Error", f"Could not read file: {err}"))
            self._reset_ui_threadsafe()
            return

        original_size = len(data)
        if original_size == 0:
            logger.warning("Selected file is empty")
            self.root.after(0, lambda: messagebox.showwarning("Warning", "File is empty!"))
            self._reset_ui_threadsafe()
            return

        has_non_ascii = any(ord(c) >= 256 for c in data)
        if has_non_ascii:
            logger.warning("File contains non-ASCII characters. These will be ignored by LZW.")
            self.root.after(0, lambda: messagebox.showwarning("Warning", "The file contains non-ASCII characters.\nThese will be ignored by the LZW compression algorithm."))

        algos = [
            ("RLE", rle_compress),
            ("Huffman", huffman_compress),
            ("LZW", lzw_compress)
        ]

        self.results = []

        for name, func in algos:
            self._update_status_threadsafe(f"Processing {name} Compression...")
            logger.info(f"Executing {name} algorithm")
            
            start_t = time.perf_counter()
            compressed_data = func(data)
            end_t = time.perf_counter()

            if name == "Huffman":
                comp_size = len(compressed_data) // 8  # Bits to Bytes
            else:
                comp_size = len(str(compressed_data))

            ratio = original_size / comp_size if comp_size > 0 else 0
            exec_time = (end_t - start_t) * 1000  # ms

            # Pass the result back to the main thread to update the table
            result_data = (name, original_size, comp_size, ratio, exec_time)
            self.results.append((name, ratio))
            self.root.after(0, self._insert_tree_item, result_data)

            logger.info(f"{name} completed: Ratio={ratio:.2f}x, Time={exec_time:.3f}ms")
            
            # Small artificial sleep just to make the progress bar and status transitions visible
            # since small text files compress almost instantly.
            time.sleep(0.3)

        # Final UI updates
        self._update_status_threadsafe("Generating Performance Chart...")
        self.root.after(0, self.update_chart)
        self._reset_ui_threadsafe()

    def _insert_tree_item(self, data):
        """Thread-safe method to insert a row into the treeview."""
        name, original, comp, ratio, exec_time = data
        self.tree.insert("", "end", values=(name, f"{original:,}", f"{comp:,}", f"{ratio:.2f}x", f"{exec_time:.3f}"))

    def _update_status_threadsafe(self, msg):
        """Thread-safe method to update status label."""
        self.root.after(0, lambda: self.status_var.set(msg))

    def _reset_ui_threadsafe(self):
        """Thread-safe method to restore UI controls after benchmark is done."""
        def reset():
            self.progress.stop()
            self.btn_run.config(state="normal")
            self.btn_browse.config(state="normal")
            self.status_var.set("Benchmark Complete.")
        self.root.after(0, reset)

    def update_chart(self):
        logger.debug("Updating performance chart")

        names = [r[0] for r in self.results]
        ratios = [r[1] for r in self.results]

        # Use a modern styling for the plot to match the dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Transparent background for the plot area
        fig.patch.set_facecolor('#1c1c1c') 
        ax.set_facecolor('#1c1c1c')
        
        # Plot with modern colors
        bars = ax.bar(names, ratios, color=['#0078D7', '#881798', '#10893E'], width=0.6)
        
        ax.axhline(1, color='#ff5555', linewidth=1.5, linestyle='--')  # 1x line
        ax.set_ylabel('Compression Ratio (Higher is Better)', color='#dddddd')
        ax.set_title('Efficiency Benchmark', color='white', pad=15)

        # Remove borders
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        ax.tick_params(colors='#dddddd')

        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, f'{yval:.2f}x', 
                    ha='center', va='bottom', color='white', fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
