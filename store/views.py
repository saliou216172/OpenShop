from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from.forms import AnnonceForm
from.models import Annonce, Categorie, SousCategorie
from django.http import JsonResponse

@login_required(login_url='authentication:login')
def creer_annonce(request):
    form = AnnonceForm()
    if request.method == "POST":
        form = AnnonceForm(request.POST, request.FILES)
        if form.is_valid():
            annonce = form.save(commit=False)
            annonce.auteur = request.user
            annonce.save()
            return redirect('home')

    categories = Categorie.objects.all()
    return render(request, 'store/creer_annonce.html', {
        'form': form,
        'categories': categories,
    })

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


def get_sous_categories(request):
    """Vue appelée en AJAX pour charger les sous-catégories selon la catégorie choisie"""
    categorie_id = request.GET.get('categorie_id')
    sous_categories = SousCategorie.objects.filter(categorie_id=categorie_id).values('id', 'nom')
    return JsonResponse(list(sous_categories), safe=False)