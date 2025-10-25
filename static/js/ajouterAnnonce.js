
document.addEventListener("DOMContentLoaded", function() {
    const categorieSelect = document.getElementById("id_categorie");
    const sousCategorieSelect = document.getElementById("id_sous_categorie");

    categorieSelect.addEventListener("change", function() {
        const categorieId = this.value;

        fetch(`/get_sous_categories/${categorieId}/`)
            .then(response => response.json())
            .then(data => {
                sousCategorieSelect.innerHTML = '<option value="">---------</option>';
                data.forEach(function(item) {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.nom;
                    sousCategorieSelect.appendChild(option);
                });
            });
    });
});
