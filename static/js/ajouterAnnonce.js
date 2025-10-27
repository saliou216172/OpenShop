document.addEventListener("DOMContentLoaded", () => {
    const categorieSelect = document.getElementById('categorie');
    const sousCategorieSelect = document.getElementById('sous_categorie');

    categorieSelect.addEventListener('change', function () {
        const categorieId = this.value;

        // Message de chargement
        sousCategorieSelect.innerHTML = '<option>Chargement...</option>';

        if (!categorieId) {
            sousCategorieSelect.innerHTML = '<option value="">-- Sélectionne d’abord une catégorie --</option>';
            return;
        }

        fetch(`/store/get_sous_categories/?categorie_id=${categorieId}`)
            .then(response => response.json())
            .then(data => {
                sousCategorieSelect.innerHTML = '<option value="">-- Sélectionne une sous-catégorie --</option>';
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
    });
});