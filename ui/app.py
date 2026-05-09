import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import CompressionAlgorithms

class CompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multimedia Compression Lab")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e2e") # Dark background

        self.selected_algo = tk.StringVar(value="Huffman")
        self.style = ttk.Style()
        self.configure_styles()
        self.setup_ui()

    def configure_styles(self):
        self.style.theme_use('clam')
        # Custom styles for a modern look
        self.style.configure("TFrame", background="#1e1e2e")
        self.style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#89b4fa")
        self.style.configure("Card.TLabelframe", background="#1e1e2e", foreground="#89b4fa", borderwidth=2)
        self.style.configure("Card.TLabelframe.Label", font=("Segoe UI", 11, "bold"), foreground="#89b4fa")
        
        # Modern Button
        self.style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=10, background="#89b4fa")
        self.style.map("Action.TButton", background=[('active', '#74c7ec')])

        # Modern Treeview
        self.style.configure("Treeview", background="#313244", foreground="white", fieldbackground="#313244", borderwidth=0)
        self.style.configure("Treeview.Heading", background="#45475a", foreground="white", font=("Segoe UI", 10, "bold"))

    def setup_ui(self):
        # Header
        ttk.Label(self.root, text="Multimedia Compression System", style="Header.TLabel").pack(pady=20)

        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=30)

        # 1. Input Section
        input_card = ttk.LabelFrame(main_container, text=" 1. Text Source ", style="Card.TLabelframe")
        input_card.pack(fill="x", pady=10)

        btn_row = ttk.Frame(input_card)
        btn_row.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_row, text="📂 Load File", command=self.load_file, style="Action.TButton").pack(side="left", padx=5)
        ttk.Button(btn_row, text="🧹 Clear All", command=self.clear_input, style="Action.TButton").pack(side="left", padx=5)

        self.input_text = scrolledtext.ScrolledText(input_card, height=6, bg="#313244", fg="#cdd6f4", insertbackground="white", borderwidth=0, font=("Consolas", 11))
        self.input_text.pack(fill="x", padx=15, pady=10)

        # 2. Controls
        ctrl_card = ttk.Frame(main_container)
        ctrl_card.pack(fill="x", pady=10)

        ttk.Label(ctrl_card, text="Algorithm:").pack(side="left", padx=5)
        algo_combo = ttk.Combobox(ctrl_card, textvariable=self.selected_algo, 
                                  values=["RLE", "Shannon-Fano", "Arithmetic", "Huffman", "LZW"], 
                                  state="readonly", width=15)
        algo_combo.pack(side="left", padx=10)

        ttk.Button(ctrl_card, text="⚡ Compress", command=self.compress, style="Action.TButton").pack(side="left", padx=5)
        ttk.Button(ctrl_card, text="📊 Compare All", command=self.start_comparison_thread, style="Action.TButton").pack(side="left", padx=5)
        
        self.progress = ttk.Progressbar(ctrl_card, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(side="right", padx=20)

        # 3. Results Section
        res_container = ttk.Frame(main_container)
        res_container.pack(fill="both", expand=True, pady=10)

        # Table (Left Side)
        table_card = ttk.LabelFrame(res_container, text=" Results Table ", style="Card.TLabelframe")
        table_card.pack(side="left", fill="both", expand=True, padx=(0, 10))

        cols = ("Algorithm", "Original (B)", "Compressed (B)", "Ratio", "Time (ms)")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Chart (Right Side)
        chart_card = ttk.LabelFrame(res_container, text=" Efficiency Graph ", style="Card.TLabelframe")
        chart_card.pack(side="right", fill="both", expand=True)
        self.chart_frame = tk.Frame(chart_card, bg="#1e1e2e")
        self.chart_frame.pack(fill="both", expand=True)

    # --- Logic ---

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if path:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", f.read())

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        for row in self.tree.get_children(): self.tree.delete(row)
        for w in self.chart_frame.winfo_children(): w.destroy()
        self.progress['value'] = 0

    def compress(self):
        data = self.input_text.get("1.0", tk.END).strip()
        # Auto-ignore non-ascii characters to prevent dictionary errors
        data = data.encode("ascii", "ignore").decode("ascii")
        if not data: return
        
        algo = self.selected_algo.get()
        funcs = {
            "RLE": CompressionAlgorithms.rle_compress,
            "Shannon-Fano": CompressionAlgorithms.shannon_fano_compress,
            "Arithmetic": CompressionAlgorithms.arithmetic_compress,
            "Huffman": CompressionAlgorithms.huffman_compress,
            "LZW": CompressionAlgorithms.lzw_compress
        }
        
        start = time.perf_counter()
        comp = funcs[algo](data)
        end = time.perf_counter()
        
        size = len(comp) // 8 if algo in ["Shannon-Fano", "Arithmetic", "Huffman"] else len(comp)
        ratio = len(data) / max(size, 1)
        
        # Clear and update table for single view
        for row in self.tree.get_children(): self.tree.delete(row)
        self.tree.insert("", "end", values=(algo, len(data), size, f"{ratio:.2f}x", f"{(end-start)*1000:.2f}"))

    def start_comparison_thread(self):
        # Run in thread to keep GUI responsive during animation
        threading.Thread(target=self.compare_all, daemon=True).start()

    def compare_all(self):
        data = self.input_text.get("1.0", tk.END).strip()
        # Auto-ignore non-ascii characters to prevent dictionary errors
        data = data.encode("ascii", "ignore").decode("ascii")
        if not data: return

        self.root.after(0, lambda: self.tree.delete(*self.tree.get_children()))
        algos = [
            ("RLE", CompressionAlgorithms.rle_compress),
            ("Shannon-Fano", CompressionAlgorithms.shannon_fano_compress),
            "Arithmetic", CompressionAlgorithms.arithmetic_compress,
            "Huffman", CompressionAlgorithms.huffman_compress,
            "LZW", CompressionAlgorithms.lzw_compress
        ]

        results = []
        for i, (name, func) in enumerate(algos):
            # Update Progress Bar
            progress_val = ((i + 1) / len(algos)) * 100
            self.root.after(0, lambda v=progress_val: self.progress.configure(value=v))
            
            start = time.perf_counter()
            comp = func(data)
            end = time.perf_counter()
            
            # Logic: bit strings are divided by 8 to get bytes
            size = len(comp) // 8 if name in ["Shannon-Fano", "Arithmetic", "Huffman"] else len(comp)
            ratio = len(data) / max(size, 1)
            results.append((name, len(data), size, ratio, (end-start)*1000))
            
            # Dynamic table update
            self.root.after(0, lambda n=name, o=len(data), s=size, r=ratio, t=(end-start)*1000: 
                           self.tree.insert("", "end", values=(n, o, s, f"{r:.2f}x", f"{t:.2f}")))
            time.sleep(0.2) # Small delay to show animation

        self.root.after(0, lambda: self.draw_chart(results))

    def draw_chart(self, results):
        for w in self.chart_frame.winfo_children(): w.destroy()
        
        names = [r[0] for r in results]
        # Calculate size difference (Original - Compressed)
        differences = [r[1] - r[2] for r in results]

        # Use a dark style for the plot
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#1e1e2e')
        ax.set_facecolor('#1e1e2e')
        
        colors = ['#f38ba8', '#89b4fa', '#a6e3a1', '#cba6f7', '#f9e2af']
        bars = ax.bar(names, differences, color=colors)
        
        ax.set_ylabel('Difference (Bytes)', fontsize=9)
        ax.axhline(0, color='gray', linewidth=0.8)
        ax.tick_params(axis='x', labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        y_min, y_max = ax.get_ylim()
        padding = (y_max - y_min) * 0.15
        ax.set_ylim(y_min - padding if y_min < 0 else 0, y_max + padding)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'{int(yval)}B', 
                    ha='center', va='bottom' if yval >= 0 else 'top', fontsize=8, color='white')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
