import os
import json
import re
import pdfplumber

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'products.json')

# simplistic regex to capture 5-digit product codes
PRODUCT_RE = re.compile(r'\b(\d{5})\b')


def process_text(text):
    """Clean up whitespace in extracted text."""
    lines = [line.strip() for line in text.split('\n')]
    return [line for line in lines if line]


def parse_pdf(path):
    """Parse a single PDF file and return list of product dicts."""
    products = []
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ''
            for line in process_text(text):
                match = PRODUCT_RE.search(line)
                if match:
                    code = match.group(1)
                    description = line.replace(code, '').strip(' -')
                    products.append(
                        {
                            'code': code,
                            'description': description,
                            'page': page_no,
                            'file': os.path.basename(path),
                        }
                    )
    return products


def main():
    all_products = []
    for filename in sorted(os.listdir(DATA_DIR)):
        if filename.lower().endswith('.pdf'):
            filepath = os.path.join(DATA_DIR, filename)
            all_products.extend(parse_pdf(filepath))

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(all_products)} products to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
