import pdfplumber
import json
import os

# Ścieżka do folderu z plikami PDF
pdf_dir = os.path.join("data")

# Lista plików PDF w katalogu
pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

# Struktura na wyekstrahowane produkty
products = {}

def process_text(text):
    """
    Przykładowa funkcja przetwarzania tekstu.
    Zakładamy, że w PDF kategorie są zapisane WIELKIMI literami,
    a linie zawierające produkty mają postać "Nazwa: Opis".
    
    Jeśli linia jest w całości wielkimi literami, traktujemy ją jako kategorię.
    W przeciwnym razie, jeśli zawiera dwukropek, dzielimy ją na nazwę i opis.
    """
    lines = text.split("\n")
    current_category = "Inne"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isupper():
            current_category = line
            if current_category not in products:
                products[current_category] = []
        else:
            if ":" in line:
                parts = line.split(":", 1)
                name = parts[0].strip()
                description = parts[1].strip()
                prod = {
                    "name": name,
                    "description": description,
                    "image": ""  # Dodaj ścieżkę do obrazu, jeśli uda się automatycznie wyekstrahować zdjęcie
                }
                if current_category not in products:
                    products[current_category] = []
                products[current_category].append(prod)
    return

# Przetwórz każdy plik PDF (posortowane alfabetycznie)
for pdf_file in sorted(pdf_files):
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                process_text(text)

# Zapisz dane do pliku JSON w katalogu data
with open(os.path.join("data", "products.json"), "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print("Ekstrakcja zakończona, wyniki zapisane w data/products.json")
