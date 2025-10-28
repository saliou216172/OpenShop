
const sousCategorieUrl = "{% url 'get_sous_categories' %}";

document.addEventListener("DOMContentLoaded", () => {
    const categorieSelect = document.getElementById('categorie');
    const sousCategorieSelect = document.getElementById('sous_categorie');

    categorieSelect.addEventListener('change', function () {
        const categorieId = this.value;

        sousCategorieSelect.innerHTML = '<option>Chargement...</option>';

        if (!categorieId) {
            sousCategorieSelect.innerHTML = '<option value="">-- Sélectionne d’abord une catégorie --</option>';
            return;
        }

        fetch(`${sousCategorieUrl}?categorie_id=${categorieId}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                sousCategorieSelect.innerHTML = '<option value="">-- Sélectionne une sous-catégorie --</option>';
                data.forEach(sc => {
                    const option = document.createElement('option');
                    option.value = sc.id;
                    option.textContent = sc.nom;
                    sousCategorieSelect.appendChild(option);
                });
            })
            .catch(err => {
                console.error(err);
                sousCategorieSelect.innerHTML = '<option value="">Erreur de chargement</option>';
            });
    });
});

