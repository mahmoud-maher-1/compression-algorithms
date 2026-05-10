# Multimedia Compression Algorithms

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

A modern, dark‑themed desktop application that demonstrates **five classic lossless compression algorithms** on text data.  
Ideal for students, educators, and anyone exploring how multimedia data can be reduced in size without losing information.

---

## ✨ Features

- 📂 **Load text files** or type directly into the editor.
- ⚡ **Single algorithm compression** – select one of five techniques and instantly see:
  - Original & compressed size (bytes)
  - Compression ratio
  - Execution time
- 📊 **Compare All** – run all algorithms simultaneously with a **progress bar** and a detailed **benchmark table**.
- 📈 **Dynamic bar chart** showing compression ratios for visual comparison.
- 🧵 **Threaded execution** keeps the GUI responsive during comparisons.
- 🎨 **Clean, modern UI** with custom styles and a dark colour palette.

---

## 🧠 Implemented Algorithms

| Algorithm | Type | Description |
|-----------|------|-------------|
| **Run‑Length Encoding (RLE)** | Lossless | Replaces consecutive identical characters with a count. Efficient for highly repetitive data. |
| **Shannon‑Fano Coding** | Lossless | A top‑down entropy coding method that splits symbols into roughly equal probability groups. |
| **Arithmetic Coding** | Lossless | Represents the entire message as a single fractional number. (Simplified for educational use) |
| **Huffman Coding** | Lossless | Bottom‑up optimal prefix coding using a frequency‑based binary tree. |
| **Lempel‑Ziv‑Welch (LZW)** | Lossless | Dictionary‑based compression that builds a table of repeated sub‑strings on the fly. |

> **Note:** For Arithmetic Coding, the implementation uses a **truncated input** (first 100 characters) and a representative bit‑pattern to avoid floating‑point precision issues. This is sufficient for demonstration but not for production use.

---

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/multimedia-compression-lab.git
   cd multimedia-compression-lab
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install matplotlib
   ```
   `tkinter` usually comes bundled with Python. If not, install it via your package manager (e.g., `sudo apt install python3-tk` on Ubuntu).

4. **Run the app**
   ```bash
   python main.py
   ```

---

## 🚀 Usage

1. **Enter text** – either type directly in the editor or click *Load File* to open a `.txt` document.
2. **Choose an algorithm** from the dropdown list.
3. **Click *Compress*** to see the result for that algorithm alone.
4. **Click *Compare All*** to benchmark all five algorithms at once – you’ll get a table and a chart.
5. The **compressed output** is displayed in the interface. You can save it using the *Save Compressed File* button.

---

## 📁 Project Structure

```
multimedia-compression-lab/
├── main.py               # Main application file
├── README.md             # This file
├── requirements.txt      # Optional dependency list
└── assets/               # Screenshots and icons (for documentation)
```

---

## 📦 Dependencies

- Python 3.8+
- [matplotlib](https://matplotlib.org/) – for chart rendering
- Standard library modules: `tkinter`, `heapq`, `itertools`, `math`, `threading`

A minimal `requirements.txt` file is provided:
```
matplotlib>=3.5.0
```

---

## ⚠️ Limitations

- **Arithmetic Coding** is a simplified textbook implementation. For large inputs it uses a truncated sample and a placeholder bit‑pattern; ratio results may therefore be approximate.
- Size measurements for bit‑oriented outputs (Shannon‑Fano, Arithmetic, Huffman) convert bits to bytes by integer division, simulating a realistic storage scenario but not an exact binary file.
- The primary goal is **educational demonstration** – not production compression speed or efficiency.

---

## 👤 Authors

**Akram ElNahtawy**  
[GitHub](https://github.com/KemoMoh11) • [LinkedIn](https://linkedin.com/in/akram-elnahtawy)

**Mahmoud Maher**  
[GitHub](https://github.com/mahmoud-maher-1) • [LinkedIn](https://linkedin.com/in/mahmoudmaherm)

---

*Happy compressing!* 🚀  
If you find this project useful, please consider giving it a ⭐ on GitHub.
