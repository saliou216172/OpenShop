document.addEventListener("DOMContentLoaded", () => {
    const categorieSelect = document.getElementById('categorie');
    const sousCategorieSelect = document.getElementById('sous_categorie');

    categorieSelect.addEventListener('change', function () {
        const categorieId = this.value;
        sousCategorieSelect.innerHTML = '<option value="">Chargement...</option>';

        if (categorieId) {
            fetch(`/store/get_sous_categories/${categorieId}/`)
                .then(response => response.json())
                .then(data => {
                    sousCategorieSelect.innerHTML = '<option value="">Sélectionne une sous-catégorie</option>';
                    data.forEach(sc => {
                        const option = document.createElement('option');
                        option.value = sc.id;
                        option.textContent = sc.nom;
                        sousCategorieSelect.appendChild(option);
                    });
                })
                .catch(() => {
                    sousCategorieSelect.innerHTML = '<option value="">Erreur de chargement</option>';
                });
        } else {
            sousCategorieSelect.innerHTML = '<option value="">Sélectionne d’abord une catégorie</option>';
        }
    });
});
