
// --- Récupération dynamique des sous-catégories ---
document.getElementById('categorie').addEventListener('change', function () {
    const categorieId = this.value;
    const sousCategorieSelect = document.getElementById('sous_categorie');
    sousCategorieSelect.innerHTML = '<option value="">Chargement...</option>';

    if (categorieId) {
        fetch(`/store/get_sous_categories/?categorie_id=${categorieId}`)
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

