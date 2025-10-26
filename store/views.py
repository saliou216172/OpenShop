from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.forms import AnnonceForm
from.models import Annonce, Categorie, SousCategorie
from django.http import JsonResponse

@login_required(login_url="authentication:login")
def creer_annonce(request):
    step = int(request.POST.get('step', 1))

    # Si POST, créer le formulaire avec request.POST et request.FILES
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES)

        # --------------------------
        # Étape 1 : Suivant
        # --------------------------
        if step == 1 and 'next' in request.POST:
            # rendre les champs de l'étape 2 non requis temporairement
            for field in ['prix', 'photo', 'telephone', 'email_contact']:
                form.fields[field].required = False

            if form.is_valid():
                step = 2
            else:
                step = 1

        # --------------------------
        # Étape 2 : Précédent
        # --------------------------
        elif step == 2 and 'previous' in request.POST:
            step = 1

        # --------------------------
        # Étape 2 : Publier
        # --------------------------
        elif step == 2 and 'publish' in request.POST:
            # rendre tous les champs non requis sauf ceux nécessaires
            for field in ['prix', 'photo', 'telephone', 'email_contact']:
                form.fields[field].required = False

            if form.is_valid():
                annonce = form.save(commit=False)
                annonce.auteur = request.user
                # Vérifier que sous-catégorie correspond à la catégorie
                if annonce.sous_categorie and annonce.sous_categorie.categorie != annonce.categorie:
                    form.add_error('sous_categorie', 'La sous-catégorie ne correspond pas à la catégorie sélectionnée.')
                else:
                    # Sauvegarder l'annonce même si photo est vide
                    annonce.save()
                    return redirect('home')
    else:
        form = AnnonceForm()

    return render(request, 'store/creer_annonce.html', {'form': form, 'step': step})

def home(request):
    categories = Categorie.objects.all()
    return render(request,'store/home.html', {'categories':categories})

def annonces_par_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    sous_categories = categorie.sous_categories.all()
    return render(request, 'store/annonces.html', {
        'categorie': categorie,
        'sous_categories': sous_categories
    })

def annonces_par_souscategorie(request, souscategorie_id):
    annonces = Annonce.objects.filter(sous_categorie_id=souscategorie_id)
    souscategorie = get_object_or_404(SousCategorie, id=souscategorie_id)
    return render(request, 'store/sous_annonces.html', {
        'annonces': annonces,
        'souscategorie': souscategorie
    })


def get_sous_categories(request, categorie_id):
    sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id).values('id', 'nom')
    return JsonResponse(list(sous_categories), safe=False)
