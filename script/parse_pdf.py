import pdfplumber
import json
import os

# Ścieżka do folderu z plikami PDF
pdf_dir = os.path.join("data")

# Utwórz listę plików PDF w katalogu
pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]

# Upewnij się, że folder na obrazy istnieje
images_dir = os.path.join("data", "images")
os.makedirs(images_dir, exist_ok=True)

# Słownik na wyekstrahowane produkty
products = {}

def process_page(page, pdf_filename):
    """
    Przetwarza jedną stronę PDF:
      - Ekstrahuje obrazy i zapisuje je do katalogu images.
      - Ekstrahuje tekst i na podstawie niego tworzy produkty.
      - Jeśli na stronie są obrazy, przypisuje je do kolejnych produktów w kolejności.
    """
    # Ekstrakcja obrazów
    extracted_images = []
    if page.images:
        for i, img in enumerate(page.images):
            try:
                img_data = page.extract_image(img["object_id"])
                image_filename = f"{os.path.splitext(os.path.basename(pdf_filename))[0]}-page{page.page_number}-img{i}.png"
                image_path = os.path.join(images_dir, image_filename)
                with open(image_path, "wb") as f:
                    f.write(img_data["image"])
                extracted_images.append(image_path)
            except Exception as e:
                print(f"Error extracting image on page {page.page_number}: {e}")

    # Ekstrakcja tekstu i przypisywanie produktów
    text = page.extract_text()
    if not text:
        return

    lines = text.split("\n")
    current_category = "Inne"
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Przyjmujemy, że linie zapisana WIELKIMI literami to nagłówki kategorii
        if line.isupper():
            current_category = line
            if current_category not in products:
                products[current_category] = []
        else:
            # Produkty mają postać "Nazwa: Opis"
            if ":" in line:
                parts = line.split(":", 1)
                name = parts[0].strip()
                description = parts[1].strip()
                prod = {
                    "name": name,
                    "description": description,
                    "image": ""
                }
                # Jeżeli z tej strony udało się wyekstrahować obraz, przypisz pierwszy dostępny
                if extracted_images:
                    prod["image"] = extracted_images.pop(0)
                products.setdefault(current_category, []).append(prod)

# Przetwarzamy każdy plik PDF (sortowane alfabetycznie)
for pdf_file in sorted(pdf_files):
    with pdfplumber.open(pdf_file) as pdf:
        print(f"Przetwarzam plik: {pdf_file}")
        for page in pdf.pages:
            process_page(page, pdf_file)

# Zapisz dane do pliku JSON
with open(os.path.join("data", "products.json"), "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

print("Ekstrakcja zakończona, wyniki zapisane w data/products.json")
