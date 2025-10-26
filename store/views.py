from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.forms import AnnonceForm
from.models import Annonce, Categorie, SousCategorie
from django.http import JsonResponse


@login_required(login_url="authentication:login")
def creer_annonce(request):
    step = int(request.POST.get('step', 1))
    annonce = None

    # Récupérer l'annonce temporaire depuis la session si elle existe
    annonce_id = request.session.get('annonce_id')
    if annonce_id:
        try:
            annonce = Annonce.objects.get(id=annonce_id, auteur=request.user)
        except Annonce.DoesNotExist:
            annonce = None

    if request.method == 'POST':
        # Créer le formulaire avec l'instance si elle existe
        form = AnnonceForm(request.POST, request.FILES, instance=annonce)

        # --------------------------
        # Étape 1 : Suivant
        # --------------------------
        if step == 1 and 'next' in request.POST:
            # rendre champs étape 2 non requis temporairement
            for field in ['prix', 'photo', 'telephone', 'email_contact']:
                form.fields[field].required = False

            if form.is_valid():
                # sauvegarder l'annonce partiellement
                annonce = form.save(commit=False)
                annonce.auteur = request.user
                annonce.save()
                # stocker l'ID de l'annonce pour l'étape 2
                request.session['annonce_id'] = annonce.id
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
            # rendre champs de l'étape 2 non requis sauf ceux nécessaires
            for field in ['prix', 'photo', 'telephone', 'email_contact']:
                form.fields[field].required = False

            if form.is_valid():
                annonce = form.save(commit=False)
                annonce.auteur = request.user
                # vérifier la correspondance sous-catégorie/catégorie
                if annonce.sous_categorie and annonce.sous_categorie.categorie != annonce.categorie:
                    form.add_error('sous_categorie', 'La sous-catégorie ne correspond pas à la catégorie sélectionnée.')
                else:
                    annonce.save()
                    # supprimer l'annonce temporaire de la session
                    if 'annonce_id' in request.session:
                        del request.session['annonce_id']
                    return redirect('home')
    else:
        form = AnnonceForm(instance=annonce)

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
