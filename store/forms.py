# forms.py
from django import forms
from .models import Annonce, Categorie, SousCategorie

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'categorie', 'sous_categorie', 'prix', 'photo', 'telephone', 'email_contact']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’annonce'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description détaillée'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'sous_categorie': forms.Select(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix en GNF'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre numéro whatssap'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (facultatif)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre la sous-catégorie vide au début, elle sera remplie selon la catégorie
        self.fields['sous_categorie'].queryset = SousCategorie.objects.none()

        if 'categorie' in self.data:
            try:
                categorie_id = int(self.data.get('categorie'))
                self.fields['sous_categorie'].queryset = SousCategorie.objects.filter(categorie_id=categorie_id).order_by('nom')
            except (ValueError, TypeError):
                pass  # ignore invalid input
        elif self.instance.pk:
            self.fields['sous_categorie'].queryset = self.instance.categorie.sous_categories.order_by('nom')
