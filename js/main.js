document.addEventListener("DOMContentLoaded", function() {
  fetch("data/products.json")
    .then(response => response.json())
    .then(data => {
      const productsContainer = document.getElementById("products");
      for (const [category, products] of Object.entries(data)) {
        // Utwórz sekcję dla kategorii
        let categorySection = document.createElement("div");
        categorySection.className = "product-category";
        let categoryTitle = document.createElement("h2");
        categoryTitle.textContent = category;
        categorySection.appendChild(categoryTitle);

        // Dodaj produkty dla tej kategorii
        products.forEach(prod => {
          let prodDiv = document.createElement("div");
          prodDiv.className = "product";
          
          let prodName = document.createElement("h3");
          prodName.textContent = prod.name;
          prodDiv.appendChild(prodName);
          
          let prodDesc = document.createElement("p");
          prodDesc.textContent = prod.description;
          prodDiv.appendChild(prodDesc);
          
          // Jeśli istnieje ścieżka do obrazka, dodaj element <img>
          if (prod.image) {
            let prodImg = document.createElement("img");
            prodImg.src = prod.image;
            prodDiv.appendChild(prodImg);
          }
          categorySection.appendChild(prodDiv);
        });
        productsContainer.appendChild(categorySection);
      }
    })
    .catch(error => console.error("Błąd ładowania produktów:", error));
});
