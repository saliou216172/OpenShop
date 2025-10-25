# models.py
from django.db import models
from django.conf import settings
from PIL import Image as image

class Categorie(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.nom

class SousCategorie(models.Model):
    nom = models.CharField(max_length=50)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='sous_categories')

    class Meta:
        verbose_name_plural = "sous-categories"
        unique_together = ('nom', 'categorie')  # pas de doublon pour la même catégorie

    def __str__(self):
        return f"{self.nom} ({self.categorie.nom})"

class Annonce(models.Model):
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="annonces"
    )
    titre = models.CharField(max_length=100)
    description = models.TextField()
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    sous_categorie = models.ForeignKey(SousCategorie, on_delete=models.CASCADE, null=True, blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(upload_to="annonces/", null=True, blank=True)
    telephone = models.CharField(max_length=15)
    email_contact = models.EmailField(null=True, blank=True)
    date_pub = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            img = image.open(self.photo.path)
            max_size = (800, 600)
            img.thumbnail(max_size)
            img.save(self.photo.path)

    def __str__(self):
        return f"{self.titre} - {self.categorie.nom} - {self.sous_categorie.nom if self.sous_categorie else ''}"
