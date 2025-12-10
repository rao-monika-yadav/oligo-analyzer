# 🧬 Oligo Analyzer Pro

**A professional bioinformatics dashboard for primer design and QC. Features include batch FASTA processing, Tm & Molecular Weight calculation, GC visualization, and instant reverse complement generation. Built with Python & Streamlit.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here)

## 📌 Overview
The **Oligo Analyzer** is a web-based application built to streamline the workflow of molecular biologists. It replaces manual calculations and Excel sheets with an automated, error-free dashboard. 

It handles both **single-sequence analysis** for quick checks and **batch processing** for analyzing hundreds of primers from FASTA files simultaneously.

## 🚀 Key Features
* **Accurate Tm Calculation:** Uses the standard **Wallace Rule** (`2°C * (A+T) + 4°C * (G+C)`) for short oligos.
* **Batch Processing:** Upload `.fasta` or `.txt` files to analyze 50+ sequences in seconds.
* **Quality Control (QC):**
    * Interactive **Scatter Plots** to identify outliers (e.g., primers with extreme GC% or Tm).
    * **Nucleotide Composition** charts for visual validation.
* **Reverse Complement:** Instantly generates the 5'-3' reverse complement for ordering.
* **Export Ready:** One-click download of full reports as `.csv` files.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Framework:** Streamlit (Web UI)
* **Data Manipulation:** Pandas
* **Visualization:** Streamlit Native Charts

## 🧪 Scientific Logic
The tool calculates parameters based on standard molecular biology formulas:
1.  **Melting Temperature (Tm):** Calculated using the Wallace Rule for oligos < 50bp.
2.  **GC Content:** `(G + C) / Length * 100`
3.  **AT Content:** `(A + T) / Length * 100`
4.  **Molecular Weight:** Uses standard atomic weights for ssDNA (accounting for phosphate removal).

## 💻 How to Run Locally
If you want to run this tool on your own machine:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/rao-monika-yadav/oligo-analyzer.git](https://github.com/rao-monika-yadav/oligo-analyzer.git)
    ```
2.  **Install dependencies**
    ```bash
    pip install streamlit pandas
    ```
3.  **Run the app**
    ```bash
    streamlit run app.py
    ```

## 👨‍🔬 Author
**Monika Yadav**
* MSc Bioinformatics Candidate
* BSc/MSc Biotechnology

[LinkedIn](will add soon) | [GitHub](https://github.com/rao-monika-yadav)

---

*Disclaimer: This tool is intended for research and educational purposes only.*

