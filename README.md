# gomarket-reimo

This repository contains PDF catalog files and a script to extract product data using `pdfplumber`.

## How to use

1. Install dependencies:
   ```bash
   pip install pdfplumber
   ```
2. Run the extraction script:
   ```bash
   python script/parse_pdf.py
   ```
   This generates `data/products.json` with parsed product lines.
3. Open `index.html` in your web browser to see the product list loaded dynamically from the JSON file.

The PDFs are located in the `data/` directory.
