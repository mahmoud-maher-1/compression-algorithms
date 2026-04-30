import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config.logger import logger
from algorithms import rle_compress, huffman_compress, lzw_compress

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multimedia Compression Lab")
        self.root.geometry("1000x750")
        self.file_path = ""
        self.results = []

        logger.info("Initializing UI Components")
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="Multimedia File Compression System", font=("Arial", 18, "bold"))
        header.pack(pady=15)

        # File Selection Frame
        file_frame = tk.LabelFrame(self.root, text=" 1. Select Multimedia File ")
        file_frame.pack(fill="x", padx=20, pady=10)

        self.btn_browse = ttk.Button(file_frame, text="Browse File", command=self.browse_file)
        self.btn_browse.pack(side="left", padx=10, pady=10)

        self.lbl_file_details = tk.Label(file_frame, text="No file selected", fg="gray")
        self.lbl_file_details.pack(side="left", padx=10)

        # Control Frame
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(pady=10)

        self.btn_run = ttk.Button(ctrl_frame, text="Run Compression Benchmark", state="disabled",
                                  command=self.run_benchmark)
        self.btn_run.pack()

        # Comparison Table
        table_frame = tk.LabelFrame(self.root, text=" 2. Performance Comparison ")
        table_frame.pack(fill="x", padx=20, pady=10)

        cols = ("Algorithm", "Original (B)", "Compressed (B)", "Ratio", "Time (ms)")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="x", padx=10, pady=10)

        # Chart Frame
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Multimedia Files", "*.txt *.pdf *.png *.jpg"), ("All Files", "*.*")])
        if self.file_path:
            f_name = os.path.basename(self.file_path)
            f_size = os.path.getsize(self.file_path)
            self.lbl_file_details.config(text=f"File: {f_name} | Size: {f_size} Bytes", fg="black")
            self.btn_run.config(state="normal")
            logger.info(f"File selected: {self.file_path} (Size: {f_size} bytes)")

    def run_benchmark(self):
        logger.info(f"Running benchmark on {self.file_path}")
        # Read file as text for demonstration (simulating character streams [cite: 40, 56])
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            messagebox.showerror("Error", f"Could not read file: {e}")
            return

        original_size = len(data)
        if original_size == 0:
            logger.warning("Selected file is empty")
            messagebox.showwarning("Warning", "File is empty!")
            return

        # Check for non-ASCII characters to warn the user about LZW behavior
        has_non_ascii = any(ord(c) >= 256 for c in data)
        if has_non_ascii:
            logger.warning("File contains non-ASCII characters. These will be ignored by LZW.")
            messagebox.showwarning("Warning", "The file contains non-ASCII characters.\nThese will be ignored by the LZW compression algorithm.")

        # Algorithm list
        algos = [
            ("RLE", rle_compress),
            ("Huffman", huffman_compress),
            ("LZW", lzw_compress)
        ]

        self.results = []
        for i in self.tree.get_children(): self.tree.delete(i)

        for name, func in algos:
            logger.info(f"Executing {name} algorithm")
            start_t = time.perf_counter()
            compressed_data = func(data)
            end_t = time.perf_counter()

            # Measure size of output (treating Huffman as bit-length/8)
            if name == "Huffman":
                comp_size = len(compressed_data) // 8  # Bits to Bytes
            else:
                comp_size = len(str(compressed_data))

            # Calculate Compression Ratio
            # Higher is better. If < 1, the file grew (negative compression).
            ratio = original_size / comp_size if comp_size > 0 else 0
            exec_time = (end_t - start_t) * 1000  # ms

            self.results.append((name, ratio))
            self.tree.insert("", "end", values=(name, original_size, comp_size, f"{ratio:.2f}x", f"{exec_time:.3f}"))
            logger.info(f"{name} completed: Ratio={ratio:.2f}x, Time={exec_time:.3f}ms")

        self.update_chart()

    def update_chart(self):
        logger.debug("Updating performance chart")
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        names = [r[0] for r in self.results]
        ratios = [r[1] for r in self.results]

        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(names, ratios, color=['#3498db', '#9b59b6', '#2ecc71'])
        ax.axhline(1, color='red', linewidth=0.8, linestyle='--')  # 1x line
        ax.set_ylabel('Compression Ratio (Higher is Better)')
        ax.set_title('Efficiency Benchmark')

        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, f'{yval:.2f}x', ha='center', va='bottom')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
