# Register your models here.
# admin.py
from django.contrib import admin
from .models import Categorie, SousCategorie, Annonce

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(SousCategorie)
class SousCategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie')
    search_fields = ('nom',)
    list_filter = ('categorie',)

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = (
        'titre',
        'categorie',
        'sous_categorie',
        'auteur',
        'prix',
        'premium_status',
        'date_pub'
    )

    list_filter = (
        'categorie',
        'sous_categorie',
        'is_premium',
        'date_pub'
    )

    search_fields = ('titre', 'description', 'auteur__username')

    fields = (
        'auteur',
        'titre',
        'description',
        'categorie',
        'sous_categorie',
        'prix',
        'photo',
        'telephone',
        'email_contact',
        'is_premium',
        'premium_until',
    )

    def premium_status(self, obj):
        if obj.is_active_premium():
            return "⭐ Actif"
        return "Normal"

    premium_status.short_description = "Statut"